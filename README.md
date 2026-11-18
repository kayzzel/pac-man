*This project was created as a part of the 42 curriculum by gabach, ibady.*


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

  The goal of this project was to recreate the Pac-Man game in Python, using an external maze generator package provided by the 42 project __A-Maze-Ing__. We decided to implement three different modes: mandatory, arcade and custom. The mandatory mode respects the game mechanics of the original game (ghosts patterns), but uses maps from the maze generator, makes the ghosts spawn at the four corners, and does not include collectibles other than pacgums and super pacgums. The arcade mode, however, is a copy of the original game, with the same maps/levels and collectibles (apple, melon, galaxian, etc). And then the custom mode allows the player to create their own maps/levels. The whole game display was made using tbe __pyray__ library (wrapped from raylib in C).

### Instructions


  ____

  **Installation**

  This project uses `uv` as a dependency manager. To install the required packages (`pyray` and the `mazegenerator`   provided), you can simply run:
  ```
  make
  ```
  Or you can directly use `uv` to sync the dependencies:
  ```
  uv sync
  ```

  **Execution**

  To execute and run the game, you can use the following command at the root of the repository:
  ```
  make run [ARGS="config_file"]
  ```
  Or again, you can directly use `uv` to run the program:
  ```
  uv run python pac-man.py <config_file>
  ```

  **Build**

  To package and create an executable of the game, you can run:
  ```
  make build
  ```
  This command creates a standalone executable bundled with the required assets, configuration file and documentation that    you can find in the `dist/` directory.

### Configuration


  ____

  The specifications of the game rely on a JSON configuration file (by default, `config.json`), which is checked and validated through Pydantic models to make sure the game is not given invalid data.<br>

  **Structure of the file and default values:**

  + `score_file` (string) : The path to the file in which are stored the scores for the mandatory maps (default=`.maps/mandatory/score.json`)<br>
  + `life` (integer) : The initial number of lives for the player (default=`3`)<br>
  + `width` (integer) : The width (number of columns) of the generated maze for mandatory maps (default=`15`)<br>
  + `height` (integer) : The height (number of rows) of the generated maze for mandatory maps (default=`15`)<br>
  + `seed` (integer) : The random seed for the first maze generation (first level)<br>
  + `time` (integer) : The time limit in seconds to complete a level (default=`120`)<br>
  + `pacgum_points` (integer) : The number of points awarded to the player when collecting a pacgum (default=`10`)<br>
  + `super_pacgum_points` (integer) : The number of points awarded to the player when collecting a super pacgum (default=`50`)<br>
  + `ghost_points` (integer) : The number of points awarded to the player when eating a ghost (default=`200`)<br>

  In case of missing or invalid keys, the default values are adopted. Unknown keys are ignored.<br><br>

### Highscore


  ____

  The highscore system allows the player to save their scores for the different maps by storing them in JSON files,
  all located by default in a `.maps/<map_name>/score.json` file, with the <map_name> being the name of the collection of maps/levels (for example, `mandatory` or `arcade`).<br>

  **How the scores are stored:**

  TO BE FILLED BY GAUTHIER

### Maze Generation


  ____

  For the maze generation of the mandatory levels, we used the `mazegenerator` package provided, from the `A-Maze-Ing` 42 project.
  TO BE FILLED BY GAUTHIER


### Implementation


  ____



### General Software Architecture


  ____


### Project Management


  ____


### Resources


  ____

  **Links:**

  + Pyray documentation
  + Raylib cheatsheet
  + Raylib examples

  **AI Usage:**

  TO BE FILLED BY GAUTHIER
