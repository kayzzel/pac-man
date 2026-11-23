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
  for the mandatory, the scores are stored in the `highscore_filename` file defined in the config (by default `highscore.json`, shipped next to the executable),
  for the arcade it is stored in the bundled `score.json` of the arcade levels,
  and all of the custom maps scores are located by default in a `.maps/<map_name>/score.json` file created at runtime, with the <map_name> being the name of the collection of maps/levels (for example, `map2` or `map1`).<br><br>

  Each map keeps its own scores in its own file, so that every level or map set has an independent ranking instead of one global board.
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
