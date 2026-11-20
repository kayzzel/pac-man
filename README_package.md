*This project has been created as part of the 42 curriculum by gabach, ibady.*

# ==== PAC-MAN ====


## Table of contents

  1. [Description](#description)
  2. [Instructions](#instructions)
  3. [Configuration](#configuration)
  4. [Highscore](#highscore)<br><br>



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


  No installation or building is needed, this is the standalone version of the game.<br>

  **Execution**

  To run the game, you just need to extract the archive and execute the provided `pac-man` binary in your terminal (giving the configuration file as argument).<br><br>

  __On Linux / macOS__:
  ```
  chmod +x ./pac-man
  ./pac-man <config_file>
  ```
  <br><br>
  

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

  TO BE FILLED LATER
  <br><br>
