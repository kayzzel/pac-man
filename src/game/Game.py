from .map.Map import Map
from .map.Map_scores import Map_scores
from .entity.Pac_man import Pac_man
from .entity.ghost.Ghost import Ghost
from ..Config import Config
from ..utils.maze_utils import convert_maze_to_map

from mazegenerator import MazeGenerator

import os
import contextlib


class Game:
    def __init__(self, config: Config) -> None:
        self.map: list[Map] = []
        self.scores: Map_scores = Map_scores()
        self.config = config
        self.player = Pac_man(config)
        self.ghosts: dict[str, Ghost] = {}
        self.timer: int = 0
        self.is_paused = False

    def pause(self) -> None:
        self.is_paused = True

    def resume(self) -> None:
        self.is_paused = False

    def game_loop(self) -> None:
        ...

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
