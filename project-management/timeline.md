# Project Timeline - Pac-Man

This timeline is reconstructed from the full commit history of the
repository (all branches, 360+ commits between September 8 and
November 12) and is part of the project management evidence.

## The team, as seen by the history

| Contributor | Commits | Role visible in the history |
|---|---|---|
| gabach | 171 | Game engine: config, maze integration, entities, game loop, threading, scores, custom maps, cheats, compliance |
| ibady | 162 | GUI: menus, views, widget framework, texture packs, rendering, map editor front-end, pull request merges into dev |

The project ran on two parallel tracks the whole way, one member
on each: the engine on `feat/*` branches merged into `dev`, and the
GUI on `features/menu`, updated and re-merged each time `dev` moved.

## Gantt view of the phases

| Phase | From | To | Track | Integrated by |
|---|---|---|---|---|
| 1. Project setup | 08-09 | 14-09 | engine | - |
| 2. GUI foundations | 10-09 | 25-09 | gui | - |
| 3. Maze generation, config | 21-09 | 23-09 | engine | PR #1, #2 (22-09) |
| 4. Game loop v1 | 22-09 | 25-09 | engine | PR #3 (28-09) |
| 5. Entities and AI | 25-09 | 04-10 | engine | PR #4 (02-10) |
| 6. Pac-Man and collectibles | 03-10 | 04-10 | engine | PR #6 (04-10) |
| 7. Game assembly + rendering | 05-10 | 06-10 | both | PR #7, #8, #9, #10 (05-10) |
| 8. A* ghost pathfinding | 11-10 | 12-10 | engine | PR #11 (12-10) |
| 9. Game start + threading | 17-10 | 24-10 | engine | PR #12 (17-10), #13 (24-10) |
| 10. Scores + custom maps | 19-10 | 28-10 | engine | PR #14, #15 (28-10) |
| 11. Widget framework + options | 22-09 | 06-11 | gui | PR #16 (06-11) |
| 12. Cheat mode | 02-11 | 06-11 | engine | PR #17 (06-11) |
| 13. Blinking power-up | 03-11 | 03-11 | engine | PR #18 (03-11) |
| 14. Map editor front-end | 08-11 | 11-11 | gui | - |
| 15. Subject compliance | 10-11 | 12-11 | engine | - |

## Detailed chronology

### September 2026 - foundations

- **08-09**: repository created. Makefile, main file, team workflow
  rules written into the README, uv project initialized. First CI
  workflows (lint on pull requests, dev-only merges to main).
- **10-09**: project structure laid out (`src/` packages); first pyray
  experiments for a main menu; class definitions drafted for split
  work; dependencies added to pyproject. Both tracks start working.
- **11-09 to 15-09**: main menu takes shape (design, gif animations,
  buttons, title icon); the map choice menu and first input box are
  drafted; the guides for the JSON utils are written.
- **17-09**: the default texture pack and sprite animation are ready.
- **21-09**: the A-Maze-ing package (mazegenerator) is integrated;
  conversion from its maze grid to a Pac-Man map begins.
- **22-09**, the busiest day of the month (24 commits): the map
  conversion is finished, the maze-generator branch integrated,
  **PR #1 (config file)** and **PR #2 (maze generator integration)**
  are merged the same day; the widget library gets its own branch
  (Widget, Panel, Input_box, Icon); the Luigi texture pack is drawn;
  the game loop is started.
- **25-09**: big parallel day - the four ghosts on the engine side
  (Entity base class, state enum, Blinky/Pinky/Inky/Clyde targeting,
  frightened wandering) while the GUI side refactors Panel, fixes the
  input box action tuples, and the animation frame delay.
- **28-29-09**: ghost behavior finished (state machine, frightened
  timer), **PR #3 (game loop)** merged; the scores view is tested
  with placeholder data on the GUI side.

### October 2026 - the engine comes together

- **02-10**: **PR #4 (ghosts)** merged; the map renderer starts
  drawing walls; the ghost targeting is refined to be closer to
  the real Pac-Man.
- **03-10**: Pac-Man comes alive - super pacgum, update function,
  direction queue (this is also when the map is prepared for
  several collectible types).
- **04-10**: **PR #6 (pacman)** merged; wall rendering "pretty much
  finished"; GameLoop exposes the elapsed time.
- **05-10**, the biggest engine day (29 commits): collisions,
  update_game, consumables, spawn/scatter wiring, and a long
  lint and fix session; **PR #7, #8, #9 and #10 merged the same
  day**; the GUI merges dev and builds the collectible and entity
  display.
- **06-10**: entity textures finally displayed on the map, the
  views get a resize-check refactor.
- **08-10**: the Dropdown widget is born (first in Scores view).
- **11-10**: A* pathfinding experiments for the ghosts, adapted to
  the real Pac-Man no-turn-back rules; endgame view started.
- **12-10**: **PR #11 (A* path finding)** merged after a full
  rewrite of the algorithm to respect the game rules; the Text
  widget lands and every view is refactored to use it.
- **13-10**: the Pac-Man font (Crackman) is implemented.
- **15 to 16-10**: Dropdown overlap fixes, Panel refactor, cheat panel
  front-end is set up.
- **17-10**, the big game-start day (15 commits): dead ends of the
  a-star branch are squashed into a single clean history; mandatory
  game mode, ghost-eaten-twice fix, map-index guard, game start
  rendering fix, precise_sleep removal, first-resume safe guard,
  error state, and the **GUI integration guide**; **PR #12 (game
  start)** merged the same day.
- **19-10**: scores branch starts - clearer JSON errors, the JSON
  write helper, Map_scores is finished.
- **20-24-10**: persistence of custom maps - Map_info classes,
  saving/loading of the maps, the map creator back-end class, the
  .maps folder in App, empty-map generation; the engine interfaces
  move to the threaded game (mandatory_game, custom_game,
  get_stored_map_list); **PR #13 (multithreading)** merged on the
  24th and the GUI immediately adapts its calls to the new loop.
- **27-28-10**: the widget framework catches up (Dropdown, Text
  widget, Input_box improvements) and the two big persistence
  branches land: **PR #14 (scores)** and **PR #15 (map creation)**
  are merged on the 28th, the same day the widget and menu branches
  are synced to the new dev.

### November 2026 - polish and compliance

- **01-11**: debug session on the options view (fonts, input areas);
  the Gohu font is added as the new default.
- **02-11**: the cheat mode is built on the engine side
  (GameCheats, clipping with all its border fixes, invincibility);
  on the GUI side, the y-flip error of the grid is solved, the
  game loop moves into App, and texture/image handling is fixed
  (dropdown, input padding, icon texture unloading).
- **03-11**: **PR #18 (frightened blinking)** - the power-up now
  shows its end; the GUI writes the new keybind input box and
  fixes the death animation.
- **05-06-11**: the cheat mode becomes the integration point:
  the GUI tests the cheat panel, the engine adjusts lives/points
  semantics, **PR #16 (widgets)** and **PR #17 (cheats)** merged
  on the 6th.
- **07-09-11**: custom map editor front-end (wall selection tool,
  entity placement, texture display fixes, smoother entity motion).
- **10-11**: subject compliance wave - the instruction file, the
  top-10 and name rules on the scores, the generator guard, the
  collectibles textures in the game view.
- **11-11**: the custom map view is finished with its countdown.
- **12-11**: final wave - the docstrings pass over the whole
  engine and widgets, the lint-strict errors are resolved.

## Activity profile

- 360+ commits over 66 calendar days, on 28 different days with
  commits; the median day has 2 commits, the busiest days are
  22-09 (24), 05-10 (29), 25-09 (28) and 28-10 (23).
- Work runs in weekly to biweekly sprints visible in the PR flow:
  a branch lives on its feature track, then a wave of merges lands
  in dev the same day (22-09, 05-10, 28-10, 06-11).
- The history also keeps its scars, which is itself evidence:
  an a-star branch with commits named "wtf", "wft 2" and "I think
  this is the end" that was finally squashed into one clean commit;
  a "kitty won't work ;-;" debug commit while testing the wall
  display; the "pushing again to see if flake8 passes" loop in
  the widget branch.
- Notable blocking point visible in the history: the map renderer
  went through a "fix/map_rendering" branch on 02-11 (textures,
  y flip, image handling) before the game view became playable.

## How this timeline maps to the deliverables

- The engine milestones match the merged pull requests: the engine
  is finished for the mandatory game on 17-10 (PR #12), becomes
  threaded on 24-10 (PR #13), persists scores and maps on 28-10
  (PR #14, #15), gains cheats on 06-11 (PR #17).
- The GUI milestones are the widget branch (merged 06-11, PR #16)
  and the map editor view (finished 11-11).
- Everything after 10-11 is compliance work: instructions, score
  rules, error handling of the external package, docstrings.
