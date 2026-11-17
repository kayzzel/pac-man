from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...Game import Game

from .Collectible import Collectible


class Super_Pacgum(Collectible):
    """The big dot giving the power-up that makes ghosts edible."""

    def __init__(self, x: int, y: int, points: int) -> None:
        """
            Description:
        Create a super pacgum on a cell.

            Parameters:
        x -> column of the cell it sits on
        y -> row of the cell it sits on
        points -> points awarded when it is eaten
        """
        super().__init__("super_pacgum", x, y, points)

    def collected(self, game: "Game") -> None:
        """
            Description:
        Eat the super pacgum: award its points, start the power-up at
        the current time, and make every ghost edible again, even the
        ones already eaten during the previous power-up.

            Parameters:
        game -> the running game
        """
        super().collected(game)

        game.player.set_energized(int(game.game_loop.elapsed_time))

        # A new power-up makes every ghost edible again
        for ghost in game.ghosts.values():
            ghost.eaten_this_power = False
