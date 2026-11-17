import pyray as pr

from pyray import KeyboardKey as kek
from typing import Callable, Any

from .View import View
from .Texture_pack import Texture_pack, TEXTURES_PACK
from .widget import (
    Text,
    ButtonPanel,
    Dropdown,
    TextPanel,
    Keybind_input_box,
    AnimIcon
)


class Options_menu(View):

    """
    A view that presents the different configuration options
    for the user to select and choose from
    (keybinds, graphics, font, texture pack, etc).
    """

    def _update_title(self) -> None:

        """
        Builds the view's title widget.
        """

        self.title: Text = Text(
            "OPTIONS",
            -2,
            self.h // 15,
            self.h // 10
        )
        self.widgets.append(self.title)

    def change_keybind(self, keybind: str) -> None:

        """
        Changes the keybind that the user entered (if valid)
        in the app's display configuration.

        Parameters
        ----------
        keybind: str
            The name of the keybind to change.
        """

        correct_keybind: str = keybind.split(" ")[0]
        if correct_keybind not in self.app.display_config.keybinds.keys():
            return
        self.app.display_config.keybinds[correct_keybind] = (
            self.keybind_input[correct_keybind].display_key
        )
        self._update(True)

    def change_font(self, font: str) -> None:

        """
        Loads a new font for the display text.

        Parameters
        ----------
        font: str
            The new font to load.
        """

        Text._load_font(font)
        self._update(True)

    def change_resolution(self, res: str) -> None:

        """
        Changes the game window's resolution
        based on the user's choice.

        Parameters
        ----------
        res: str
            The new resolution of the game's window.
        """

        if res == "fullscreen":
            pr.toggle_fullscreen()

        elif res == "1080p" or res == "720p":

            if pr.is_window_fullscreen():
                pr.toggle_fullscreen()

            if res == "1080p":
                width: int = 1920
                height: int = 1080

            elif res == "720p":
                width = 1240
                height = 720

            pr.set_window_size(width, height)

        self._update(True)

    def change_texture_pack(self, new_pack: str) -> None:

        """
        Changes the texture pack used in the game.

        Parameters
        ----------
        new_pack: str
            The path to the texture pack to use.
        """

        if new_pack not in TEXTURES_PACK.keys():
            return

        self.app.display_config.texture_pack = TEXTURES_PACK[new_pack]
        self._update(True)

    def get_key_equivalent(self, keybind: kek) -> str:

        """
        Determines the right 'name' for a specific keybind,
        mostly to return 'arrow up/down/left/right' instead of their chr.

        Parameters
        ----------
        keybind: pyray.KeyboardKey
            The keybind for which to return its 'name'.

        Returns
        -------
        str
            The 'name' or label for the keybind.
        """

        if keybind not in [
            kek.KEY_DOWN, kek.KEY_UP, kek.KEY_LEFT, kek.KEY_RIGHT
        ]:
            return chr(keybind)

        direction: str = ""
        match keybind:
            case kek.KEY_DOWN:
                direction = "down"
            case kek.KEY_UP:
                direction = "up"
            case kek.KEY_LEFT:
                direction = "left"
            case kek.KEY_RIGHT:
                direction = "right"
        return ("arrow " + direction)

    def _update_keybinds(self) -> None:

        """
        Builds the keybind option panel,
        with the four keybind input boxes for the user
        to change the keybinds associated with each move.
        """

        self.p_w: int = self.w // 2
        self.title_fontsz: int = self.h // 20

        self.keybind_title: Text = Text(
            "KEYBINDS",
            (self.p_w - Text.measure_text("KEYBINDS", self.title_fontsz)) // 2,
            self.title.lowerbound + self.h // 15,
            self.title_fontsz
        )
        self.keybind_panel: TextPanel = TextPanel(
            self.keybind_title.posx - self.w // 20,
            self.keybind_title.lowerbound + self.h // 25,
            self.keybind_title.width,
            self.h // 5,
            [
                f"{key} ({self.get_key_equivalent(value)})"
                for key, value
                in self.app.display_config.keybinds.items()
            ]
        )
        keybind_range: list[int] = [
            keycode for keycode in range(32, 126)
        ] + [kek.KEY_DOWN, kek.KEY_UP, kek.KEY_LEFT, kek.KEY_RIGHT]

        self.keybind_input: dict[str, Keybind_input_box] = {
            keybind: Keybind_input_box(
                (
                    self.keybind_panel.posx
                    + self.keybind_panel.w
                    + self.keybind_panel.w // 10
                ),
                self.keybind_panel.labels[
                    f"{keybind} ({self.get_key_equivalent(value)})"
                ].posy,
                self.keybind_title.width // 3,
                self.keybind_panel.font_size,
                (self.change_keybind, keybind),
                1,
                keybind_range
            ) for keybind, value in self.app.display_config.keybinds.items()
        }
        self.widgets += [self.keybind_title, self.keybind_panel]
        self.widgets += list(self.keybind_input.values())

    def _update_graphics(self) -> None:

        """
        Builds the graphics option panel, where the user
        can choose the game window's resolution.
        """

        self.graphics_title: Text = Text(
            "GRAPHICS",
            (self.p_w - Text.measure_text("GRAPHICS", self.title_fontsz)) // 2,
            self.keybind_panel.posy + self.keybind_panel.h + self.h // 15,
            self.title_fontsz
        )

        res_buttons: dict[
            str,
            tuple[Callable[..., Any], Any]
        ] = {
            "Screen dimensions": (lambda: 0, None)
        } | {
            res: (self.change_resolution, res)
            for res in ["fullscreen", "1080p", "720p"]
        }
        res_w: int = self.p_w // 2

        self.res_dropdown: Dropdown = Dropdown(
            (self.p_w - res_w) // 2,
            self.graphics_title.lowerbound + self.h // 25,
            res_w,
            self.graphics_title.font_size,
            res_buttons
        )
        self.widgets += [
            self.graphics_title,
            self.res_dropdown
        ]

    def _update_back_button(self) -> None:

        """
        Builds the back button for the view.
        """

        back_label: str = "back <-|"
        back_width: int = self.w // 8
        back_height: int = self.h // 15

        self.back_button: ButtonPanel = ButtonPanel(
            self.w - back_width - self.w // 25,
            self.h - back_height - self.h // 40,
            back_width,
            back_height,
            {back_label: (self.app.return_to_prev_view, None)}
        )
        self.widgets.append(self.back_button)

    def _update_font_choice(self) -> None:

        """
        Builds the font option panel, where the user
        can select which font they want to use for the whole display text.
        """

        self.font_title: Text = Text(
            "FONT",
            self.p_w + (
                self.p_w - Text.measure_text("FONT", self.title_fontsz)
            ) // 2,
            self.keybind_title.posy,
            self.title_fontsz,
            self.w // 3
        )

        font_buttons: dict[
            str,
            tuple[Callable[..., Any], Any]
        ] = {
            f"Select font (current: {Text.current_font})": (lambda: 0, None)
        } | {
            font: (self.change_font, font)
            for font in Text.fonts.keys()
        }
        font_drdw_w: int = self.p_w - self.p_w // 3

        self.font_dropdown: Dropdown = Dropdown(
            self.p_w + (self.p_w - font_drdw_w) // 2,
            self.font_title.lowerbound + self.h // 25,
            font_drdw_w,
            self.font_title.font_size,
            font_buttons
        )

    def _update_texture_pack(self) -> None:

        """
        Builds the texture pack option panel,
        with the dropdown showing the available texture packs,
        and a small preview of two sprites of the current texture pack
        (PacMan and Blinky Ghost).
        """

        self.texture_title: Text = Text(
            "TEXTURES",
            self.p_w + (
                self.p_w - Text.measure_text("TEXTURES", self.title_fontsz)
            ) // 2,
            self.font_dropdown.posy + self.font_dropdown.h + self.h // 15,
            self.title_fontsz,
            self.w // 3
        )

        current_pack: str = "DEFAULT"
        for k, v in TEXTURES_PACK.items():
            if v == self.app.display_config.texture_pack:
                current_pack = k
                break

        texture_buttons: dict[
            str,
            tuple[Callable[..., Any], Any]
        ] = {
            f"Select texture pack (current: {current_pack})": (lambda: 0, None)
        } | {
            pack: (self.change_texture_pack, pack)
            for pack in TEXTURES_PACK.keys()
        }
        text_drdw_w: int = self.p_w - self.p_w // 3

        self.txt_dropdown: Dropdown = Dropdown(
            self.p_w + (self.p_w - text_drdw_w) // 2,
            self.texture_title.lowerbound + self.h // 25,
            text_drdw_w,
            self.texture_title.font_size,
            texture_buttons
        )

        self.preview_label: Text = Text(
            "PREVIEW : ",
            self.p_w,
            self.txt_dropdown.posy + self.txt_dropdown.h + self.h // 15,
            self.title_fontsz
        )

        h_rem: int = self.h - (
            self.preview_label.lowerbound + self.back_button.h + self.h // 15
        )
        h_rem -= h_rem // 4
        start_x: int = (self.p_w - h_rem * 2 - self.p_w // 8) // 2

        texture_pack: Texture_pack = Texture_pack(
            self.app.display_config.texture_pack
        )
        self.preview_icon_pacman: AnimIcon = AnimIcon(
            self.p_w + start_x,
            self.preview_label.lowerbound + self.h // 25,
            texture_pack.get_texture("pacman_right"),
            (h_rem, h_rem),
            True
        )
        self.preview_icon_ghost: AnimIcon = AnimIcon(
            self.preview_icon_pacman.posx + h_rem + self.p_w // 8,
            self.preview_label.lowerbound + self.h // 25,
            texture_pack.get_texture("blinky_left"),
            (h_rem, h_rem),
            True
        )
        self.widgets += [
            self.texture_title,
            self.preview_label,
            self.preview_icon_pacman,
            self.preview_icon_ghost,
            self.txt_dropdown
        ]
        self.widgets += [self.font_title, self.font_dropdown]

    def _update(self, forced: bool = False) -> None:

        """
        Updates the menu, checking if the window has been resized,
        and re-building the widgets if needed.

        Parameters
        ----------
        forced: bool (default False)
            Whether or not the view MUST be updated.
        """

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_title()
        self._update_back_button()
        self._update_keybinds()
        self._update_graphics()
        self._update_font_choice()
        self._update_texture_pack()
