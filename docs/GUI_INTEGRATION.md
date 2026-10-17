# Game side integration guide (threaded game loop)

This document explains how the game runs now that the game loop lives in its own
thread, and exactly what the GUI must (and must not) do. Read the "Rules" section
before wiring anything up — the design is deliberately simple, but only if you
follow the contract.

## TL;DR

```python
from src.game.Game import mandatory_game

game = mandatory_game(config)   # returns IMMEDIATELY, game already running in a worker thread
```

From that point:

- the **main thread** owns pyray/raylib — window, input, rendering, animations
- the **worker thread** runs the whole game (all levels) at a fixed 100 Hz
- the GUI **reads** game attributes every frame and **pushes intents** through
  a few methods. That is the entire interaction.

## Threading model

| Thread | Runs | Never does |
|---|---|---|
| Main (GUI) | raylib render loop, input polling, animations, `resume()`/`stop()` | never calls `update_game`, `game.start()`, or spawns its own game thread |
| Worker (game) | `Game.start()` → all maps, fixed-timestep ticks | never touches raylib or the window |

No locks, no queues, no callbacks are needed anywhere in the GUI. CPython's GIL
makes every single-attribute read/write below atomic. Do not add
`threading.Lock` for game state — it is not required and can only cause trouble.

## The one entry point

`mandatory_game(config: Config) -> Game`

- Generates all levels (`nb_level`, default 10) and starts the worker thread.
- Returns in a few milliseconds — it does **not** block.
- The game starts **paused**, parked on the first level, with
  `game.state == Game_state.PAUSED`. It waits for the GUI to call `resume()`
  (typically when the player presses "start").
- Do not call `Game.start()` or `Game.start_async()` yourself —
  `mandatory_game` already did it. Calling `start_async()` again is guarded,
  but pointless.

`config` comes from the normal `App.load_config(...)` flow (a `Config` object).

## What to read each frame (all safe to poll at 60 fps)

| Data | Access | Notes |
|---|---|---|
| Score | `game.player.score` | int, add `game.config.point_per_ghost` per eaten ghost |
| Level timer | `game.timer` | int, seconds remaining of the current level, counts down |
| Lives | `game.player.nb_lives` | int |
| Pacman position | `game.player.pos_x`, `.pos_y` | floats in cell units; cell centers are `x + 0.5` |
| Pacman direction | `game.player.direction` | `"N"`, `"S"`, `"E"`, `"W"` — for sprite orientation |
| Energized | `game.player.is_energized` | True for ~6 s after a super pacgum |
| Map cells | `game.map[game.map_index].cells` | 2D list indexed `cells[y][x]`; `cell.walls` dict, `cell.collectible` |
| Current map | `game.map_index` | always valid (clamped by the game), never out of range |
| Ghosts | `game.ghosts["BLINKY"]`, `["PINKY"]`, `["CLYDE"]`, `["INKY"]` | each has `pos_x`, `pos_y`, `direction`, `state` (`Ghost_state`) |
| Game state | `game.state` | see state machine below |

Positions are continuous floats; render them interpolated between cells —
that is what gives smooth movement at any frame rate.

## The state machine — what the GUI must react to

`game.state` is a `Game_state` enum (from `src.utils.enum_utils`):

| State | Meaning | What the GUI should do |
|---|---|---|
| `PAUSED` | waiting at the start of a map | show "press start" / ready screen, then `game.resume()` |
| `RUNNING` | normal play | nothing — just render |
| `DIED` | pacman lost a life; entities reset to spawns | play the death animation, then `game.resume()` |
| `FINISHED_MAP` | map cleared; next map is ready | play the "level cleared" animation, then `game.resume()` |
| `LOST` | game over (no lives left, or level timer expired) | show game over |
| `WON` | all maps cleared | show victory |
| `ERROR` | an exception occurred in the game thread | show an error message; the traceback is on stderr |

Key property: **while paused (`PAUSED`/`DIED`/`FINISHED_MAP`) the worker thread
is parked and consumes zero CPU.** You can take as long as you want for
animations; nothing moves, no timer runs. `resume()` wakes it within about one
tick (~10 ms — always less than one render frame).

## What the GUI writes (the complete list)

```python
game.player.set_next_direction("N")   # or "S", "E", "W" — queue the next turn
game.resume()                          # leave PAUSED / DIED / FINISHED_MAP
game.pause(Game_state.PAUSED)         # pause menu (any status is fine, PAUSED is the usual)
game.stop()                            # request worker shutdown (e.g. on quit)
game.join(2.0)                         # wait up to 2 s for a clean shutdown
```

`set_next_direction` is consumed when pacman next crosses a cell center —
that is the arcade-style input buffer, not input lag. Invalid strings are
ignored.

### Quit protocol (in this order)

```python
game.stop()      # ask the worker to exit
game.join(2.0)   # wait politely; returns even if something is stuck
```

`stop()` while paused is safe — the loop wakes parked threads on stop.
The worker thread is a daemon, so even a worst-case hang cannot block
process exit; `join` is the polite path.

## What to delete from the current GUI branch

The GUI branch carries an old copy of the game with a temporary hack. On
integration:

1. **Delete `Pac_man.test_update` and every call to it** (`Game_view.catch_player_input`).
   The worker thread replaces this — the GUI used to step pacman itself, which
   is exactly what the thread now does (properly, at a fixed rate, ghosts included).
2. **Replace the `is_paused`/`is_won` int flags with `game.state`**
   (`Game_state` enum, table above). The int API no longer exists.
3. **Drop the GUI's own map generation** (`game.map.append(game.generate_map(...))`,
   `game.start_position()` in `Game_view.__init__`) — `mandatory_game` prepares
   everything. Keep only `game.map[game.map_index]` reads for rendering.

## Rules (why this is safe — and stays safe)

1. **One writer per field.** The worker writes score/timer/positions/states; the
   GUI only reads them. The GUI writes direction/pause/resume/stop; the worker
   only reads them. Single-attribute writes are atomic under the GIL. This
   split must stay clean: the GUI must never, for instance, modify
   `game.player.pos_x` to teleport pacman.
2. **Never call game-loop internals from the GUI**: no `update_game`, no
   `game.game_loop.run/pause/resume/stop` (use the `Game` methods instead),
   no direct fiddling with `GameLoop` attributes.
3. **raylib on the main thread only** — window, input, drawing. The worker never
   touches pyray.
4. **Do not spawn a second thread for the game** — `mandatory_game` owns the
   only one. Restarting a finished game means building a new `Game` via
   `mandatory_game` again (fresh object, fresh thread).
5. Reading `(pos_x, pos_y)` together can catch a one-frame-old value for one of
   the two — worst case is sub-pixel on screen. Ignore it; do not add locks.

## Minimal render-loop skeleton

```python
game = mandatory_game(app.config)          # once, at app start
ready_screen_shown = False

while not window_should_close():           # main thread, raylib loop
    # input
    if key_pressed(KEY_UP):    game.player.set_next_direction("N")
    if key_pressed(KEY_DOWN):  game.player.set_next_direction("S")
    if key_pressed(KEY_LEFT):  game.player.set_next_direction("W")
    if key_pressed(KEY_RIGHT): game.player.set_next_direction("E")

    # state machine
    st = game.state
    if st == Game_state.PAUSED and not ready_screen_shown:
        show_ready_screen()
        ready_screen_shown = True
    elif st == Game_state.DIED:
        play_death_animation()             # takes as long as you want
        game.resume()
    elif st == Game_state.FINISHED_MAP:
        play_map_cleared_animation()
        game.resume()
    elif st == Game_state.LOST or st == Game_state.WON:
        show_end_screen(st)                # or change_view(...)
    elif st == Game_state.ERROR:
        show_error_screen()

    # render: read game.map[game.map_index], entities positions, score, timer...
    draw_everything(game)

# on quit
game.stop()
game.join(2.0)
close_window()
```

## Quick reference — timing facts (measured)

- Worker ticks at a fixed 100 Hz; the game clock is exact regardless of pauses
  (paused time is never added to the level timer).
- Parked game consumes ~0 CPU (measured 0.1 ms over 2 s).
- `resume()` takes effect within one tick (~10 ms), i.e. always inside your
  next render frame.
- Quit while parked: `stop()` + `join()` completes in well under 1 ms.
- A game-thread crash becomes `game.state == Game_state.ERROR` with the
  traceback printed to stderr — the GUI never freezes silently.
