import pyray as pr

from .Texture_pack import Texture_pack
from .widget import Icon, AnimIcon

from ..game.Game import Game
from ..game.map.Cell import Cell
from ..game.entity.Pac_man import Pac_man
from ..game.entity.Entity import Entity
from ..game.entity.collectible.Consumable import Consumable
from ..game.entity.ghost.Ghost import Ghost
from ..utils.enum_utils import Game_state, Pacman_state, Ghost_state


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

    """
    A class that handles the rendering and display of the game map.
    """

    def __init__(
        self,
        game: Game,
        texture_pack: str
    ) -> None:

        """
        Initializes the main attributes of the map renderer,
        creating the sprites dictionaries.

        Parameters
        ----------
        game: Game
            The game the player has started.
        texture_pack: str
            The texture pack to use for loading the sprites.
        """

        self.game: Game = game
        self.texture_pack: Texture_pack = Texture_pack(texture_pack)
        self.collectible_icons: dict[str, Icon] = {}
        self.sprites: dict[str, AnimIcon] = {}
        self.end_states: list[Game_state] = [
            Game_state.WON,
            Game_state.LOST,
            Game_state.DIED,
            Game_state.FINISHED_MAP
        ]

    def update_grid(
        self,
        grid: list[list[Cell]],
        map_size: tuple[int, int],
        map_coor: tuple[int, int],
        cell_size: int,
        entities: list[Entity]
    ) -> None:

        """
        Updates the map renderer's grid and map values (x, y, w, h, etc)
        aswell as resetting the entities'
        saved directions, alignment and coordinates.
        Also calculates the size of
        cells, wall lines, and entities/collectibles.
        Redraws the grid's texture (walls) to avoid drawing them every loop.

        Parameters
        ----------
        grid: list[list[Cell]]
            The cells of the map to render.
        map_size: tuple[int, int]
            Respectively the width and height of the map.
        map_coor: tuple[int, int]
            Respectively the x and y coordinates of the map.
        cell_size: int
            The size the cell takes on the screen.
        entities: list[Entity]
            All the entities that are part of the game.
        """

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
        self.consumable_size: int = cell_size // 2
        self.entity_space: int = self.cell_size - self.cell_padding * 2
        self.entity_size: int = self.entity_space - self.entity_space // 8

        self.update_sprites()
        self.update_texture()

    def set_correct_dir(self, entity: Entity) -> None:

        """
        Stores the given entity's direction, alignment and coordinates
        inside a dictionary, the entity's name being the key.

        Parameters
        ----------
        entity: Entity
            The entity for which to store
            the direction, alignment and coordinates.
        """

        if self.game.state not in [Game_state.RUNNING, *self.end_states]:
            return

        alignment: str = self.saved_dirs[entity.name][1]

        if entity.direction != self.saved_dirs[entity.name][0]:
            match entity.direction:

                case "N":
                    alignment = "L" if alignment == "R" else "R"

                case "S":
                    if self.saved_dirs[entity.name][0] == "N":
                        alignment = "L" if alignment == "R" else "R"

                case "E":
                    alignment = "R"

                case "W":
                    alignment = "L"

        self.saved_dirs[entity.name] = (
            entity.direction,
            alignment,
            (entity.pos_x, entity.pos_y)
        )

    def get_pacman_texture(self, pac_man: Pac_man) -> str:

        """
        Determines which texture to use for PacMan
        based on his state (dead or alive).

        Parameters
        ----------
        pac_man: Pac_man
            The PacMan entity for which to return the texture path.

        Returns
        -------
        str
            The path of the texture to use for PacMan.
        """

        self.set_correct_dir(pac_man)
        if (
            self.game.state in self.end_states
            and self.game.state not in [
                Game_state.WON, Game_state.FINISHED_MAP
            ]
        ):
            return "pacman_death"
        return self.get_entity_texture(pac_man)

    def get_ghost_texture(self, ghost: Ghost) -> str:

        """
        Determines which texture to use for a ghost
        based on its state (eaten, frightened or normal).

        Parameters
        ----------
        ghost: Ghost
            The Ghost entity for which to return the texture path.

        Returns
        -------
        str
            The path of the texture to use for the ghost.
        """

        self.set_correct_dir(ghost)
        if ghost.state == Ghost_state.EATEN:
            return "eyes_" + DIRECTIONS[self.saved_dirs[ghost.name][0]]

        elif ghost.state == Ghost_state.FRIGHTENED:
            if self.pacman_state == Pacman_state.ENERGIZED_END:
                return "afraid_blinking"
            return "afraid_blue"

        return self.get_entity_texture(ghost)

    def get_entity_texture(self, entity: Entity) -> str:

        """
        Determines which texture to use for an entity
        based on its stored direction and alignment.

        Parameters
        ----------
        entity: Entity
            The entity for which to return the texture path.

        Returns
        -------
        str
            The path of the texture to use for the entity.
        """

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

        """
        Draws all of the given cell's walls,
        calculating the lines to draw based on its neighbors
        and whether or not the walls form an angle etc.

        Parameters
        ----------
        cell: Cell
            The cell for which to draw the walls.
        x: int
            The cell's x coordinate (inside the grid, not on the screen).
        y: int
            The cell's y coordinate (inside the grid, not on the screen).
        """

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
                elif (
                    cell.neighbors["W"]
                    and cell.neighbors["N"]
                    and cell.neighbors["N"].walls["W"]
                ):
                    sx = x - self.cell_padding
                else:
                    draw_corner_left = True

            if not cell.walls["E"]:

                if cell.neighbors["E"] and cell.neighbors["E"].walls["N"]:
                    ex = end_x
                elif (
                    cell.neighbors["E"]
                    and cell.neighbors["N"]
                    and cell.neighbors["N"].walls["E"]
                ):
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
                elif (
                    cell.neighbors["W"]
                    and cell.neighbors["S"]
                    and cell.neighbors["S"].walls["W"]
                ):
                    sx = x - self.cell_padding
                else:
                    draw_corner_left = True

            if not cell.walls["E"]:

                if cell.neighbors["E"] and cell.neighbors["E"].walls["S"]:
                    ex = end_x
                elif (
                    cell.neighbors["E"]
                    and cell.neighbors["S"]
                    and cell.neighbors["S"].walls["E"]
                ):
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
                elif (
                    cell.neighbors["N"]
                    and cell.neighbors["W"]
                    and cell.neighbors["W"].walls["N"]
                ):
                    sy = y - self.cell_padding
                else:
                    draw_corner_up = True

            if not cell.walls["S"]:

                if cell.neighbors["S"] and cell.neighbors["S"].walls["W"]:
                    ey = end_y
                elif (
                    cell.neighbors["S"]
                    and cell.neighbors["W"]
                    and cell.neighbors["W"].walls["S"]
                ):
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
                elif (
                    cell.neighbors["N"]
                    and cell.neighbors["E"]
                    and cell.neighbors["E"].walls["N"]
                ):
                    sy = y - self.cell_padding
                else:
                    draw_corner_up = True

            if not cell.walls["S"]:

                if cell.neighbors["S"] and cell.neighbors["S"].walls["E"]:
                    ey = end_y
                elif (
                    cell.neighbors["S"]
                    and cell.neighbors["E"]
                    and cell.neighbors["E"].walls["S"]
                ):
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

    def add_collectibles(self, cell: Cell) -> None:

        """
        Adds the cell's collectibles icons to the collectible dictionary
        if the icon for this texture is not already built and stored.

        Parameters
        ----------
        cell: Cell
            The cell for which to add collectibles' icons.
        """

        if (
            cell.collectible
            and cell.collectible.name not in self.collectible_icons.keys()
        ):

            texture_name: str = cell.collectible.name
            texture_size: int = self.collectible_size

            if isinstance(cell.collectible, Consumable):
                texture_name += "_c"
                texture_size = self.consumable_size

            self.collectible_icons[cell.collectible.name] = Icon(
                0,
                0,
                self.texture_pack.get_texture(texture_name),
                (texture_size, texture_size),
                True
            )

    def calculate_entity_pos(
        self,
        en_posx: float,
        en_posy: float
    ) -> tuple[int, int]:

        """
        Calculates the entity position (on the screen) directly from
        its float position in the grid: multiplying by the full cell
        size keeps the sprite continuous when it crosses a cell
        boundary, where the old per-cell mapping used to jump.

        Parameters
        ----------
        en_posx: float
            The entity's x coordinate in the grid (cell units).
        en_posy: float
            The entity's y coordinate in the grid (cell units).

        Returns
        -------
        tuple[int, int]
            The entity's pixel coordinates on the screen.
        """

        posx = int(
            self.map_x + en_posx * self.cell_size - self.entity_size // 2
        )
        posy = int(
            self.map_y + en_posy * self.cell_size - self.entity_size // 2
        )
        return (posx, posy)

    def _unload_images(self) -> None:

        """
        Unloads all the sprites' images and textures,
        aswell as the grid texture if it has been created.
        """

        for icon in self.collectible_icons.values():
            icon._unload_image()

        for sprite in self.sprites.values():
            sprite._unload_image()

        if hasattr(self, "grid_texture"):
            pr.unload_render_texture(self.grid_texture)

    def update_sprites(self) -> None:

        """
        Resets the collectibles/sprites/current sprites dictionaries to empty.
        """

        self.collectible_icons = {}
        self.sprites = {}
        self.current_sprites: dict[str, AnimIcon] = {}

    def draw_sprites(self, cell: Cell, x: int, y: int) -> None:

        """
        Displays all the sprites needed by searching for their icons
        inside the collectibles/sprites dictionaries, and simply changing
        their coordinates based on the cell given before displaying them.

        Parameters
        ----------
        cell: Cell
            The current cell for which to display the sprites.
        x: int
            The cell's x coordinate (inside the grid).
        y: int
            The cell's y coordinate (inside the grid).
        """

        if (
            cell.collectible
            and cell.collectible.name in self.collectible_icons.keys()
        ):

            collectible: Icon = self.collectible_icons[cell.collectible.name]
            collectible.x = x + (self.cell_size - collectible.i_w) // 2
            collectible.y = y + (self.cell_size - collectible.i_h) // 2
            collectible.display_widget()

        for entity in self.entities:

            if not self.entity_is_in(entity, cell):
                continue

            if isinstance(entity, Pac_man):
                self.pacman_state = entity.is_energized

            self.set_correct_dir(entity)
            en_posx: int
            en_posy: int
            en_posx, en_posy = self.calculate_entity_pos(
                *self.saved_dirs[entity.name][2]
            )

            if isinstance(entity, Pac_man):
                texture_path = self.texture_pack.get_texture(
                    self.get_pacman_texture(entity)
                )
            elif isinstance(entity, Ghost):
                texture_path = self.texture_pack.get_texture(
                    self.get_ghost_texture(entity)
                )
            else:
                continue

            if (
                texture_path not in self.sprites.keys()
                or texture_path != self.sprites[texture_path].image_path
            ):

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
            self.current_sprites[entity.name] = self.sprites[texture_path]

            self.check_over()

    def check_over(self) -> bool:

        """
        Checks if the game is finished, and whether or not the PacMan animation
        displayed on the screen has finished its loop.

        Returns
        -------
        bool
            True if PacMan has finished animating, False otherwise.
        """

        if (
            "pacman" not in self.current_sprites.keys()
            or self.game.state not in self.end_states
        ):
            return True

        pacman_death_path: str = self.texture_pack.get_texture("pacman_death")

        if (
            self.game.state in self.end_states
            and self.current_sprites["pacman"].loop_finished
        ):
            if (
                pacman_death_path == self.current_sprites["pacman"].image_path
                and self.game.state == Game_state.DIED
            ):
                self.current_sprites["pacman"].reset_loop()
                self.game.resume()

            elif self.game.state in [Game_state.WON, Game_state.FINISHED_MAP]:

                if not hasattr(self, "end_loop_counter"):
                    self.end_loop_counter: int = 0

                if self.end_loop_counter < 3:
                    self.current_sprites["pacman"].reset_loop()
                    self.end_loop_counter += 1
                    return False

            return True

        return False

    def get_neighbors(self, cell: Cell) -> None:

        """
        Determines the given cell's neighboring cells.

        Parameters
        ----------
        cell: Cell
            The cell for which to determine its neighbors.
        """

        if cell.pos_x > 0:
            cell.neighbors["W"] = self.grid[cell.pos_y][cell.pos_x - 1]

        if cell.pos_x < len(self.grid[0]) - 1:
            cell.neighbors["E"] = self.grid[cell.pos_y][cell.pos_x + 1]

        if cell.pos_y > 0:
            cell.neighbors["N"] = self.grid[cell.pos_y - 1][cell.pos_x]

        if cell.pos_y < len(self.grid) - 1:
            cell.neighbors["S"] = self.grid[cell.pos_y + 1][cell.pos_x]

    def entity_is_in(self, entity: Entity, cell: Cell) -> bool:

        """
        Checks whether or not the given entity is inside the given cell.

        Parameters
        ----------
        entity: Entity
            The entity to check if it's inside a specific cell.
        cell: Cell
            The cell to check if the entity is inside of.

        Returns
        -------
        bool
            True if the entity is inside the cell, False otherwise.
        """

        return (
            cell.pos_x <= entity.pos_x < cell.pos_x + 1
            and cell.pos_y <= entity.pos_y < cell.pos_y + 1
        )

    def update_texture(self) -> None:

        """
        Creates and draws the whole grid on a render texture to avoid
        re-drawing the walls each frame.
        """

        self.grid_texture = pr.load_render_texture(self.map_w, self.map_h)
        pr.begin_texture_mode(self.grid_texture)
        pr.clear_background(pr.BLACK)

        cell_y: int = 0

        for row in self.grid:

            cell_x: int = 0

            for cell in row:

                self.draw_walls(cell, cell_x, cell_y)
                self.add_collectibles(cell)

                cell_x += self.cell_size

            cell_y += self.cell_size

        pr.end_texture_mode()

    def display_grid(self) -> None:

        """
        Displays the render texture of the grid (walls),
        and all the sprites needed on the screen.
        """

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


class Custom_map_renderer(Map_renderer):

    """
    A custom map renderer used to display a custom map
    for the Custom_view.
    """

    def __init__(self) -> None:

        """
        Empty init because this map renderer does not need
        any of the init parameters of its parent.
        """
        ...

    def update_special_grid(
        self,
        grid: list[list[Cell]],
        map_size: tuple[int, int],
        map_coor: tuple[int, int],
        cell_size: int,
        show_lines: bool = False
    ) -> None:

        """
        Updates the map renderer's grid and map values (x, y, w, h, etc)
        aswell as calculates the size of
        cells, wall lines, and entities/collectibles.
        Redraws the grid's texture (walls) to avoid drawing them every loop.

        Parameters
        ----------
        grid: list[list[Cell]]
            The cells of the map to render.
        map_size: tuple[int, int]
            Respectively the width and height of the map.
        map_coor: tuple[int, int]
            Respectively the x and y coordinates of the map.
        cell_size: int
            The size the cell takes on the screen.
        show_lines: bool (default False)
            True if the grid mapping lines (square cut lines)
            should be displayed behind the walls on the grid texture.
        """

        self.grid: list[list[Cell]] = grid

        self.map_w, self.map_h = map_size
        self.map_x, self.map_y = map_coor

        self.cell_size: int = cell_size
        self.line_thickness: int = 3
        self.cell_padding: int = cell_size // 8 + self.line_thickness

        self.collectible_size: int = cell_size // 3
        self.consumable_size: int = cell_size // 2
        self.entity_space: int = self.cell_size - self.cell_padding * 2
        self.entity_size: int = self.entity_space - self.entity_space // 8

        self.update_texture(show_lines)

    def _unload_images(self) -> None:

        """
        Unloads the render texture for the grid if it has been created.
        """

        if hasattr(self, "grid_texture"):
            pr.unload_render_texture(self.grid_texture)

    def update_texture(self, show_lines: bool = False) -> None:

        """
        Creates and draws the whole grid on a render texture to avoid
        re-drawing the walls each frame,
        also drawing mapping lines of the grid behind the walls
        if needed.
        """

        self.grid_texture = pr.load_render_texture(
            self.map_w + self.cell_padding,
            self.map_h + self.cell_padding - self.line_thickness
        )
        pr.begin_texture_mode(self.grid_texture)
        pr.clear_background(pr.BLACK)

        if show_lines:

            cell_y: int = 0
            for row_i, row in enumerate(self.grid):
                cell_x: int = 0
                for cell_i, cell in enumerate(row):
                    line_x: int = cell_x + self.cell_size
                    line_y: int = cell_y + self.cell_size

                    if cell_i == 0 or cell_i == len(row) - 1:
                        line_x += self.cell_padding // 2

                    if row_i == 0 or row_i == len(self.grid) - 1:
                        line_y += self.cell_padding // 2

                    if row_i > 0:
                        pr.draw_line(
                            cell_x, cell_y, line_x, cell_y, pr.LIGHTGRAY
                        )
                    if cell_i > 0:
                        pr.draw_line(
                            cell_x, cell_y, cell_x, line_y, pr.LIGHTGRAY
                        )

                    cell_x += self.cell_size
                    if cell_i == 0:
                        cell_x += self.cell_padding // 2

                cell_y += self.cell_size
                if row_i == 0:
                    cell_y += self.cell_padding // 2

        pr.draw_rectangle_lines_ex(
            (
                0,
                0,
                self.map_w + self.cell_padding,
                self.map_h + self.cell_padding - self.line_thickness
            ),
            self.line_thickness,
            pr.DARKBLUE
        )

        cell_y = self.cell_padding // 2 - self.line_thickness // 2

        for row_i, row in enumerate(self.grid):

            cell_x = self.cell_padding // 2 + self.line_thickness

            for cell_i, cell in enumerate(row):

                self.draw_walls(cell, cell_x, cell_y)

                cell_x += self.cell_size

            cell_y += self.cell_size

        pr.end_texture_mode()

    def get_cell_coor(self, cell_to_find: Cell) -> tuple[int, int]:

        """
        Calculates the given cell's coordinates on the screen.

        Parameters
        ----------
        cell_to_find: Cell
            The cell for which to calculate its coordinates.

        Returns
        -------
        tuple[int, int]
            Respectively the x and y coordinate of the cell on the screen.
        """

        cell_y = self.map_y + self.cell_padding * 2 - self.line_thickness

        for row_i, row in enumerate(self.grid):

            cell_x = self.map_x + self.cell_padding * 2

            for cell_i, cell in enumerate(row):

                if cell == cell_to_find:
                    return (cell_x, cell_y)

                cell_x += self.cell_size

            cell_y += self.cell_size

        return (-1, -1)

    def display_grid(self) -> None:

        """
        Displays the grid render texture on the screen.
        """

        pr.draw_texture_rec(
            self.grid_texture.texture,
            (
                0,
                0,
                float(self.map_w + self.cell_padding),
                -float(self.map_h + self.cell_padding - self.line_thickness)
            ),
            (self.map_x, self.map_y),
            pr.RAYWHITE
        )

    def display_set_sprites(
        self,
        textures_set: list[tuple[Icon, list[Cell], int]]
    ) -> None:

        """
        Displays the sprites icons set by the user
        when creating their custom map
        (these are the sprites that the user has already placed on the map).

        Parameters
        ----------
        textures_set: list[tuple[Icon, list[Cell], int]]
            A list containing tuples, with respectively
            the sprite icon, all the cells in which it was placed,
            and the size of the icon (entity/collectible/consumable).
        """

        for icon, cells, size in textures_set:

            rect_pad: int = size // 20

            for cell in cells:

                icon.x, icon.y = self.get_cell_coor(cell)
                pr.draw_rectangle(
                    icon.x - rect_pad,
                    icon.y - rect_pad,
                    size + rect_pad * 2,
                    size + rect_pad * 2,
                    pr.GREEN
                )
                icon.display_widget()

    def display_cur_sprite(self, cur_t: Icon, cell: Cell, size: int) -> None:

        """
        Displays the current sprite, which means the one the user
        has selected and is currently choosing a placement for it on the map.

        Parameters
        ----------
        cur_t: Icon
            The current sprite icon the user has selected.
        cell: Cell
            The current cell the sprite is located in.
        size: int
            The size of the icon texture (entity/collectible/consumable).
        """

        rect_pad: int = size // 20

        cur_t.x, cur_t.y = self.get_cell_coor(cell)

        pr.draw_rectangle(
            cur_t.x - rect_pad,
            cur_t.y - rect_pad,
            size + rect_pad * 2,
            size + rect_pad * 2,
            pr.DARKGRAY
        )

        cur_t.display_widget()
