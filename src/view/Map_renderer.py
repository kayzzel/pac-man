import pyray as pr
from ..game.map.Cell import Cell


class Map_renderer:

    def __init__(
        self,
        grid: list[list[Cell]],
        map_coor: tuple[int, int],
        cell_size: int
    ) -> None:

        self.grid: list[list[Cell]] = grid
        self.map_x, self.map_y = map_coor
        self.cell_size: int = cell_size
        self.line_thickness: int = 2
        self.cell_padding: int = cell_size // 6 + self.line_thickness

    def draw_walls(self, cell: Cell, x: int, y: int) -> None:

        end_x: int = x + self.cell_size
        end_y: int = y + self.cell_size

        if cell.walls["north"]:

            sx: int = x + self.cell_padding
            sy: int = y + self.cell_padding - self.line_thickness
            ex: int = end_x - self.cell_padding
            ey: int = sy

            if cell.neighbors["west"] and cell.neighbors["west"].walls["north"]:
                sx = x

            if cell.neighbors["east"] and cell.neighbors["east"].walls["north"]:
                ex = end_x

            pr.draw_line_ex(
                (sx, sy),
                (ex, ey),
                self.line_thickness,
                pr.DARKBLUE
            )

        if cell.walls["south"]:

            sx = x + self.cell_padding
            sy = end_y - self.cell_padding
            ex = end_x - self.cell_padding
            ey = sy

            if cell.neighbors["west"] and cell.neighbors["west"].walls["north"]:
                sx = x

            if cell.neighbors["east"] and cell.neighbors["east"].walls["north"]:
                ex = end_x

            pr.draw_line_ex(
                (sx, sy),
                (ex, ey),
                self.line_thickness,
                pr.DARKBLUE
            )

        if cell.walls["west"]:

            sx = x + self.cell_padding - self.line_thickness
            sy = y + self.cell_padding
            ex = x + self.cell_padding
            ey = end_y - self.cell_padding

            if cell.neighbors["north"] and cell.neighbors["north"].walls["west"]:
                sy = y

            if cell.neighbors["south"] and cell.neighbors["south"].walls["west"]:
                ey = end_y

            pr.draw_line_ex(
                (sx, sy),
                (ex, ey),
                self.line_thickness,
                pr.DARKBLUE
            )

        if cell.walls["east"]:

            sx = end_x - self.cell_padding
            sy = y + self.cell_padding
            ex = end_x - self.cell_padding + self.line_thickness
            ey = end_y - self.cell_padding

            if cell.neighbors["north"] and cell.neighbors["north"].walls["east"]:
                sy = y

            if cell.neighbors["south"] and cell.neighbors["south"].walls["east"]:
                ey = end_y

            pr.draw_line_ex(
                (sx, sy),
                (ex, ey),
                self.line_thickness,
                pr.DARKBLUE
            )

    def draw_cell(self, cell: Cell) -> None:

        ...

    def get_neighbors(self, cell: Cell) -> None:

        cell.neighbors: dict[str, Cell | None] = {
            direction: None
            for direction in ["north", "south", "east", "west"]
        }

        if cell.posx > 0:
            cell.neighbors["west"] = self.grid[cell.posy][cell.posx - 1]

        if cell.posx < len(self.grid[0]):
            cell.neighbors["east"] = self.grid[cell.posy][cell.posx + 1]

        if cell.posy > 0:
            cell.neighbors["north"] = self.grid[cell.posy - 1][cell.posx]

        if cell.posy < len(self.grid):
            cell.neighbors["south"] = self.grid[cell.posy + 1][cell.posx]

    def draw_grid(self) -> None:

        cell_y: int = self.map_y

        for row in self.grid:

            cell_x: int = self.map_x

            for cell in row:

                self.get_neighbors(cell)
                self.draw_walls(cell, cell_x, cell_y)

                cell_x += self.cell_size

            cell_y += self.cell_size
