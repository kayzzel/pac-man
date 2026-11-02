import pyray as pr
from ..game.map.Cell import Cell
from ..game.Game import Game
from ..utils.enum_utils import Game_state
from .Texture_pack import Texture_pack
from .widget import Icon, AnimIcon
from ..game.entity.Pac_man import Pac_man
from ..game.entity.Entity import Entity
from ..game.entity.ghost.Ghost import Ghost_state, Ghost

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
        game: Game,
        texture_pack: str
    ) -> None:

        self.game: Game = game
        self.texture_pack: Texture_pack = Texture_pack(texture_pack)
        self.collectible_icons: dict[str, Icon] = {}
        self.sprites: dict[str, AnimIcon] = {}

    def update_grid(
        self,
        grid: list[list[Cell]],
        map_size: tuple[int, int],
        map_coor: tuple[int, int],
        cell_size: int,
        entities: list[Entity]
    ) -> None:

        self.grid: list[list[Cell]] = grid
        self.entities: list[Entity] = entities
        self.saved_dirs: dict[str, tuple[str, str, tuple[float, float]]] = {
            entity.name: (entity.direction, "R", (entity.pos_x, entity.pos_y))
            for entity in entities
        }

        self.map_w, self.map_h = map_size
        self.map_x, self.map_y = map_coor

        self.cell_size: int = cell_size
        self.line_thickness: int = 3
        self.cell_padding: int = cell_size // 8 + self.line_thickness

        self.collectible_size: int = cell_size // 3
        self.entity_space: int = self.cell_size - self.cell_padding * 2
        self.entity_size: int = self.entity_space - self.entity_space // 8

        self.update_sprites()
        self.update_texture()

    def set_correct_dir(self, entity: Entity) -> None:

        if not self.game.state == Game_state.RUNNING:
            return

        alignment: str = self.saved_dirs[entity.name][1]

        if entity.direction != self.saved_dirs[entity.name][0]:
            match entity.direction:

                case "N":
                    alignment = "L" if alignment == "R" else "R"

                case "S":
                    if entity.direction == "N":
                        alignment = "L" if entity.alignment == "R" else "R"

                case "E":
                    alignment = "R"

                case "W":
                    alignment = "L"

        self.saved_dirs[entity.name] = (entity.direction, alignment, (entity.pos_x, entity.pos_y))

    def get_pacman_texture(self, pac_man: Pac_man) -> str:

        self.set_correct_dir(pac_man)
        if self.game.state == Game_state.DIED:
            return "pacman_death"
        return self.get_entity_texture(pac_man)

    def get_ghost_texture(self, ghost: Ghost) -> str:

        self.set_correct_dir(ghost)
        if ghost.state == Ghost_state.EATEN:
            return "eyes_" + DIRECTIONS[self.saved_dirs[ghost.name][0]]

        elif ghost.state == Ghost_state.FRIGHTENED:
            return "afraid_blue"

        return self.get_entity_texture(ghost)

    def get_entity_texture(self, entity: Entity) -> str:

        direction = self.saved_dirs[entity.name][0]
        alignment = self.saved_dirs[entity.name][1]

        texture_to_get: str = entity.name + "_" + DIRECTIONS[direction]

        if direction in ["N", "S"]:

            spe_texture: str = entity.name + "_" + DIRECTIONS[
                direction + alignment
            ]
            if spe_texture in self.texture_pack.all_textures.keys():
                texture_to_get = spe_texture

        return texture_to_get

    def draw_walls(self, cell: Cell, x: int, y: int) -> None:

        self.get_neighbors(cell)

        if all(wall for wall in cell.walls.values()):
            return

        end_x: int = x + self.cell_size
        end_y: int = y + self.cell_size

        if cell.walls["N"]:

            sx: int = x + self.cell_padding - 2
            sy: int = y + self.cell_padding
            ex: int = end_x - self.cell_padding
            ey: int = sy

            draw_corner_left: bool = False
            draw_corner_right: bool = False

            if not cell.walls["W"]:

                if cell.neighbors["W"] and cell.neighbors["W"].walls["N"]:
                    sx = x
                elif cell.neighbors["W"] and cell.neighbors["N"] and cell.neighbors["N"].walls["W"]:
                    sx = x - self.cell_padding
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
                    (sx, y),
                    (sx, sy),
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

            sx = x + self.cell_padding - 2
            sy = end_y - self.cell_padding
            ex = end_x - self.cell_padding
            ey = sy

            draw_corner_left = False
            draw_corner_right = False

            if not cell.walls["W"]:

                if cell.neighbors["W"] and cell.neighbors["W"].walls["S"]:
                    sx = x
                elif cell.neighbors["W"] and cell.neighbors["S"] and cell.neighbors["S"].walls["W"]:
                    sx = x - self.cell_padding
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
                    (sx, end_y),
                    (sx, sy),
                    self.line_thickness,
                    pr.DARKBLUE
                )
            if draw_corner_right:
                pr.draw_line_ex(
                    (ex, end_y),
                    (ex, ey),
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
                    sy = y - self.cell_padding
                else:
                    draw_corner_up = True

            if not cell.walls["S"]:

                if cell.neighbors["S"] and cell.neighbors["S"].walls["W"]:
                    ey = end_y
                elif cell.neighbors["S"] and cell.neighbors["W"] and cell.neighbors["W"].walls["S"]:
                    ey = end_y + self.cell_padding
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
                    sy = y - self.cell_padding
                else:
                    draw_corner_up = True

            if not cell.walls["S"]:

                if cell.neighbors["S"] and cell.neighbors["S"].walls["E"]:
                    ey = end_y
                elif cell.neighbors["S"] and cell.neighbors["E"] and cell.neighbors["E"].walls["S"]:
                    ey = end_y + self.cell_padding
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
                    (ex, sy),
                    (end_x, sy),
                    self.line_thickness,
                    pr.DARKBLUE
                )
            if draw_corner_down:
                pr.draw_line_ex(
                    (ex, ey),
                    (end_x, ey),
                    self.line_thickness,
                    pr.DARKBLUE
                )

        if cell.collectible and cell.collectible.name not in self.collectible_icons.keys():
            self.collectible_icons[cell.collectible.name] = Icon(
                0,
                0,
                self.texture_pack.get_texture(cell.collectible.name),
                (self.collectible_size, self.collectible_size),
                True
            )

    def update_sprites(self) -> None:

        for icon in self.collectible_icons.values():
            icon._unload_image()

        for sprite in self.sprites.values():
            sprite._unload_image()

        self.collectible_icons = {}
        self.sprites = {}

    def draw_sprites(self, cell: Cell, x: int, y: int) -> None:

        if cell.collectible and cell.collectible.name in self.collectible_icons.keys():

            collectible: Icon = self.collectible_icons[cell.collectible.name]
            collectible.x = x + (self.cell_size - self.collectible_size) // 2
            collectible.y = y + (self.cell_size - self.collectible_size) // 2
            collectible.display_widget()

        entity_base_x: int = x + self.cell_padding
        entity_base_y: int = y + self.cell_padding

        for entity in self.entities:

            if not self.entity_is_in(entity, cell):
                continue

            self.set_correct_dir(entity)
            en_posx: float
            en_posy: float
            en_posx, en_posy = self.saved_dirs[entity.name][2]
            # print(f"cell pos {x, y}, entity coor : {en_posx, en_posy}")
            entity_offset_x: int = int((en_posx - cell.pos_x) * 10)
            entity_offset_y: int = int((en_posy - cell.pos_y) * 10)
            # print(f"offset before : {entity_offset_x, entity_offset_y}")

            en_posx = entity_base_x - self.entity_size // 2
            if entity_offset_x > 0:
                en_posx += (self.entity_space // 10) * entity_offset_x
            en_posy = entity_base_y - self.entity_size // 2
            if entity_offset_y > 0:
                en_posy += (self.entity_space // 10) * entity_offset_y
            # print(f"entity {entity.name}: entity pos {en_posx, en_posy} offset_x: {entity_offset_x} offset_y : {entity_offset_y}\n")

            texture_path = self.texture_pack.get_texture((
                self.get_pacman_texture(entity)
                if isinstance(entity, Pac_man)
                else self.get_ghost_texture(entity)
            ))

            if texture_path not in self.sprites.keys() or texture_path != self.sprites[texture_path].image_path:

                sprite_frames: int = 6
                if "death" in texture_path:
                    sprite_frames = 8

                self.sprites[texture_path] = AnimIcon(
                    0,
                    0,
                    texture_path,
                    (self.entity_size, self.entity_size),
                    True,
                    sprite_frames
                )
            self.sprites[texture_path].x = en_posx
            self.sprites[texture_path].y = en_posy

            self.sprites[texture_path].display_widget()

            self.check_death()

    def check_death(self) -> None:

        pacman_death_path: str = self.texture_pack.get_texture("pacman_death")
        if self.game.state == Game_state.DIED and pacman_death_path in self.sprites.keys() and self.sprites[pacman_death_path].loop_finished:
            self.game.resume()

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

    def entity_is_in(self, entity: Entity, cell: Cell) -> bool:

        return (
            cell.pos_x <= entity.pos_x < cell.pos_x + 1
            and cell.pos_y <= entity.pos_y < cell.pos_y + 1
        )

    def update_texture(self) -> None:

        if hasattr(self, "grid_texture"):
            pr.unload_render_texture(self.grid_texture)

        self.grid_texture = pr.load_render_texture(self.map_w, self.map_h)
        pr.end_drawing()
        pr.begin_texture_mode(self.grid_texture)
        pr.clear_background(pr.BLACK)

        cell_y: int = 0

        for row in self.grid:

            cell_x: int = 0

            for cell in row:

                self.draw_walls(cell, cell_x, cell_y)

                cell_x += self.cell_size

            cell_y += self.cell_size

        pr.end_texture_mode()
        pr.begin_drawing()

    def display_grid(self) -> None:

        pr.draw_texture_rec(
            self.grid_texture.texture,
            (0, 0, float(self.map_w), -float(self.map_h)),
            (self.map_x, self.map_y),
            pr.RAYWHITE
        )

        cell_y: int = self.map_y

        for row in self.grid:

            cell_x: int = self.map_x

            for cell in row:

                self.draw_sprites(cell, cell_x, cell_y)

                cell_x += self.cell_size

            cell_y += self.cell_size
