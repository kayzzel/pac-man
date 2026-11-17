from .Collectible import Collectible


class Pacgum(Collectible):
    """The small dot filling the corridors, the basic collectible."""

    def __init__(self, x: int, y: int, points: int) -> None:
        """
            Description:
        Create a simple pacgum on a cell.

            Parameters:
        x -> column of the cell it sits on
        y -> row of the cell it sits on
        points -> points awarded when it is eaten
        """
        super().__init__("pacgum", x, y, points)
