# GUI code review & performance findings

Review of the view layer (`features/menu` render path + `features/widgets`
widget framework). Written from a full code reading plus benchmarks of the
game engine on `dev`; the GUI itself could not be executed (no display on
the analysis machine), so per-frame *construction patterns* are certain —
they are in the code — while millisecond figures are engineering estimates
from pyray call costs.

Read the "Priority" column first: item 1 will make the game unplayable and
crash on its own, item 6 freezes the window on a French keyboard.

| # | Where | Priority | One-line summary |
|---|---|---|---|
| 1 | `Map_renderer.draw_cell` | **BLOCKER** | Every collectible is loaded from disk and uploaded to the GPU **every frame**, and old textures are never freed |
| 2 | `Map_renderer.draw_grid` | High | Static maze walls re-issued as thousands of raw draw calls every frame |
| 3 | `Map_renderer.get_neighbors` | Medium | Neighbor dicts rebuilt for every cell, every frame |
| 4 | `Map_renderer.draw_cell` (sprites) | Medium | Entity sprites re-load their GIF from disk on every direction/state change |
| 5 | `Dropdown._update_icon` | Medium | Arrow icon (PNG + texture) constructed every frame while visible |
| 6 | `Input_box._update_widget` | **BLOCKER** | First keystroke is duplicated; an out-of-range key on an empty box loops forever |
| 7 | `Dropdown._init_main_panel` | Medium | The `.center` assignment after construction moves nothing (dead code) |
| 8 | `Dropdown._init_main_panel` | Medium | Mutates the caller's `buttons` dict (`pop`) |
| 9 | `Widget.call_action` | Low | Falsy arguments (`0`, `False`, `""`) are silently dropped |
| 10 | `Text.__init__` | Low | Never calls `super().__init__` — inherited geometry would crash |
| 11 | `ClickableIcon` magnify | Low | One GPU texture leaked per hover enter/leave |
| 12 | Misc | Low | Dead code: `Input_box.standin_input`, `Dropdown._scroll` parameter |

---

## 1. BLOCKER — collectibles: texture from disk *per frame* (`Map_renderer.draw_cell`)

```python
if cell.collectible:
    collectible: Icon = Icon(...)   # ← new Icon EVERY frame, for EVERY pacgum
    collectible.display_widget()
```

`Icon.__init__` runs `pr.load_image()` (disk read + PNG decode) →
`image_resize` → `load_texture_from_image` (GPU texture allocation) — and
the texture from the previous frame is never unloaded.

For a typical 21×21 map (~200 collectibles) that is **~200 PNG decodes and
200 GPU texture uploads per frame** (est. 60–200 ms per frame — a slideshow
at 60 fps), leaking ~12,000 textures per minute into VRAM: performance
degrades progressively, then the GPU driver starts swapping, then it dies.
On a 50×50 map it is ~2,500 loads per frame.

**Fix** — build collectible icons once per resize, cache by texture name,
and blit them per frame:

```python
# in __init__ (or on resize):
self.collectible_icons: dict[str, Icon] = {}
for name in self.texture_pack.collectibles_needed:
    icon = Icon(0, 0, self.texture_pack.get_texture(name),
                (self.collectible_size, self.collectible_size), True)
    self.collectible_icons[name] = icon

# in draw_cell:
if cell.collectible:
    icon = self.collectible_icons[cell.collectible.name]
    icon.x = x + (self.cell_size - self.collectible_size) // 2
    icon.y = y + (self.cell_size - self.collectible_size) // 2
    icon.display_widget()
```

## 2. Walls: static content drawn from scratch every frame (`draw_grid`)

`draw_walls` issues up to ~8 `draw_line_ex` calls per cell (walls + corner
strokes). That is roughly **1,500–3,500 Python→C draw calls per frame at
21×21** (est. 3–7 ms of call overhead), and ~10,000+ at 50×50 (est.
20–30 ms — over the 16.7 ms frame budget by itself).

The maze only changes when the window is resized. **Fix**: after each
resize, render the whole grid **once** into an offscreen
`pr.RenderTexture` (`pr.load_render_texture` → draw walls →
`pr.unload_render_texture` on the next resize), then one `draw_texture`
per frame. This removes the entire per-frame wall cost.

## 3. `get_neighbors` rebuilt per cell per frame

`draw_cell` calls `get_neighbors` for every cell on every frame: ~441 (or
2,500) fresh dicts per frame for data that never changes. Compute it once
(first render or per resize) and never touch it again.

## 4. Entity sprites reload from disk on every texture change

The `sprites` cache is the right idea, but whenever the texture *name*
changes (every direction change / frightened flip — ~10 per second), the
`AnimIcon` is re-created: `load_image_anim` from disk + decode + new
texture. **Fix**: cache `AnimIcon`s keyed by texture path and only move
them; load lazily only for a texture never seen before.

## 5. `Dropdown._update_icon` constructs the arrow every frame

A new `ClickableIcon` (PNG read + GPU texture) is created on **every**
`display_widget` call while the dropdown exists, and old textures are never
freed — 60 loads/second. Construct the icon once; swap the image only when
`show` flips (with `unload_texture` for the replaced one).

## 6. BLOCKER — `Input_box` first keystroke doubled + infinite freeze

```python
self.key = pr.get_char_pressed()
while self.key > 0:
    if self.key >= self.char_range[0] and (
            self.key <= self.char_range[1]
            and len(self.input) < self.max_chars):
        self.input += chr(self.key)
    if len(self.input) > 1:                  # ← wrong: key only refreshed
        self.key = pr.get_char_pressed()     #    once input > 1 char
```

Two consequences, both deterministic:

- **The first character typed into an empty box is duplicated.** Press
  `a` on empty input: iteration 1 adds `"a"` (len 1 → no refresh),
  iteration 2 adds `"a"` again → `"aa"`.
- **An out-of-range key on an empty box freezes the GUI forever.**
  `char_range` is `(32, 125)` which excludes `é` (233) — trivial to hit on
  a French keyboard. Pressing `é` as the first character fails the range
  check, the input stays empty, the key is never refreshed → infinite
  loop, window frozen.

**Fix** — refresh unconditionally:

```python
while self.key > 0:
    if (self.key >= self.char_range[0]
            and self.key <= self.char_range[1]
            and len(self.input) < self.max_chars):
        self.input += chr(self.key)
    self.key = pr.get_char_pressed()
```

## 7. `Dropdown._init_main_panel`: the `.center` assignment is dead

`init_buttons` places buttons using the **construction-time** `center`
(default −2), and `Button.posx` uses the fixed position computed then.
Setting `main_panel.center = ...` afterwards moves nothing — the main
label stays centered in the old, narrower width. Either pass the desired
center into the `ButtonPanel` constructor or re-init the buttons after
changing it.

## 8. `Dropdown` mutates the caller's dict

`self.buttons.pop(self.main_label)` deletes the first entry from the dict
the GUI passed in — the caller can never safely reuse it. Copy first:
`self.buttons = dict(buttons)`.

## 9. `Widget.call_action` drops falsy arguments

```python
if isinstance(args, tuple): ...
elif args:          # (callback, 0) → falsy → callback() without its arg!
    self.action[0](args)
```

Should be `elif args is not None:`. Also note (convention, document it):
a tuple argument is always unpacked into positional args.

## 10. `Text` never calls `super().__init__`

`Text.__init__` sets `x`/`y` but never initializes the `Widget` base
(`w`, `h`, `pos`). Nothing breaks today only because `Text` avoids every
inherited property that touches them (`is_in`, `posx`/`posy` would
raise `AttributeError` if ever called on a `Text`). One
`super().__init__(x, y, width, font_size)` makes the hierarchy honest and
future-proof.

## 11. `ClickableIcon` magnify leaks one texture per hover cycle

Each hover enter/leave runs `load_texture_from_image` without freeing
the previous texture. Call `pr.unload_texture(self.texture)` before
replacing it.

## 12. Dead code

- `Input_box.standin_input` is never used.
- `Dropdown._scroll(direction=0)`'s parameter is immediately overwritten
  by `pr.get_mouse_wheel_move()` — use it or drop it.

---

## What is already good (no action needed)

- **Menu views are correctly gated**: widgets are rebuilt only on window
  resize; `Texture_pack` loads every sprite once. Per-frame menu cost is
  negligible.
- **Engine side (measured on `dev`)**: the game loop has ~590× headroom at
  default map size and ~167× at the maximum 50×50; the only tail risk is
  a rare ~10 ms A* burst at max size, invisible at default settings.
- The widget architecture (ABC base, `action` tuple convention,
  `_update_widget` hook) is consistent, and the layout math
  (`calculate_label_spacing`, button areas, relative `-x` positioning)
  all traced correctly.

## Verifying after the fixes

Log `pr.get_frame_time()` once per second from the game view loop:
before the fixes expect tens of milliseconds on the game view (worse
over time as VRAM fills); after fixes 1–4 expect ~1–2 ms per frame,
stable over long sessions.

Suggested order: 1 → 6 (blockers, both small diffs), then 2 → 3 → 5 → 7,
then the rest at leisure.
