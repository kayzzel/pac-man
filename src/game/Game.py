from .GameLoop import GameLoop
from .GameCheats import GameCheats
from .map.Map import Map
from .map.Map_scores import Map_scores
from .map.Map_storing import load_map_from_file
from .entity.Pac_man import Pac_man
from .entity.ghost.Ghost import Ghost
from .entity.ghost.Blinky import Blinky
from .entity.ghost.Pinky import Pinky
from .entity.ghost.Clyde import Clyde
from .entity.ghost.Inky import Inky
from .entity.collectible.Consumable import Consumable
from ..Config import Config
from ..utils.maze_utils import convert_maze_to_map, generate_maze
from ..utils.enum_utils import Game_state, Ghost_state, Pacman_state

from pathlib import Path

import os
import sys
import threading
import contextlib


class Game:
    """A whole game: maps, entities, scores, cheat panel and thread."""

    def __init__(
                self,
                config: Config,
                map_name: str,
                score_file: Path,  # maps_folder/map_name/score.json
            ) -> None:
        """
            Description:
        Create a game for one map: Pac-Man, the four ghosts, the
        scores of the map, the cheat panel and the game loop, in the
        NOT_RUNNING state, without any level in it.

            Parameters:
        config -> the loaded config of the game
        map_name -> the name of the map or mode played
        score_file -> the json file keeping the scores of this game
        """
        self.map: list[Map] = []
        self.map_index: int = 0

        self.scores: Map_scores = Map_scores(map_name, score_file)
        self.config = config

        self.player = Pac_man(config)
        self.ghosts: dict[str, Ghost] = {
                "BLINKY": Blinky(),
                "PINKY": Pinky(),
                "CLYDE": Clyde(),
                "INKY": Inky(),
            }
        self.consumables: list[Consumable] = []

        self.timer: int = 0
        self.__map_finished: bool = False

        self.__thread: threading.Thread | None = None
        self.game_loop = GameLoop(update_game, duration=config.level_max_time)
        self.state: Game_state = Game_state.NOT_RUNNING

        self.cheats: GameCheats = GameCheats(self)

    def stop(self, status: Game_state = Game_state.LOST) -> None:
        """
            Description:
        Put the game in the given state and ask the loop to end. A
        FINISHED_MAP status is also remembered so the next level is
        announced with the right state, even to a GUI that resumed
        too early.

            Parameters:
        status -> the state to give the game
        """
        self.state = status
        if status == Game_state.FINISHED_MAP:
            self.__map_finished = True
        self.game_loop.stop()

    def pause(self, status: Game_state = Game_state.PAUSED) -> None:
        """
            Description:
        Pause the game with the given state: the worker thread parks,
        using no CPU, and the state tells the GUI why (waiting for a
        start, a death or a cleared level animation).

            Parameters:
        status -> the pause state to give the game
        """
        self.state = status
        self.game_loop.pause()

    def resume(self) -> None:
        """
            Description:
        Put the game in the RUNNING state and wake the parked worker
        thread: the timer and the game only move while running.
        """
        self.state = Game_state.RUNNING
        self.game_loop.resume()

    def start(self) -> None:
        """
            Description:
        Play every level in order: reset the clock and the
        positions, park at PAUSED (or FINISHED_MAP right after a
        cleared level) waiting for resume, run the level until it is
        cleared, lost or stopped, then move on to the next one. All
        levels cleared means WON.
        """
        for _ in self.map:

            self.start_position()
            self.game_loop.reset()
            self.timer = self.game_loop.timer

            if self.__map_finished:
                self.__map_finished = False
                self.pause(Game_state.FINISHED_MAP)
            else:
                self.pause(Game_state.PAUSED)
            self.game_loop.run(self)

            if self.state == Game_state.LOST:
                self.stop(Game_state.LOST)
                return

            if self.map_index + 1 != len(self.map):
                self.map_index += 1

        self.stop(Game_state.WON)

    def generate_map(self, width: int, height: int, seed: int = 0) -> Map:
        """
            Description:
        Generate one level with the external A-Maze-ing package and
        build a complete map out of it: walls, pacgums, super
        pacgums in the corners and the spawns. Any failure of the
        package becomes a clean ValueError.

            Parameters:
        width -> width of the level, in cells
        height -> height of the level, in cells
        seed -> seed of the maze, 0 for a random one

            Returns value:
        return the generated map, ready to be played
        """
        if width < 2 or height < 2:
            raise ValueError(f"Invalid map size: {width}x{height}")

        with (
            open(os.devnull, "w") as devnull,
            contextlib.redirect_stdout(devnull),
        ):
            maze: list[list[int]] = generate_maze(width, height, seed)

        try:
            return convert_maze_to_map(maze, self.config)
        except Exception as err:
            raise ValueError(
                    "failed to build the map from the generated "
                    f"maze: {err}"
                ) from err

    def start_position(self) -> None:
        """
            Description:
        Put every entity back in place: Pac-Man on his spawn without
        any power-up, and the four ghosts on their spawns in SCATTER,
        at their normal speed.
        """
        cur_map = self.map[self.map_index]

        self.player.pos_x, self.player.pos_y = cur_map.pacman_spawn

        self.player.is_energized = Pacman_state.NORMAL

        for ghost_name in ["BLINKY", "PINKY", "CLYDE", "INKY"]:
            ghost = self.ghosts[ghost_name]

            ghost.spawn_point = cur_map.ghosts_spawn[ghost_name]
            ghost.scatter_point = cur_map.ghosts_scatter[ghost_name]

            ghost.pos_x, ghost.pos_y = ghost.spawn_point

            ghost.real_path_finding = cur_map.real_path_finding
            if ghost.state == Ghost_state.EATEN:
                ghost.speed /= 2
            ghost.state = Ghost_state.SCATTER

    def start_async(self) -> None:
        """
            Description:
        Start playing the game in a daemon worker thread and come
        back immediately: the GUI keeps the hand and drives the
        pauses with resume().
        """
        if self.__thread is not None and self.__thread.is_alive():
            return
        self.__thread = threading.Thread(target=self.__run_safe, daemon=True)
        self.__thread.start()

    def __run_safe(self) -> None:
        """
            Description:
        Body of the worker thread: play the game, and turn any
        unexpected exception into a clean ERROR state instead of a
        frozen game.
        """
        try:
            self.start()
        except Exception as err:
            print(err, file=sys.stderr)
            self.state = Game_state.ERROR
            self.game_loop.stop()

    def join(self, timeout: float = 2.0) -> None:
        """
            Description:
        Wait politely for the worker thread to end, at most the
        given timeout, typically before leaving the app.

            Parameters:
        timeout -> maximum seconds to wait
        """
        if self.__thread is not None:
            self.__thread.join(timeout)


def calculate_collision(game: Game) -> bool:
    """
        Description:
    Handle what happens on Pac-Man's tile: eat the collectible if
    there, then check the ghosts standing on the same tile: an
    invincible or energized Pac-Man eats them, anything else costs
    him a life.

        Parameters:
    game -> the running game

        Returns value:
    return True when the collision cost Pac-Man a life
    """
    pacman = game.player

    x = int(pacman.pos_x)
    y = int(pacman.pos_y)

    cell = game.map[game.map_index].cells[y][x]

    if (cell.collectible):
        cell.collectible.collected(game)

    for ghost in game.ghosts.values():
        if (
                ghost.state == Ghost_state.EATEN
                or (x, y) != (int(ghost.pos_x), int(ghost.pos_y))
                ):
            continue

        if (
                game.cheats.is_invincible or
                (
                    pacman.is_energized != Pacman_state.NORMAL and
                    not ghost.eaten_this_power
                )
        ):
            ghost.set_eaten()
            pacman.score += game.config.point_per_ghost

        else:
            pacman.nb_lives -= 1
            return True

    return False


def update_game(game: Game) -> None:
    """
        Description:
    Advance the whole game by one tick: refresh the visible timer,
    move Pac-Man and the four ghosts, then handle the collisions:
    a lost life respawns everything and parks the game in DIED, no
    life left ends the game in LOST, and a fully eaten map ends the
    level in FINISHED_MAP.

        Parameters:
    game -> the running game
    """
    game.timer = game.game_loop.timer

    pacman = game.player
    cur_map = game.map[game.map_index]

    pacman.update(
            cur_map.cells[int(pacman.pos_y)][int(pacman.pos_x)],
            int(game.game_loop.elapsed_time),
            game.cheats.is_clipping,
            (len(cur_map.cells[0]), len(cur_map.cells))
        )

    for ghost in game.ghosts.values():
        ghost.update(
                {"pacman": pacman, "blinky": game.ghosts["BLINKY"]},
                cur_map.cells,
                int(game.game_loop.elapsed_time)
             )

    if calculate_collision(game):
        if pacman.nb_lives == 0:
            game.stop(Game_state.LOST)
            return

        game.start_position()
        game.pause(Game_state.DIED)

    if cur_map.collectible_count <= 0:
        game.stop(Game_state.FINISHED_MAP)


def mandatory_game(config: Config) -> Game | None:
    """
        Description:
    Build the mandatory game on the levels generated by the
    A-Maze-ing package (the first one from the fixed seed, the
    others random) and start playing it in its own thread.

        Parameters:
    config -> the loaded config of the game

        Returns value:
    return the running game, or None with a clear message printed
    when the generator fails
    """
    game = Game(config, "Mandatory", Path(config.highscore_filename))
    first = True

    width, height = config.levels_dimensions

    try:
        for _ in range(config.nb_level):
            if first:
                game.map.append(
                        game.generate_map(width, height, config.seed)
                    )
                first = False
            else:
                game.map.append(game.generate_map(width, height))
    except ValueError as err:
        print(err, file=sys.stderr)
        return None

    game.start_async()

    return game


def custom_game(
            map_name: str,
            map_directory: Path,
            config: Config | None = None
        ) -> Game | None:
    """
        Description:
    Load the stored custom map called map_name and start playing
    it, in its own thread, on the folder's own scores.

        Parameters:
    map_name -> name of the map, and of its folder
    map_directory -> the folder holding every custom map
    config -> the config of the game, default values when None

        Returns value:
    return the running game, or None when the map does not exist,
    is not well formatted, or its name tries to escape
    map_directory
    """
    if config is None:
        config = Config()

    if map_name != Path(map_name).name:
        return None

    map_file = map_directory / map_name / "map.json"

    try:
        new_map = load_map_from_file(str(map_file))
    except ValueError:
        return None

    game = Game(config, map_name, map_file)
    game.map.append(new_map)
    game.start_async()

    return game
