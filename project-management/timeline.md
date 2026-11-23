# Project Timeline - Pac-Man

This timeline is reconstructed from the full commit history of the
repository (all branches, 480+ commits between September 8 and
November 23, the last day being the busiest of the whole project)
and is part of the project management evidence.

## The team, as seen by the history

| Contributor | Commits | Role visible in the history |
|---|---|---|
| gabach | 210 | Game engine: config, maze integration, entities, game loop, threading, scores, custom maps, cheats, arcade levels, subject compliance, timeline and README reviews |
| ibady | 272 | GUI: menus, views, widget framework, texture packs, rendering, map editor front-end, packaging, README main writing, pull request merges into dev |

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
| 15. Subject compliance | 10-11 | 21-11 | engine | PR #19 (13-11), PR #26 (21-11) |
| 16. GUI docstrings and polish | 13-11 | 19-11 | gui | PR #20 (18-11) |
| 17. Multi-map custom editor | 17-11 | 17-11 | engine | PR #22 (17-11) |
| 18. Packaging | 18-11 | 23-11 | gui | PR #31 (23-11) |
| 19. Arcade levels | 20-11 | 22-11 | engine | PR #27 (22-11) |
| 20. README and instructions | 16-11 | 23-11 | both | PR #26, #28, #29 (21-11, 23-11) |
| 21. Final integration | 20-11 | 23-11 | both | PR #23, #24, #25, #30 (20-11, 23-11) |

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
- **12-11**: final engine wave of the month - the docstrings pass
  over the whole engine, the lint-strict errors are resolved; the
  GUI fixes double-free errors and cleans App, and the project
  timeline file itself is started from the commit history.
- **13-11**: **PR #19 (custom map launch)** - the error at the start
  of `custom_game` is fixed; the GUI adds the instructions view to
  the main menu, fixes the dropdown clicking, lets the map editor
  remove a collectible by pressing its icon again, and rearranges
  the score display.
- **14-15-11**: the GUI documents its own code - first all the
  widgets (14th), then almost every view (15th).
- **16-11**: both tracks pass `App` type checking into the views;
  the `Custom_view` docstrings are finished; a small animation loop
  is added at the end of a won game so the view does not change
  brutally; the engine attacks the entity "teleporting" bug.
- **17-11**: the multi-map custom editor lands on the engine side
  (`Maps_custom`, several maps in a single game set, kept
  lint-strict clean); the GUI builds `custom_step` so the editor
  runs as several steps; a level indicator is added before the
  3-second countdown between levels, the current keybinds are
  shown in the options menu, and the uneven map size and frozen
  countdown bugs are fixed.
- **18-11**: **PR #20 (features/menu)** merges the whole GUI wave
  into dev. The engine side makes `pac-man.py` able to start the
  app, ships the `config.json` example, creates the mandatory
  score file and registers the mandatory in the score list. The
  GUI restructures the whole view/ folder, moves the assets
  directory, adds pyinstaller to the dependencies and writes the
  first Makefile build command: packaging begins.
- **19-11**: stability day. The App main loop is moved to its own
  function to fix a segfault; the game launch is fixed by passing a
  callable instead of the instantiated Game; the base points are
  re-added in Pacgum and Super_Pacgum; the custom map load
  dropdown, the texture pack change through the pause menu and the
  escape key during the death animation are fixed; the test folder
  is removed from src.

### 20-23 November - the final sprint to the release

- **20-11**: the arcade comes alive on the engine side - the eight
  arcade levels are created (the classic maze, one fruit per
  level, and the glitched final level hiding the key), then wired
  into the Score_view and the map choice menu, moved into src/ and
  given their correct score path; the custom games get a one-hour
  level max time; `highscore.json` is gitignored and the missing
  docstrings are completed. The GUI side changes the colors
  (**PR #24**), fixes the score reading/writing catch errors, the
  player name length and the pacgum size; **PR #23 (features/menu)
  and PR #25 (map name fix)** are merged the same day.
- **21-11**: **PR #26 (subject compliance)** merges the whole
  compliance branch into dev: compliant scores, generator guard,
  custom map score file fix, docstrings everywhere, teleport fix.
- **22-11**: release cleanup - the old Custom_view file is removed,
  the Makefile build includes the game files in the zip, and the
  packaging branch is synced with dev.
- **23-11, the busiest day of the project (34 commits)**: four pull
  requests merged in the same day - **PR #28 (readme)**, **PR #29
  (instructions)**, **PR #30 (map previews)** and **PR #31
  (packaging)**. The README is finished (subject-exact first line,
  both AI usage parts, the game engine part of the implementation
  section, direct reference links, itch.io link), the instructions
  file is refined for the subject, the map choice menu gets its
  creation previews and images, and the packaging command is
  finished with README_package bundled into the zip. The project is
  complete: 30 merged pull requests numbered up to #31, more than
  480 commits.

## Activity profile

- 480+ commits over 77 calendar days (08-09 to 23-11), with
  commits on 57 different days; the median day has 5 commits, the
  busiest days are 23-11 (34, the last one), 05-10 (32) and
  20-11 (29).
- Work runs in weekly to biweekly sprints visible in the PR flow:
  a branch lives on its feature track, then a wave of merges lands
  in dev the same day (22-09, 05-10, 28-10, 06-11), with the
  biggest wave saved for the very last day (four PRs on 23-11).
- The final sprint (13-11 to 23-11) is as dense as the building
  weeks: documentation, packaging, arcade and integration all
  land in eleven days, and the project ends at full speed
  instead of tapering off.
- The history also keeps its scars, which is itself evidence:
  an a-star branch with commits named "wtf", "wft 2" and "I think
  this is the end" that was finally squashed into one clean commit;
  a "kitty won't work ;-;" debug commit while testing the wall
  display; the "pushing again to see if flake8 passes" loop in
  the widget branch.
- Notable blocking points visible in the history: the map renderer
  went through a "fix/map_rendering" branch on 02-11 (textures,
  y flip, image handling) before the game view became playable;
  and on 19-11 a segfault at startup forced the App main loop
  into its own function and the game launch to pass a callable
  instead of the instantiated Game.

## How this timeline maps to the deliverables

- The engine milestones match the merged pull requests: the engine
  is finished for the mandatory game on 17-10 (PR #12), becomes
  threaded on 24-10 (PR #13), persists scores and maps on 28-10
  (PR #14, #15), gains cheats on 06-11 (PR #17), supports several
  custom maps in one game on 17-11 (PR #22) and its arcade levels
  until the patch series merged 22-11 (PR #27).
- The GUI milestones are the widget branch (merged 06-11, PR #16),
  the map editor view (finished 11-11), the whole menu wave merged
  on 18-11 (PR #20) and the map previews of 23-11 (PR #30).
- The 42 requirements are covered by the compliance branch
  (merged 21-11, PR #26), the instructions file (PR #29) and the
  README + packaging pair finalized on the last day (PR #28, #31).
- Everything after 10-11 is compliance and release work:
  instructions, score rules, error handling of the external
  package, docstrings, packaging and documentation.
