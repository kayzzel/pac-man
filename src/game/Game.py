from .GameLoop import GameLoop
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
from ..utils.maze_utils import convert_maze_to_map
from ..utils.enum_utils import Game_state, Ghost_state

from mazegenerator import MazeGenerator
from pathlib import Path

import os
import sys
import threading
import contextlib


class Game:
    def __init__(
                self,
                config: Config,
                map_name: str,
                score_file: Path,  # maps_folder/map_name/score.json
            ) -> None:
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

    def stop(self, status: Game_state = Game_state.LOST) -> None:
        self.state = status
        if status == Game_state.FINISHED_MAP:
            self.__map_finished = True
        self.game_loop.stop()

    def pause(self, status: Game_state = Game_state.PAUSED) -> None:
        self.state = status
        self.game_loop.pause()

    def resume(self) -> None:
        self.state = Game_state.RUNNING
        self.game_loop.resume()

    def start(self) -> None:

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
        if width < 2 or height < 2:
            raise ValueError(f"Invalid map size: {width}x{height}")

        with (
            open(os.devnull, "w") as devnull,
            contextlib.redirect_stdout(devnull),
        ):
            generator: MazeGenerator = MazeGenerator(
                    (width, height), False, seed=seed
                )

            new_map = convert_maze_to_map(generator.maze, self.config)

        return new_map

    def start_position(self) -> None:
        cur_map = self.map[self.map_index]

        self.player.pos_x, self.player.pos_y = cur_map.pacman_spawn

        self.player.is_energized = False

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
        if self.__thread is not None and self.__thread.is_alive():
            return
        self.__thread = threading.Thread(target=self.__run_safe, daemon=True)
        self.__thread.start()

    def __run_safe(self) -> None:
        try:
            self.start()
        except Exception as err:
            print(err, file=sys.stderr)
            self.state = Game_state.ERROR
            self.game_loop.stop()

    def join(self, timeout: float = 2.0) -> None:
        if self.__thread is not None:
            self.__thread.join(timeout)


def calculate_collision(game: Game) -> bool:
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

        if pacman.is_energized and not ghost.eaten_this_power:
            ghost.set_eaten()
            pacman.score += game.config.point_per_ghost

        else:
            pacman.nb_lives -= 1
            return True

    return False


def update_game(game: Game) -> None:
    game.timer = game.game_loop.timer

    pacman = game.player
    cur_map = game.map[game.map_index]

    pacman.update(
            cur_map.cells[int(pacman.pos_y)][int(pacman.pos_x)],
            int(game.game_loop.elapsed_time)
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


def mandatory_game(config: Config) -> Game:
    game = Game(config, "Mandatory", Path(config.highscore_filename))
    first = True

    width, height = config.levels_dimensions

    for _ in range(config.nb_level):
        if first:
            game.map.append(game.generate_map(width, height, config.seed))
            first = False
        else:
            game.map.append(game.generate_map(width, height))

    game.start_async()

    return game


def custom_game(
            map_name: str,
            map_directory: Path,
            config: Config | None = None
        ) -> Game | None:
    """Start an async game on the stored map called map_name.

    Returns the running Game, or None when the map does not exist,
    is not well formatted, or its name tries to escape map_directory.
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
