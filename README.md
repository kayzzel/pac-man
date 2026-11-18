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

  This project uses `uv` as a dependency manager. To install the required packages (`pyray` and the `mazegenerator` provided), you can simply run:
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
  This command creates a standalone executable bundled with the required assets, configuration file and documentation into 
  a `pac-man.zip` archive that you can find in the `dist/` directory.
