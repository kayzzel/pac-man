from .Step_three import Step_three
from ..View import View
from ...widgets import ClickableIcon


class Step_four(Step_three):

    """
    A step used for the user to place the Ghosts' spawn and scatter points.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step,
        setting all of the sprites/textures' names,
        getting the previous view's already placed sprites via the main view,
        and calling the Custom_step's parent method for the other attributes.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self._init_names(main_view)
        self.spawn_sprites: list[str] = [
            en_name + "_idle"
            for en_name in self.entity_names
            if en_name != "pacman"
        ]
        self.scatter_sprites: list[str] = [
            en_name + "_scatter"
            for en_name in self.entity_names
            if en_name != "pacman"
        ]
        self.sprites: list[str] = self.spawn_sprites + self.scatter_sprites
        if hasattr(main_view, "steps_completed"):
            for step in main_view.steps_completed:
                if step.number == 3 and isinstance(step, Step_three):
                    self.sprites_set = {
                        k: val for k, val in step.sprites_set.items()
                    }

        super(Step_three, self).__init__(
            4,
            main_view,
            "Place the Ghosts spawn and scatter points (spawn first)"
        )

    def activate_sprite(self, spr_name: str) -> None:

        """
        Activates the placement mode for the given sprite,
        which means that an icon
        of the current activated sprite will now appear
        under the user's mouse cursor when it hovers over the map,
        allowing the user to simply click where they wish to place it
        for it to become set in the corresponding cell.
        Also sets the 'show_message' value to display a refusal message
        in case the user tries to place the scatter before the spawn points.

        Parameters
        ----------
        spr_name: str
            The name of the sprite to activate.
        """

        if (
            spr_name in self.scatter_sprites
            and not all(self.map.ghost_spawn_set.values())
        ):
            self.show_message = (
                "Place the spawn points of all ghosts first"
            )
            return

        self.current_sprite = spr_name

        if spr_name in self.sprites_set.keys():
            self.sprites_set.pop(spr_name)

    def set_sprite(self, x: int, y: int, spr_name: str) -> bool:

        """
        Determines the correct setting function to call
        based on the sprite's name (spawn/scatter), and returns
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
            True if the placement of this ghost spawn/scatter
            inside this cell was possible, False otherwise.
        """

        if spr_name in self.spawn_sprites:
            return self.map.set_ghost_spawn(
                x, y, spr_name.removesuffix("_idle").upper()
            )
        elif spr_name in self.scatter_sprites:
            return self.map.set_ghost_scatter(
                x, y, spr_name.removesuffix("_scatter").upper()
            )
        return False

    def _update_sidetextures(self) -> None:

        """
        Builds the side icons that the user can click on
        to activate the placement mode for a specific sprite.
        """

        side_text_sz: int = self.map_h // (len(self.sprites) // 2)
        t_pad: int = self.map_h // 50
        side_text_sz = min(side_text_sz - t_pad * 2, self.map_x * 3 // 4)
        fst_t_x: int = (self.map_x - side_text_sz * 2 - side_text_sz // 2) // 2
        scd_t_x: int = fst_t_x + side_text_sz + side_text_sz // 2

        self.side_textures: dict[str, ClickableIcon] = {
            t_name: ClickableIcon(
                fst_t_x,
                self.map_y + i * (side_text_sz + t_pad * 2) + t_pad,
                self.texture_pack.get_texture(t_name),
                (self.activate_sprite, t_name),
                (side_text_sz, side_text_sz),
                True,
                False
            ) for i, t_name in enumerate(self.spawn_sprites)
        } | {
            t_name: ClickableIcon(
                scd_t_x,
                self.map_y + i * (side_text_sz + t_pad * 2) + t_pad,
                self.texture_pack.get_texture(t_name),
                (self.activate_sprite, t_name),
                (side_text_sz, side_text_sz),
                True,
                False
            ) for i, t_name in enumerate(self.scatter_sprites)
        }

    def check_next(self) -> None:

        """
        Checks whether or not all of the Ghosts' spawn/scatter points
        has been set, which allows the 'next' button to be shown to the user.
        """

        self.show_next = (
            all(self.map.ghost_spawn_set.values())
            and all(self.map.ghost_scatter_set.values())
        )
