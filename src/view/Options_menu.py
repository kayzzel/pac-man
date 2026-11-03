import pyray as pr
from pyray import KeyboardKey as kek
from .View import View
from .Texture_pack import Texture_pack, TEXTURES_PACK
from .widget import Widget, Text, ButtonPanel, Dropdown, TextPanel, Input_box, Keybind_input_box, AnimIcon
from typing import Callable, Any


class Options_menu(View):

    def _update_title(self) -> None:

        self.title: Text = Text(
            "OPTIONS",
            -2,
            self.h // 15,
            self.h // 10
        )
        self.widgets.append(self.title)

    def change_keybind(self, keybind: str) -> None:

        if keybind not in self.app.display_config.keybinds.keys():
            return
        self.app.display_config.keybinds[keybind] = self.keybind_input[keybind].display_key
        self._update(True)

    def _update_keybinds(self) -> None:

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
            list(self.app.display_config.keybinds.keys())
        )
        keybind_range: list[int] = [
            keycode for keycode in range(32, 126)
        ] + [kek.KEY_DOWN, kek.KEY_UP, kek.KEY_LEFT, kek.KEY_RIGHT]
        self.keybind_input: dict[str, Keybind_input_box] = {
            keybind: Keybind_input_box(
                self.keybind_panel.posx + self.keybind_panel.w + self.keybind_panel.w // 10,
                self.keybind_panel.labels[keybind].posy,
                self.keybind_title.width // 2,
                self.keybind_panel.font_size,
                (self.change_keybind, keybind),
                1,
                keybind_range
            ) for keybind in list(self.app.display_config.keybinds.keys())
        }
        self.widgets += [self.keybind_title, self.keybind_panel]
        self.widgets += list(self.keybind_input.values())

    def change_resolution(self, res: str) -> None:

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

    def change_fps(self) -> None:

        if not self.fps_input.input.isdigit():
            return
        self.app.display_config.fps_max = int(self.fps_input.input)
        self._update(True)

    def _update_graphics(self) -> None:

        self.graphics_title: Text = Text(
            "GRAPHICS",
            (self.p_w - Text.measure_text("GRAPHICS", self.title_fontsz)) // 2,
            self.keybind_panel.posy + self.keybind_panel.h + self.h // 15,
            self.title_fontsz
        )
        res_buttons: dict[str, tuple[Callable, Any]] = {
            "Screen dimensions": (lambda: 0, None)
        } | {
            res: (self.change_resolution, res)
            for res in ["fullscreen", "1080p", "720p"]
        }
        res_w: int = self.p_w // 2
        self.resolution_dropdown: Dropdown = Dropdown(
            (self.p_w - res_w) // 2,
            self.graphics_title.lowerbound + self.h // 25,
            res_w,
            self.graphics_title.font_size,
            res_buttons
        )
        fps_string: str = f"FPS max ({self.app.display_config.fps_max})"
        fps_input_sz: int = self.resolution_dropdown.w // 5 + self.resolution_dropdown.w // 8
        self.fps_label: Text = Text(
            f"FPS max ({self.app.display_config.fps_max})",
            self.resolution_dropdown.posx + (
                self.resolution_dropdown.w
                - Text.measure_text(fps_string, self.resolution_dropdown.main_panel.font_size)
                - fps_input_sz
            ) // 2,
            self.resolution_dropdown.posy + self.resolution_dropdown.h + self.h // 25,
            self.resolution_dropdown.main_panel.font_size,
            self.resolution_dropdown.w - fps_input_sz
        )
        self.fps_input: Input_box = Input_box(
            self.fps_label.posx + self.fps_label.width + self.resolution_dropdown.w // 16,
            self.fps_label.posy,
            self.resolution_dropdown.w // 5,
            self.graphics_title.font_size,
            (self.change_fps, None),
            4,
            (48, 57)
        )
        self.widgets += [self.graphics_title, self.fps_label, self.fps_input, self.resolution_dropdown]

    def _update_back_button(self) -> None:

        back_label: str = "back <-|"
        button_font_sz: int = self.h // 20
        button_padding: int = button_font_sz - 5

        back_width: int = Text.measure_text(back_label, button_font_sz) + button_padding
        button_height: int = button_font_sz + button_padding

        self.back_button: ButtonPanel = ButtonPanel(
            self.w - back_width - 10,
            self.h - button_height - 10,
            back_width,
            button_height,
            {back_label: (self.app.return_to_prev_view, None)},
            (button_padding // 2, 2, 0.1)
        )
        self.widgets.append(self.back_button)

    def change_texture_pack(self, new_pack: str) -> None:

        if new_pack not in TEXTURES_PACK.keys():
            return

        self.app.display_config.texture_pack = TEXTURES_PACK[new_pack]
        self._update(True)

    def _update_texture_pack(self) -> None:

        self.texture_title: Text = Text(
            "TEXTURES",
            self.p_w + (self.p_w - Text.measure_text("TEXTURES", self.title_fontsz)) // 2,
            self.keybind_title.posy,
            self.title_fontsz,
            self.w // 3
        )
        current_pack: str = "DEFAULT"
        for k, v in TEXTURES_PACK.items():
            if v == self.app.display_config.texture_pack:
                current_pack = k
                break
        texture_buttons: dict[str, tuple[Callable, Any]] = {
            f"Select texture pack (current: {current_pack})": (lambda: 0, None)
        } | {
            pack: (self.change_texture_pack, pack)
            for pack in TEXTURES_PACK.keys()
        }
        text_drdw_w: int = self.p_w - self.p_w // 3
        self.texture_dropdown: Dropdown = Dropdown(
            self.p_w + (self.p_w - text_drdw_w) // 2,
            self.texture_title.lowerbound + self.h // 25,
            text_drdw_w,
            self.texture_title.font_size,
            texture_buttons
        )
        self.preview_label: Text = Text(
            "PREVIEW : ",
            self.p_w,
            self.texture_dropdown.posy + self.texture_dropdown.h + self.h // 15,
            self.title_fontsz
        )
        height_remaining: int = self.h - (self.preview_label.lowerbound + self.back_button.h + self.h // 15)
        height_remaining -= height_remaining // 4
        start_x: int = (self.p_w // 2 - height_remaining) // 2
        self.preview_icon_pacman: AnimIcon = AnimIcon(
            self.p_w + start_x,
            self.preview_label.lowerbound + self.h // 15,
            Texture_pack(self.app.display_config.texture_pack).get_texture("pacman_right"),
            (height_remaining, height_remaining),
            True
        )
        self.preview_icon_ghost: AnimIcon = AnimIcon(
            self.p_w + self.p_w // 2 + start_x,
            self.preview_label.lowerbound + self.h // 15,
            Texture_pack(self.app.display_config.texture_pack).get_texture("blinky_left"),
            (height_remaining, height_remaining),
            True
        )
        self.widgets += [self.texture_title, self.preview_label, self.preview_icon_pacman, self.preview_icon_ghost, self.texture_dropdown]

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_back_button()
        self._update_keybinds()
        self._update_graphics()
        self._update_texture_pack()
