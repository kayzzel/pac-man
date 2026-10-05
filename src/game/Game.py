from .GameLoop import GameLoop
from .map.Map import Map
from .map.Map_scores import Map_scores
from .entity.Pac_man import Pac_man
from .entity.ghost.Ghost import Ghost, Ghost_state
from .entity.ghost.Blinky import Blinky
from .entity.ghost.Pinky import Pinky
from .entity.ghost.Clyde import Clyde
from .entity.ghost.Inky import Inky
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
        self.ghosts: dict[str, Ghost] = {
                "BLINKY": Blinky(),
                "PINKY": Pinky(),
                "CLYDE": Clyde(),
                "INKY": Inky(),
            }
        self.consumables: list[Consumable] = []

        self.timer: int = 0

        self.game_loop = GameLoop(update_game)
        self.is_paused = False
        self.is_won: int = 0  # -1 lost / 0 not finished / 1 won

    def stop(self, status: int) -> None:
        self.is_won = status
        self.game_loop.stop()

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

    def start_position(self) -> None:
        cur_map = self.map[self.map_index]

        self.player.pos_x, self.player.pos_y = (
                cur_map.pacman_spawn
            )

        self.player.is_energized = False

        for ghost_name in ["BLINKY", "PINKY", "CLYDE", "INKY"]:
            ghost = self.ghosts[ghost_name]

            ghost.spawn_point = cur_map.ghosts_spawn[ghost_name]
            ghost.scatter_point = cur_map.ghosts_scatter[ghost_name]

            ghost.pos_x, ghost.pos_y = ghost.spawn_point

            ghost.state = Ghost_state.SCATTER


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
                cur_map.cells[int(ghost.pos_y)][int(ghost.pos_x)],
                int(game.game_loop.elapsed_time)
             )

    if calculate_collision(game):
        if pacman.nb_lives == 0:
            game.stop(-1)
            return

        game.start_position()
        game.pause()
