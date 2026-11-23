*This project has been created as part of the 42 curriculum by gabach, ibady.*


# ==== PAC-MAN ====


## Table of contents

  1. [Description](#description)
  2. [Instructions](#instructions)
  3. [Configuration](#configuration)
  4. [Highscore](#highscore)
  5. [Maze Generation](#maze-generation)
  6. [Implementation](#implementation)
  7. [General Software Architecture](#general-software-architecture)
  8. [Project Management](#project-management)
  9. [Resources](#resources)<br><br>



### Description


  ____


  The goal of this project was to recreate the Pac-Man game in Python, using an external maze generator package provided by the 42 project __A-Maze-Ing__.<br><br>
  We decided to implement three different modes: __mandatory__, __arcade__ and __custom__.<br><br>
  The mandatory mode respects the game mechanics of the original game (ghosts patterns), but uses maps from the maze generator, makes the ghosts spawn at the four corners, and does not include collectibles other than pacgums and super pacgums.<br><br>
  The arcade mode, however, is a copy of the original game, with the same maps/levels and collectibles (apple, melon, galaxian, etc).<br><br>
  And then the custom mode allows the player to create their own maps/levels.<br><br>
  The whole game display was made using the `pyray` library (wrapped from raylib in C).<br><br>

### Instructions


  ____


  **Installation**

  This project uses `uv` as a dependency manager. To install the required packages (`pyray`, `pydantic`, and the `mazegenerator` provided), you can simply run:
  ```
  make
  ```
  Or you can directly use `uv` to sync the dependencies:
  ```
  uv sync
  ```
  <br>

  **Execution**

  To execute and run the game, you can use the following command at the root of the repository:
  ```
  make run [ARGS="config_file"]
  ```
  Or again, you can directly use `uv` to run the program:
  ```
  uv run python pac-man.py <config_file>
  ```
  <br>

  **Build**

  To package and create an executable of the game, you can run:
  ```
  make build
  ```
  This command creates a standalone executable bundled with the required assets, configuration file and documentation into a `pacman.zip` that you can find in the `dist/` directory.<br><br>

### Configuration


  ____
  

  The specifications of the game rely on a JSON configuration file (by default, `config.json`), which is checked and validated through Pydantic models to make sure the game is not given invalid data.<br>

  **Structure of the file and default values:**

  + `highscore_filename` (string) : The path to the file in which are stored the top-10 scores of the mandatory game (default=`highscore.json`)<br>
  + `nb_level` (integer) : The number of levels in the mandatory game (default=`10`, minimum 10)<br>
  + `levels_dimensions` (array of two integers) : The size `[width, height]` in cells of each generated level for the mandatory game, each dimension must be between 10 and 50 (default=`[15, 15]`)<br>
  + `lives` (integer) : The initial number of lives for the player (default=`3`, minimum 1)<br>
  + `point_per_pacgum` (integer) : The number of points awarded to the player when collecting a pacgum (default=`10`, minimum 0)<br>
  + `point_per_super_pacgum` (integer) : The number of points awarded to the player when collecting a super pacgum (default=`50`, minimum 0)<br>
  + `point_per_ghost` (integer) : The number of points awarded to the player when eating a ghost (default=`200`, minimum 0)<br>
  + `seed` (integer) : The random seed for the first level's maze generation, the following levels are generated randomly, so it only defines the first level (default=`42`)<br>
  + `level_max_time` (integer) : The time limit in seconds to complete a level, the time spent paused is not counted (default=`90`)<br>

  In case of missing or invalid keys, the default values are adopted. Unknown keys are ignored.<br><br>

### Highscore


  ____


  The highscore system allows the player to save their scores for the different maps by storing them in JSON files:<br>
  for the mandatory, the scores are stored in the `highscore_filename` file defined in the config (by default `highscore.json` at the root of the repository),
  for the arcade it is stored in `src/arcade/arcade/score.json`,
  and all of the custom maps scores are located by default in a `.maps/<map_name>/score.json` file, with the <map_name> being the name of the collection of maps/levels (for example, `map2` or `map1`).<br><br>

  Each map keeps its own scores in its own file, so that every level or map set has an independent ranking instead of one global board.
  The files are JSON so that they stay human-readable and easy to check or edit by hand.
  Only the ten best scores are kept per map: when a game ends, the score is added to the file only if it belongs to these top-10 scores, and the lowest score is dropped when the file already holds ten of them.<br>

  **How the scores are stored:**
  ``` json
  [
    {
        "name": {player-name},
        "score": {player-score}
    },
    ...
  ]
  ```
  with the scores sorted from the best to the lowest one.<br>
  <br><br>

### Maze Generation


  ____
  

  For the maze generation of the mandatory levels, we used the `mazegenerator` package provided, from the `A-Maze-Ing` 42 project.<br>
  After the generation of the maze, we created a function to convert it into a map with everything needed. The walls were all converted into cells and put collectibles in them (pacgum and super-pacgum), we set pacman spawn (the cells nearest to the center of the maze that is a possible position so not inside the 42 and not in a full cell), and set the ghosts position and scatter points into the corners

  <br><br>


### Implementation


  ____
  

  As required by the 42 subject for this project, it was built entirely in Python.<br><br>
  The UI interface used `pyray` as the graphic library to make an easy 2D rendering system with `views`, the main `App` cycling through them. The views use `widgets` built from scratch using basic `pyray` functions, for more complex display options.<br>
  There are 10 views (not including the abstract parent class `View`). From the `Main_menu`, the game provides in-game instructions, options of configuration (font, texture pack, keybinds, etc.), and a display of the best scores as well. When the player clicks on "start game", there is a menu to choose the mode, and then either a new game starts, or if you chose the custom mode you can go through the step-by-step process of creating your own maps.<br><br>

### General Software Architecture


  ____


  At the root of the repository, the Makefile, README.md, `pac-man.py` as well as the default `config.json` are present. There's also an `assets` folder containing all the sprites/icons.<br>
  And then all of the code Python files are found inside the `src` folder. At the root of `src` we put the main `App` class and the `Config` class, otherwise we structured the files into four subfolders: `arcade`, `display`, `game` and `utils`.<br>
  The `arcade` folder contains the data of the arcade mode: the eight arcade levels (`map.json` to `map_7.json`, the last one being the glitched level holding the key) and their `score.json`.<br>
  The `display` folder contains everything display-related, such as the `views`, the `widgets`, and also the `Texture_pack` class.<br>
  The `game` folder contains everything game core-related, such as the `map` classes (`Map`, `Cell`, `Map_custom`, etc.), the `game` classes (`Game`, `GameLoop`, etc.) and of course the entity classes (`Entity`, `Pac_man`, `Ghost`, `Collectible`, etc.).<br>
  And then the `utils` folder contains all the helper functions and enums.<br><br>

  **`src` tree architecture:**
  ```
    src
  ├── __init__.py
  ├── App.py
  ├── Config.py
  ├── arcade
  │   └── arcade
  │       ├── map.json
  │       ├── map_1.json
  │       ├── map_2.json
  │       ├── map_3.json
  │       ├── map_4.json
  │       ├── map_5.json
  │       ├── map_6.json
  │       ├── map_7.json
  │       └── score.json
  ├── display
  │   ├── __init__.py
  │   ├── Texture_pack.py
  │   ├── views
  │   │   ├── __init__.py
  │   │   ├── custom_view
  │   │   │   ├── Custom_step.py
  │   │   │   ├── Custom_view.py
  │   │   │   ├── __init__.py
  │   │   │   ├── Step_five.py
  │   │   │   ├── Step_four.py
  │   │   │   ├── Step_one.py
  │   │   │   ├── Step_seven.py
  │   │   │   ├── Step_six.py
  │   │   │   ├── Step_three.py
  │   │   │   ├── Step_two.py
  │   │   │   └── Step_zero.py
  │   │   ├── Endgame_view.py
  │   │   ├── Game_view.py
  │   │   ├── Instructions_view.py
  │   │   ├── Main_menu.py
  │   │   ├── Map_choice_menu.py
  │   │   ├── Options_menu.py
  │   │   ├── Pause_menu.py
  │   │   ├── renderer
  │   │   │   └── Map_renderer.py
  │   │   ├── Save_score_view.py
  │   │   ├── Scores_view.py
  │   │   └── View.py
  │   └── widgets
  │       ├── Button.py
  │       ├── Dropdown.py
  │       ├── Icon.py
  │       ├── __init__.py
  │       ├── Input_box.py
  │       ├── Panel.py
  │       ├── Text.py
  │       └── Widget.py
  ├── game
  │   ├── __init__.py
  │   ├── entity
  │   │   ├── __init__.py
  │   │   ├── collectible
  │   │   │   ├── __init__.py
  │   │   │   ├── Collectible.py
  │   │   │   ├── Consumable.py
  │   │   │   ├── Pacgum.py
  │   │   │   └── Super_Pacgum.py
  │   │   ├── Entity.py
  │   │   ├── ghost
  │   │   │   ├── __init__.py
  │   │   │   ├── Blinky.py
  │   │   │   ├── Clyde.py
  │   │   │   ├── Ghost.py
  │   │   │   ├── Inky.py
  │   │   │   └── Pinky.py
  │   │   └── Pac_man.py
  │   ├── GameCheats.py
  │   ├── GameLoop.py
  │   ├── Game.py
  │   └── map
  │       ├── __init__.py
  │       ├── Cell.py
  │       ├── Map_custom.py
  │       ├── Map.py
  │       ├── Map_scores.py
  │       └── Map_storing.py
  └── utils
      ├── __init__.py
      ├── enum_utils.py
      ├── json_utils.py
      ├── maze_utils.py
      └── path_utils.py
  ```
  <br><br>

### Project Management


  ____


  At the beginning of the project, we put together a roadmap detailing every single class/function to implement, as well as basic display ideas. We also wrote the prototypes of every class that we would both use, ensuring that our code would not clash at any point.<br>
  Then we divided the two main aspects of the project between us: __gabach__ took care of the game engine and entities, and __ibady__ did the UI interface (display) part. A more detailed reconstruction of the project timeline can be found in the dedicated [project-management/](project-management/) directory of the repository (see [project-management/timeline.md](project-management/timeline.md)).<br>
  We implemented git rules that made it impossible to merge our branches directly with dev or main, to avoid having to clean up messes on the dev branch later. Instead, we had to make Pull Requests to merge a specific branch into dev: this branch had to pass __lint__ checks and then the merge had to be approved by the other person.<br><br>
  When we had questions/points/issues to address with the other, we either discussed them on the campus, or we called/messaged via Discord.
  We didn't really have any big interfering code issues while progressing because our parts were almost completely isolated from one another, and even when we had stuff to modify in the other's part, it was usually resolved very easily.<br>
  Overall, the communication was fluid and the project went smoothly.<br><br>
 
### Resources


  ____


  **Links:**

  + [Pyray documentation](https://electronstudio.github.io/raylib-python-cffi/pyray.html)<br>
  + [Raylib cheatsheet](https://www.raylib.com/cheatsheet/cheatsheet.html)<br>
  + [Raylib examples](https://www.raylib.com/examples.html)<br>
  + [Free pixel art editor online used to make the sprites](https://www.piskelapp.com/)<br><br>

  **AI Usage:**

  For the display part, AI was only used two or three times when stuck for too long on an issue and not managing to find the root of the problem (since it sometimes came from the graphic library itself, and `pyray` being a wrapper of a library originally written in C, the behavior of some functions could change).<br><br>
  For the game engine part, I principally used the AI for documentation on python usage and tests until the display was up for tests. I also used it on the docstrings
