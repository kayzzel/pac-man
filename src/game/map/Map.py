from .Cell import Cell


class Map:
    """A level: its grid of cells, its spawns and its collectibles."""

    def __init__(self) -> None:
        """
            Description:
        Create an empty map: no cells, no collectible and every spawn
        at the origin, ready to be filled by a builder.
        """
        self.name: str = ""
        self.cells: list[list[Cell]] = []
        self.real_path_finding = False
        self.collectible_count: int = 0
        self.pacman_spawn: tuple[float, float] = (0, 0)
        self.ghosts_spawn: dict[str, tuple[float, float]] = {
                "BLINKY": (0, 0),
                "PINKY": (0, 0),
                "CLYDE": (0, 0),
                "INKY": (0, 0),
        }
        self.ghosts_scatter: dict[str, tuple[float, float]] = {
                "BLINKY": (0, 0),
                "PINKY": (0, 0),
                "CLYDE": (0, 0),
                "INKY": (0, 0),
        }
