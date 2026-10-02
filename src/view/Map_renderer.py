import pyray as pr
from ..game.map.Cell import Cell


class Map_renderer:

    def __init__(self, grid: list[list[Cell]]) -> None:

        self.grid: list[list[Cell]] = grid

    def draw_cell(self, cell: Cell) -> None:

        ...

    def draw_walls(self, cell: Cell) -> None:

        ...

    def draw_grid(self) -> None:

        for row in self.grid:

            for cell in row:

                self.draw_cell(cell)
