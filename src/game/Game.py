from .map.Map import Map
from .entity.Pac_man import Pac_man
from .entity.ghost.Ghost import Ghost
from ..Config import Config
from ..utils.maze_utils import convert_maze_to_map

from mazegenerator import MazeGenerator


class Game:
    def __init__(self, config: Config) -> None:
        self.map: list[Map] = []
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

    def generate_map(self, widht: int, height: int, seed: int = 0) -> Map:
        generator: MazeGenerator = MazeGenerator(
                    (widht, height), False
                )

        generator.generate(seed)

        return convert_maze_to_map(generator.maze, self.config)
