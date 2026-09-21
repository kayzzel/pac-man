from .map.Map import Map
from .entity.Pac_man import Pac_man
from .entity.ghost.Ghost import Ghost
from ..Config import Config
from ..utils.maze_utils import convert_maze_to_map

from mazegenerator import MazeGenerator


class Game:
    def __init__(self, config: Config) -> None:
        self.map = Map()
        self.config = config
        self.player = Pac_man(config)
        self.ghosts: dict[str, Ghost] = {}
        self.timer: int = 0
        self.is_paused = False

    def pause(self) -> None:
        ...

    def resume(self) -> None:
        ...

    def game_loop(self) -> None:
        ...

    def generate_map(self, widht: int, height: int, seed: int = 0):
        generator: MazeGenerator = MazeGenerator(
                    (widht, height), False
                )

        generator.generate(seed)

        self.map = convert_maze_to_map(generator.maze)
