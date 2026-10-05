from .GameLoop import GameLoop
from .map.Map import Map
from .map.Map_scores import Map_scores
from .entity.Pac_man import Pac_man
from .entity.ghost.Ghost import Ghost, Ghost_state
from .entity.collectible.Consumable import Consumable
from ..Config import Config
from ..utils.maze_utils import convert_maze_to_map

from mazegenerator import MazeGenerator

import os
import contextlib


class Game:
    def __init__(self, config: Config) -> None:
        self.map: list[Map] = []
        self.map_index: int = 0
        self.scores: Map_scores = Map_scores()
        self.config = config
        self.player = Pac_man(config)
        self.ghosts: dict[str, Ghost] = {}
        self.timer: int = 0
        self.is_paused = False
        self.game_loop = GameLoop(update_game)
        self.consumables: list[Consumable] = []

    def pause(self) -> None:
        self.is_paused = True
        self.game_loop.pause()

    def resume(self) -> None:
        self.is_paused = False
        self.game_loop.resume()

    def start(self) -> None:
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


def update_game(game: Game, dt: float) -> None:
    ...


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

        if pacman.is_energized:
            ghost.set_eaten()
            pacman.score += game.config.point_per_ghost

        else:
            pacman.nb_lives -= 1
            return True

    return False
