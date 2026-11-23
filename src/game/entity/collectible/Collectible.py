from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...Game import Game

from abc import ABC


class Collectible(ABC):
    """Base of everything Pac-Man can eat on a cell."""

    def __init__(
                self,
                name: str,
                x: int,
                y: int,
                points: int
            ) -> None:
        """
            Description:
        Create a collectible on a cell, worth at least 0 point: a
        negative value is clamped to 0.

            Parameters:
        name -> name of the collectible, used to pick its texture
        x -> column of the cell it sits on
        y -> row of the cell it sits on
        points -> points awarded when it is eaten
        """
        self.name = name
        self.pos_x: int = x
        self.pos_y: int = y
        if points < 0:
            self.points = 0
        else:
            self.points = points

    def collected(self, game: "Game") -> None:
        """
            Description:
        Apply the effects of eating this collectible: award its points,
        take it off its cell and update the remaining collectibles
        count of the current map.

            Parameters:
        game -> the running game
        """
        game.player.score += self.points
        current_map = game.map[game.map_index]
        current_map.collectible_count -= 1
        current_map.cells[self.pos_y][self.pos_x].collectible = None
