from ...Config import Config
from .collectible.Collectible import Collectible


class Pac_man:
    def __init__(self, config: Config) -> None:
        self.score = 0
        self.nb_lives = config.lives
        self.pos_x: float = 0.0
        self.pos_y: float = 0.0
        self.direction = "N"
        self.collectible: list[None | Collectible] = []
