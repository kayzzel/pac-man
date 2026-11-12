from ..entity.collectible.Collectible import Collectible


class Cell:
    """One tile of a map: its walls, its collectible and its position."""

    def __init__(self, pos_x: int, pos_y: int) -> None:
        """
            Description:
        Create an open cell (no walls) holding no collectible, at the
        given position in the grid.

            Parameters:
        pos_x -> column of the cell in the grid
        pos_y -> row of the cell in the grid
        """
        self.pos_x: int = pos_x
        self.pos_y: int = pos_y
        self.collectible: Collectible | None = None
        self.walls: dict[str, bool] = {
                "N": False,
                "S": False,
                "E": False,
                "W": False,
        }
        self.special: bool = False
