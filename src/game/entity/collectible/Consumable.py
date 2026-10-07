from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...Game import Game

from .Collectible import Collectible
from ....utils.enum_utils import Consumable_type


class Consumable(Collectible):
    def __init__(
                self,
                name: Consumable_type,
                x: int,
                y: int,
                points: int
            ) -> None:
        super().__init__(name, x, y, points)

    def collected(self, game: "Game") -> None:
        super().collected(game)

        game.consumables.append(self)
