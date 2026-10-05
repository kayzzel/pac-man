from .Cell import Cell


class Map:
    def __init__(self) -> None:
        self.cells: list[list[Cell]] = []
        self.collectible_count: int = 0
        self.pacman_spawn: tuple[int, int] = (0, 0)
        self.ghosts_spawn: dict[str, tuple[int, int]] = {
                "BLINKY": (0, 0),
                "PINKY": (0, 0),
                "CLYDE": (0, 0),
                "INKY": (0, 0),
        }
        self.ghosts_scatter: dict[str, tuple[int, int]] = {
                "BLINKY": (0, 0),
                "PINKY": (0, 0),
                "CLYDE": (0, 0),
                "INKY": (0, 0),
        }
