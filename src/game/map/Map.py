from .Cell import Cell


class Map:
    def __init__(self) -> None:
        self.cells: list[list[Cell]] = []
        self.collectible_count: int = 0
        self.spawn: tuple[int, int] = (0, 0)
