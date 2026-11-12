from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...Game import Game

from .Collectible import Collectible
from ....utils.enum_utils import Consumable_type


class Consumable(Collectible):
    """A bonus fruit, kept in the game once collected."""

    def __init__(
                self,
                name: Consumable_type,
                x: int,
                y: int,
                points: int
            ) -> None:
        """
            Description:
        Create a bonus fruit on a cell, identified by its type.

            Parameters:
        name -> the kind of fruit, a Consumable_type value
        x -> column of the cell it sits on
        y -> row of the cell it sits on
        points -> points awarded when it is eaten
        """
        super().__init__(name, x, y, points)

    def collected(self, game: "Game") -> None:
        """
            Description:
        Eat the fruit and add it to the list of the consumables the
        player already collected.

            Parameters:
        game -> the running game
        """
        super().collected(game)

        game.consumables.append(self)
