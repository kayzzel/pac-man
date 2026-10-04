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

        if all(wall for wall in cell.walls.values()):
            return

        end_x: int = x + self.cell_size
        end_y: int = y + self.cell_size

        if cell.walls["north"]:

            sx: int = x + self.cell_padding
            sy: int = y + self.cell_padding - self.line_thickness
            ex: int = end_x - self.cell_padding
            ey: int = sy

            draw_corner_left: bool = False
            draw_corner_right: bool = False

            if not cell.walls["west"]:

                if cell.neighbors["west"] and cell.neighbors["west"].walls["north"]:
                    sx = x
                elif cell.neighbors["west"] and cell.neighbors["north"] and cell.neighbors["north"].walls["west"]:
                    sx = x - self.cell_padding + self.line_thickness
                else:
                    draw_corner_left = True

            if not cell.walls["east"]:

                if cell.neighbors["east"] and cell.neighbors["east"].walls["north"]:
                    ex = end_x
                elif cell.neighbors["east"] and cell.neighbors["north"] and cell.neighbors["north"].walls["east"]:
                    ex = end_x + self.cell_padding - self.line_thickness
                else:
                    draw_corner_right = True

            pr.draw_line_ex(
                (sx, sy),
                (ex, ey),
                self.line_thickness,
                pr.DARKBLUE
            )
            if draw_corner_left:
                pr.draw_line_ex(
                    (sx - self.line_thickness, y),
                    (sx - self.line_thickness, sy),
                    self.line_thickness,
                    pr.DARKBLUE
                )
            if draw_corner_right:
                pr.draw_line_ex(
                    (ex, y),
                    (ex, ey),
                    self.line_thickness,
                    pr.DARKBLUE
                )

        if cell.walls["south"]:

            sx = x + self.cell_padding
            sy = end_y - self.cell_padding
            ex = end_x - self.cell_padding
            ey = sy

            draw_corner_left = False
            draw_corner_right = False

            if not cell.walls["west"]:

                if cell.neighbors["west"] and cell.neighbors["west"].walls["south"]:
                    sx = x
                elif cell.neighbors["west"] and cell.neighbors["south"] and cell.neighbors["south"].walls["west"]:
                    sx = x - self.cell_padding + self.line_thickness
                else:
                    draw_corner_left = True

            if not cell.walls["east"]:

                if cell.neighbors["east"] and cell.neighbors["east"].walls["south"]:
                    ex = end_x
                elif cell.neighbors["east"] and cell.neighbors["south"] and cell.neighbors["south"].walls["east"]:
                    ex = end_x + self.cell_padding - self.line_thickness
                else:
                    draw_corner_right = True

            pr.draw_line_ex(
                (sx, sy),
                (ex, ey),
                self.line_thickness,
                pr.DARKBLUE
            )
            if draw_corner_left:
                pr.draw_line_ex(
                    (sx - self.line_thickness, end_y),
                    (sx - self.line_thickness, sy + self.line_thickness),
                    self.line_thickness,
                    pr.DARKBLUE
                )
            if draw_corner_right:
                pr.draw_line_ex(
                    (ex, end_y),
                    (ex, ey + self.line_thickness),
                    self.line_thickness,
                    pr.DARKBLUE
                )

        if cell.walls["west"]:

            sx = x + self.cell_padding - self.line_thickness
            sy = y + self.cell_padding
            ex = sx
            ey = end_y - self.cell_padding

            draw_corner_up = False
            draw_corner_down = False

            if not cell.walls["north"]:

                if cell.neighbors["north"] and cell.neighbors["north"].walls["west"]:
                    sy = y
                elif cell.neighbors["north"] and cell.neighbors["west"] and cell.neighbors["west"].walls["north"]:
                    sy = y - self.cell_padding + self.line_thickness
                else:
                    draw_corner_up = True

            if not cell.walls["south"]:

                if cell.neighbors["south"] and cell.neighbors["south"].walls["west"]:
                    ey = end_y
                elif cell.neighbors["south"] and cell.neighbors["west"] and cell.neighbors["west"].walls["south"]:
                    ey = end_y + self.cell_padding - self.line_thickness
                else:
                    draw_corner_down = True

            pr.draw_line_ex(
                (sx, sy),
                (ex, ey),
                self.line_thickness,
                pr.DARKBLUE
            )
            if draw_corner_up:
                pr.draw_line_ex(
                    (x, sy),
                    (sx, sy),
                    self.line_thickness,
                    pr.DARKBLUE
                )
            if draw_corner_down:
                pr.draw_line_ex(
                    (x, ey),
                    (sx, ey),
                    self.line_thickness,
                    pr.DARKBLUE
                )

        if cell.walls["east"]:

            sx = end_x - self.cell_padding
            sy = y + self.cell_padding
            ex = sx
            ey = end_y - self.cell_padding

            draw_corner_up = False
            draw_corner_down = False

            if not cell.walls["north"]:

                if cell.neighbors["north"] and cell.neighbors["north"].walls["east"]:
                    sy = y
                elif cell.neighbors["north"] and cell.neighbors["east"] and cell.neighbors["east"].walls["north"]:
                    sy = y - self.cell_padding + self.line_thickness
                else:
                    draw_corner_up = True

            if not cell.walls["south"]:

                if cell.neighbors["south"] and cell.neighbors["south"].walls["east"]:
                    ey = end_y
                elif cell.neighbors["south"] and cell.neighbors["east"] and cell.neighbors["east"].walls["south"]:
                    ey = end_y + self.cell_padding - self.line_thickness
                else:
                    draw_corner_down = True

            pr.draw_line_ex(
                (sx, sy),
                (ex, ey),
                self.line_thickness,
                pr.DARKBLUE
            )
            if draw_corner_up:
                pr.draw_line_ex(
                    (ex + self.line_thickness, sy),
                    (end_x, sy),
                    self.line_thickness,
                    pr.DARKBLUE
                )
            if draw_corner_down:
                pr.draw_line_ex(
                    (ex + self.line_thickness, ey),
                    (end_x, ey),
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

        if cell.pos_x > 0:
            cell.neighbors["west"] = self.grid[cell.pos_y][cell.pos_x - 1]

        if cell.pos_x < len(self.grid[0]) - 1:
            cell.neighbors["east"] = self.grid[cell.pos_y][cell.pos_x + 1]

        if cell.pos_y > 0:
            cell.neighbors["north"] = self.grid[cell.pos_y - 1][cell.pos_x]

        if cell.pos_y < len(self.grid) - 1:
            cell.neighbors["south"] = self.grid[cell.pos_y + 1][cell.pos_x]

    def draw_grid(self) -> None:

        cell_y: int = self.map_y

        for row in self.grid:

            cell_x: int = self.map_x

            for cell in row:

                self.get_neighbors(cell)
                self.draw_walls(cell, cell_x, cell_y)

                cell_x += self.cell_size

            cell_y += self.cell_size
