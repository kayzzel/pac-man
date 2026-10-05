import pyray as pr
from ..game.map.Cell import Cell
from .Texture_pack import Texture_pack

DEFAULT_TEXTURE_PACK: str = "src/view/assets/default_texture_pack"

DIRECTIONS: dict[str, str] = {
    "N": "up",
    "S": "down",
    "W": "left",
    "E": "right",
    "NR": "upright",
    "NL": "upleft",
    "SR": "downright",
    "SL": "downleft"
}


class Map_renderer:

    def __init__(
        self,
        grid: list[list[Cell]],
        map_coor: tuple[int, int],
        cell_size: int,
        entities: list[Entity]
    ) -> None:

        self.grid: list[list[Cell]] = grid
        self.map_x, self.map_y = map_coor
        self.cell_size: int = cell_size
        self.line_thickness: int = 2
        self.cell_padding: int = cell_size // 6 + self.line_thickness
        self.texture_size: int = cell_size // 3
        self.texture_pack: Texture_pack = Texture_pack(DEFAULT_TEXTURE_PACK)

    def set_correct_dir(self, entity: Entity) -> None:

        match entity.next_direction:

            case "N":
                entity.alignment = "L" if entity.alignment == "R" else "R"

            case "S":
                if entity.next_direction == "N":
                    entity.alignment = "L" if entity.alignment == "R" else "R"

            case "E":
                entity.alignment = "R"

            case "W":
                entity.alignment = "L"

    def get_pacman_texture(self, pac_man: Pac_man) -> str:

        return self.get_entity_texture(pac_man)

    def get_ghost_texture(self, ghost: Ghost) -> str:

        if ghost_state == Ghost_state.EATEN:
            return "eyes_" + DIRECTIONS[ghost.next_direction]

        elif ghost_state == Ghost_state.FRIGHTENED:
            return "afraid_blue_" + DIRECTIONS[ghost.next_direction]

        return self.get_entity_texture(ghost)

    def get_entity_texture(self, entity: Entity) -> str:

        self.set_correct_dir(entity)
        texture_to_get: str = entity.name + "_" + DIRECTIONS[entity.next_direction]

        if entity.next_direction in ["N", "S"]:

            spe_texture: str = entity.name + "_" + DIRECTIONS[
                entity.next_direction + entity.alignment
            ]
            if spe_texture in self.texture_pack.all_textures.keys():
                texture_to_get = spe_texture

        return texture_to_get

    def draw_walls(self, cell: Cell, x: int, y: int) -> None:

        if all(wall for wall in cell.walls.values()):
            return

        end_x: int = x + self.cell_size
        end_y: int = y + self.cell_size

        if cell.walls["N"]:

            sx: int = x + self.cell_padding
            sy: int = y + self.cell_padding - self.line_thickness
            ex: int = end_x - self.cell_padding
            ey: int = sy

            draw_corner_left: bool = False
            draw_corner_right: bool = False

            if not cell.walls["W"]:

                if cell.neighbors["W"] and cell.neighbors["W"].walls["N"]:
                    sx = x
                elif cell.neighbors["W"] and cell.neighbors["N"] and cell.neighbors["N"].walls["W"]:
                    sx = x - self.cell_padding + self.line_thickness
                else:
                    draw_corner_left = True

            if not cell.walls["E"]:

                if cell.neighbors["E"] and cell.neighbors["E"].walls["N"]:
                    ex = end_x
                elif cell.neighbors["E"] and cell.neighbors["N"] and cell.neighbors["N"].walls["E"]:
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

        if cell.walls["S"]:

            sx = x + self.cell_padding
            sy = end_y - self.cell_padding
            ex = end_x - self.cell_padding
            ey = sy

            draw_corner_left = False
            draw_corner_right = False

            if not cell.walls["W"]:

                if cell.neighbors["W"] and cell.neighbors["W"].walls["S"]:
                    sx = x
                elif cell.neighbors["W"] and cell.neighbors["S"] and cell.neighbors["S"].walls["W"]:
                    sx = x - self.cell_padding + self.line_thickness
                else:
                    draw_corner_left = True

            if not cell.walls["E"]:

                if cell.neighbors["E"] and cell.neighbors["E"].walls["S"]:
                    ex = end_x
                elif cell.neighbors["E"] and cell.neighbors["S"] and cell.neighbors["S"].walls["E"]:
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

        if cell.walls["W"]:

            sx = x + self.cell_padding - self.line_thickness
            sy = y + self.cell_padding
            ex = sx
            ey = end_y - self.cell_padding

            draw_corner_up = False
            draw_corner_down = False

            if not cell.walls["N"]:

                if cell.neighbors["N"] and cell.neighbors["N"].walls["W"]:
                    sy = y
                elif cell.neighbors["N"] and cell.neighbors["W"] and cell.neighbors["W"].walls["N"]:
                    sy = y - self.cell_padding + self.line_thickness
                else:
                    draw_corner_up = True

            if not cell.walls["S"]:

                if cell.neighbors["S"] and cell.neighbors["S"].walls["W"]:
                    ey = end_y
                elif cell.neighbors["S"] and cell.neighbors["W"] and cell.neighbors["W"].walls["S"]:
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

        if cell.walls["E"]:

            sx = end_x - self.cell_padding
            sy = y + self.cell_padding
            ex = sx
            ey = end_y - self.cell_padding

            draw_corner_up = False
            draw_corner_down = False

            if not cell.walls["N"]:

                if cell.neighbors["N"] and cell.neighbors["N"].walls["E"]:
                    sy = y
                elif cell.neighbors["N"] and cell.neighbors["E"] and cell.neighbors["E"].walls["N"]:
                    sy = y - self.cell_padding + self.line_thickness
                else:
                    draw_corner_up = True

            if not cell.walls["S"]:

                if cell.neighbors["S"] and cell.neighbors["S"].walls["E"]:
                    ey = end_y
                elif cell.neighbors["S"] and cell.neighbors["E"] and cell.neighbors["E"].walls["S"]:
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

    def draw_cell(self, cell: Cell, x: int, y: int) -> None:

        self.get_neighbors(cell)
        self.draw_walls(cell, x, y)

        if cell.collectible:
            collectible_image = pr.load_image(self.texture_pack.get_texture(cell.collectible.name))
            pr.image_resize(collectible_image, self.texture_size, self.texture_size)
            collectible_texture = pr.load_texture_from_image(collectible_image)
            pr.draw_texture(collectible_texture, self.text_x, self.text_y)

        for entity in self.entities:

            if not self.entity_is_in(entity, cell_x, cell_y):
                continue

            entity_texture = (
                self.get_pacman_texture(entity)
                if isinstance(entity, Pac_man)
                else self.get_ghost_texture(entity)
            )

    def get_neighbors(self, cell: Cell) -> None:

        cell.neighbors: dict[str, Cell | None] = {
            direction: None
            for direction in ["N", "S", "E", "W"]
        }

        if cell.pos_x > 0:
            cell.neighbors["W"] = self.grid[cell.pos_y][cell.pos_x - 1]

        if cell.pos_x < len(self.grid[0]) - 1:
            cell.neighbors["E"] = self.grid[cell.pos_y][cell.pos_x + 1]

        if cell.pos_y > 0:
            cell.neighbors["N"] = self.grid[cell.pos_y - 1][cell.pos_x]

        if cell.pos_y < len(self.grid) - 1:
            cell.neighbors["S"] = self.grid[cell.pos_y + 1][cell.pos_x]

    def entity_is_in(self, entity: Entity, x: int, y: int) -> bool:

        return (
            x <= entity.pos_x < x + self.cell_size
            and y <= entity_pos_y < y + self.cell_size
        )

    def draw_grid(self) -> None:

        cell_y: int = self.map_y

        for row in self.grid:

            cell_x: int = self.map_x

            for cell in row:

                self.draw_cell(cell, cell_x, cell_y)

                cell_x += self.cell_size

            cell_y += self.cell_size

        for entity in self.entities:


