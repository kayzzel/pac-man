from .Entity import Entity
from ...Config import Config
from .collectible.Collectible import Collectible


class Pac_man(Entity):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.score = 0
        self.nb_lives = config.lives
        self.collectible: list[None | Collectible] = []
