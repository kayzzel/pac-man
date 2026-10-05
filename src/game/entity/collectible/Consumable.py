from .Collectible import Collectible
from ...Game import Game

from enum import Enum


class Consumable_type(Enum):
    CHERRY = "cherry"
    STRAWBERRY = "strawberry"
    ORANGE = "orange"
    APPLE = "apple"
    MELON = "melon"
    GALAXIAN = "galaxian"
    BELL = "bell"
    KEY = "key"


class Consumable(Collectible):
    def __init__(
                self,
                name: Consumable_type,
                x: int,
                y: int,
                points: int
            ) -> None:
        super().__init__(x, y, points)
        self.name = name

    def collected(self, game: Game) -> None:
        super().collected(game)

        game.consumables.append(self)
