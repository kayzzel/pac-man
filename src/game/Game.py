from .map.Map import Map
from ..Config import Config
from .entity.Pac_man import Pac_man
from .entity.ghost.Ghost import Ghost


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
