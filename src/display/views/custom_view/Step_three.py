import pyray as pr

from pyray import MouseButton as mb

from .Custom_step import Custom_step, MSG_TIME
from ..View import View
from ...widgets import Text, Icon, ClickableIcon
from ...Texture_pack import Texture_pack

from src.game.map.Cell import Cell
from src.game.entity.collectible.Consumable import Consumable
from src.game.entity.collectible.Pacgum import Pacgum
from src.game.entity.collectible.Super_Pacgum import Super_Pacgum
from src.utils.enum_utils import Consumable_type


class Step_three(Custom_step):

    """
    A step used for the user to place PacMan's spawn point
    and the different collectibles of the game.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step,
        setting all of the sprites/textures' names,
        and calling the Custom_step's parent method for the other attributes.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self._init_names(main_view)
        self.sprites: list[str] = (
            ["pacman_idle"]
            + self.consumable_names
            + self.collectible_names
        )
        super().__init__(
            3,
            main_view,
            "Place PacMan and the collectibles (at least 1 collectible)"
        )

    def _init_names(self, main_view: View) -> None:

        """
        Initializes all of the textures' names
        that the step is going to use in the display,
        aswell as creating the dictionary containing
        the sprites the user has already placed.

        Parameters
        ----------
        main_view: View
            The main view overseeing every step
            (needed to get the correct texture pack before super().__init__).
        """

        self.texture_pack: Texture_pack = Texture_pack(
            main_view.app.display_config.texture_pack
        )
        self.entity_names: list[str] = [
            "pacman", "blinky", "inky", "pinky", "clyde"
        ]
        self.consumable_names: list[str] = [
            "cherry_c", "galaxian_c", "apple_c", "orange_c",
            "strawberry_c", "key_c", "bell_c", "melon_c"
        ]
        self.collectible_names: list[str] = (
            self.consumable_names
            + ["pacgum", "super_pacgum"]
        )
        self.sprites_set: dict[str, tuple[list[Cell], int]] = {}
        self.current_sprite: str = ""

    @property
    def map_x(self) -> int:

        """
        Gets the correct map start x coordinate
        from the main Custom view.

        Returns
        -------
        int
            The map's already defined start x coordinate.
        """

        return int(self.get_attr("map_x"))

    @property
    def map_y(self) -> int:

        """
        Gets the correct map start y coordinate
        from the main Custom view.

        Returns
        -------
        int
            The map's already defined start y coordinate.
        """

        return int(self.get_attr("map_y"))

    @property
    def map_w(self) -> int:

        """
        Gets the correct map width from the main Custom view.

        Returns
        -------
        int
            The map's already defined width.
        """

        return int(self.get_attr("map_w"))

    @property
    def map_h(self) -> int:

        """
        Gets the correct map height from the main Custom view.

        Returns
        -------
        int
            The map's already defined height.
        """

        return int(self.get_attr("map_h"))

    @property
    def cell_size(self) -> int:

        """
        Gets the correct cell size from the main Custom view.

        Returns
        -------
        int
            The map's already defined cell size.
        """

        return int(self.get_attr("cell_size"))

    def calculate_cell_pos(self, x: int, y: int) -> tuple[int, int] | None:

        """
        Calculates the position on the screen of the given
        cell coordinates (the x and y given being the place of the cell
        inside the grid, not on the screen).

        Parameters
        ----------
        x: int
            The cell's x position inside the grid (col index).
        y: int
            The cell's y position inside the grid (row index).

        Returns
        -------
        tuple[int, int] | None
            If found, the x and y coordinates of the cell (but on the screen),
            None otherwise.
        """

        if x < 0 or x >= self.map.cols:
            return None

        if y < 0 or y >= self.map.rows:
            return None

        return (
            self.map_x + self.cell_size * x,
            self.map_y + self.cell_size * y
        )

    def activate_sprite(self, spr_name: str) -> None:

        """
        Activates the placement mode for the given sprite,
        which means that an icon
        of the current activated sprite will now appear
        under the user's mouse cursor when it hovers over the map,
        allowing the user to simply click where they wish to place it
        for it to become set in the corresponding cell.

        Parameters
        ----------
        spr_name: str
            The name of the sprite to activate.
        """

        if (
            spr_name in self.collectible_names
            and self.map.pacman_spawn_set is False
        ):
            self.show_message = "Please place PacMan before collectibles"
            return

        elif spr_name.startswith("pacman"):
            to_remove: list[str] = [
                t_name for t_name in self.sprites_set.keys()
                if t_name in self.collectible_names
            ]
            for spr in to_remove:
                self.sprites_set.pop(spr)

        self.current_sprite = spr_name

        if spr_name in self.sprites_set.keys():
            self.sprites_set.pop(spr_name)

    def get_consumable_type(self, consumable_name: str) -> Consumable_type:

        """
        Gets the correct Consumable_type from the Enum
        based on the name of the consumable.

        Parameters
        ----------
        consumable_name: str
            The name of the consumable as a string,
            to convert into a Consumable_type.

        Returns
        -------
        Consumable_type
            The member of the type which corresponds to the string name.
            If not found, replaces it with the cherry.
        """

        for cons_type in Consumable_type:
            if cons_type.value == consumable_name:
                return cons_type
        return Consumable_type.CHERRY

    def set_sprite(self, x: int, y: int, spr_name: str) -> bool:

        """
        Determines the correct setting function to call
        based on the sprite's name and type, and returns
        the result of the call (validated or refused).

        Parameters
        ----------
        x: int
            The cell x coordinate in which the sprite has to be set.
        y: int
            The cell y coordinate in which the sprite has to be set.
        spr_name: str
            The name of the sprite to place.

        Returns
        -------
        bool
            True if the placement of this entity/collectible
            inside this cell was possible, False otherwise.
        """

        if spr_name == "pacman_idle":
            return self.map.set_pacman_spawn(x, y)
        elif spr_name in self.consumable_names:
            return self.map.set_collectible(
                x, y, Consumable(
                    self.get_consumable_type(spr_name.removesuffix("_c")),
                    x,
                    y
                )
            )
        elif spr_name == "super_pacgum":
            return self.map.set_collectible(x, y, Super_Pacgum(x, y))
        elif spr_name == "pacgum":
            return self.map.set_collectible(x, y, Pacgum(x, y))
        return False

    def try_place_sprite(self) -> None:

        """
        Attempts to place the current sprite inside the cell
        in which the user has clicked, and storing the sprite
        along with the cell and the proper texture size
        as a tuple inside the 'sprites_set' dictionary,
        to be displayed by the map renderer.
        """

        if not self.current_sprite:
            return

        if self.current_sprite not in self.textures:
            return

        if (
            self.current_sprite in self.sprites_set
            and self.current_sprite not in self.collectible_names
        ):
            return

        cell: Cell | None = self.is_in_cell(
            pr.get_mouse_x(),
            pr.get_mouse_y()
        )
        if not cell:
            return

        if self.set_sprite(cell.pos_x, cell.pos_y, self.current_sprite):

            if (
                self.current_sprite in self.collectible_names
                and self.current_sprite in self.sprites_set.keys()
            ):
                self.sprites_set[self.current_sprite][0].append(cell)
            else:
                self.sprites_set[self.current_sprite] = (
                    [cell],
                    self.texture_size(self.current_sprite)
                )
            if self.current_sprite not in self.collectible_names:
                self.current_sprite = ""

        else:

            self.show_message = "Cannot place here, try elsewhere"

    def texture_size(self, sprite_name: str) -> int:

        """
        Determines the correct texture size for the given sprite
        based on its type (entity/collecible/consumable).

        Parameters
        ----------
        sprite_name: str
            The name of the sprite for which to get the texture size.

        Returns
        -------
        int
            The correct size for the sprite's texture.
        """

        if any(sprite_name.startswith(e_name) for e_name in self.entity_names):
            return self.map_renderer.entity_size
        elif sprite_name in self.consumable_names:
            return self.map_renderer.consumable_size
        elif sprite_name in self.collectible_names:
            return self.map_renderer.collectible_size
        return 0

    def _unload_images(self) -> None:

        """
        Unloads the images and textures of all icons,
        including the grid texture of the map renderer,
        and sets 'is_freed' to True.
        """

        if self.is_freed:
            return

        if hasattr(self, "textures"):
            for icon in self.textures.values():
                icon._unload_image()

        if hasattr(self, "side_textures"):
            for icon in self.side_textures.values():
                icon._unload_image()

        if hasattr(self, "map_renderer"):
            self.map_renderer._unload_images()

        super()._unload_images()

    def _update_textures(self) -> None:

        """
        Builds all the needed icons that will be used
        in the display.
        """

        self.textures: dict[str, Icon] = {
            t_name: Icon(
                0,
                0,
                self.texture_pack.get_texture(t_name),
                (self.texture_size(t_name), self.texture_size(t_name)),
                True
            ) for t_name in (self.sprites + list(self.sprites_set.keys()))
        }
        self._update_sidetextures()

    def _update_sidetextures(self) -> None:

        """
        Builds the side icons that the user can click on
        to activate the placement mode for a specific sprite.
        """

        side_text_sz: int = (
            self.map_h // (len(self.collectible_names) // 2 + 1)
        )
        t_pad: int = self.map_h // 50
        side_text_sz = min(side_text_sz - t_pad * 2, self.map_x * 3 // 4)

        pacman_icon: ClickableIcon = ClickableIcon(
            (self.map_x - side_text_sz) // 2,
            self.map_y + t_pad,
            self.texture_pack.get_texture("pacman_idle"),
            (self.activate_sprite, "pacman_idle"),
            (side_text_sz, side_text_sz),
            True,
            False
        )

        w_rem: int = self.map_x - side_text_sz * 2
        fst_x: int = w_rem // 5 * 2
        scd_x: int = fst_x + side_text_sz + w_rem // 5

        self.side_textures: dict[str, ClickableIcon] = {
            "pacman_idle": pacman_icon
        }

        t_x: int = fst_x
        t_y: int = self.map_y + (t_pad + side_text_sz) * 2

        for i, t_name in enumerate(self.collectible_names):

            if i == len(self.collectible_names) // 2:
                t_x = scd_x
                t_y = self.map_y + (t_pad + side_text_sz) * 2

            self.side_textures[t_name] = ClickableIcon(
                t_x,
                t_y,
                self.texture_pack.get_texture(t_name),
                (self.activate_sprite, t_name),
                (side_text_sz, side_text_sz),
                True,
                False
            )
            t_y += side_text_sz + t_pad

    def display_textures(self) -> None:

        """
        Displays all the icons (set sprites, side icons, grid texture, etc).
        """

        self.map_renderer.display_set_sprites([
            (self.textures[spr_name], cells, size)
            for spr_name, (cells, size) in self.sprites_set.items()
        ])

        for side_texture in self.side_textures.values():
            side_texture.display_widget()

        if self.current_sprite:

            cell: Cell | None = self.is_in_cell(
                pr.get_mouse_x(),
                pr.get_mouse_y()
            )
            if not cell:
                return

            self.map_renderer.display_cur_sprite(
                self.textures[self.current_sprite],
                cell,
                self.texture_size(self.current_sprite)
            )

    def display_message(self) -> None:

        """
        Displays a message under the map if needed,
        for example if the user doesn't place the sprites
        in order.
        """

        if self.frame_counter < MSG_TIME:

            msg_h: int = self.h - (
                self.map_y + self.map_h
            )
            message: Text = Text(
                self.show_message,
                -2,
                self.map_y + self.map_h + (msg_h - msg_h // 2) // 2,
                msg_h // 2,
                self.map_w,
                pr.RED
            )
            message.display_widget()
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.frame_counter = 0

    def check_next(self) -> None:

        """
        Checks whether or not PacMan's spawn point
        has been set, aswell as at least one collectible,
        which allows the 'next' button to be shown to the user.
        """

        self.show_next = (
            self.map.pacman_spawn_set
            and self.map.map.collectible_count > 0
        )

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the user can go to the next step,
        if the user has clicked somewhere (trying to place a sprite),
        if the window has been resized or an update is required,
        and updates the textures/icons if so.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        self.check_next()

        if pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT):
            self.try_place_sprite()

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self.map_renderer.update_special_grid(
            self.map.map.cells,
            (self.map_w, self.map_h),
            (self.map_x, self.map_y),
            self.cell_size
        )
        self._update_textures()

    def display_view(self) -> None:

        """
        Updates and displays the step, mainly the grid
        and sprites via the map renderer.
        """

        super().display_view()

        self.map_renderer.display_grid()
        self.display_textures()
