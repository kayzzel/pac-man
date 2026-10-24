import pyray as pr
from .View import View
from .view.Texture_pack import Texture_pack, TEXTURES_PACK
from .widget import Widget, Text, ButtonPanel, Dropdown, TextPanel, Input_box, AnimIcon
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
        self.app.display_config.keybinds[keybind] = self.keybind_input[keybind].key

    def _update_keybinds(self) -> None:

        self.keybind_title: Text = Text(
            "KEYBINDS",
            self.w // 10,
            self.title.y + self.title.font_size + self.h // 15,
            self.h // 25
        )
        self.keybind_panel: TextPanel = TextPanel(
            self.keybind_title.posx,
            self.keybind_title.h + self.keybind_title.font_size,
            2 * self.keybind_title.width // 3,
            self.h // 30,
            list(self.app.display_config.keybinds.keys())
        )
        self.keybind_input: dict[str, Input_box] = {
            keybind: Input_box(
                self.keybind_panel.posx + self.keybind_panel.w + self.keybind_panel.w // 10,
                self.keybing_panel.labels[keybind].posy,
                self.keybind_title.width // 3 - self.keybind_panel.width // 5,
                self.keybind_panel.font_size,
                (self.change_keybind, keybind),
                1
            ) for keybind in list(self.app.display_config.keys())
        }
        self.widgets += [self.keybind_title, self.keybind_panel, self.keybind_input]

    def change_resolution(self, res: str) -> None:

        if res == "fullscreen":
            if not pr.is_window_fullscreen():
                pr.toggle_fullscreen()
            return

        if res == "1080p":
            pr.set_window_size(1920, 1080)

        elif res == "720p":
            pr.set_window_size(1240, 720)

    def change_fps(self) -> None:

        if not self.fps_input.input.is_digit():
            return
        self.app.display_config.fps_max = int(self.fps_input.input)

    def _update_graphics(self) -> None:

        self.graphics_title: Text = Text(
            "GRAPHICS",
            self.keybind_title.posx,
            self.keybind_panel.posy + self.keybind_panel.h + self.h // 15,
            self.h // 25
        )
        res_buttons: dict[str, tuple[Callable, Any]] = {
            "Change screen dimensions": (lambda: 0, None)
        } | {
            res: (self.change_resolution, res)
            for res in ["fullscreen", "1080p", "720p"]
        }
        self.resolution_dropdown: Dropdown = Dropdown(
            self.graphics_title.posx,
            self.graphics_title.posy + self.graphics_title.font_size + self.h // 25,
            self.graphics_title.width,
            self.graphics_title.font_size,
            res_buttons
        )
        self.fps_label: Text = Text(
            f"FPS max ({self.app.display_config.fps_max})",
            self.graphics_title.posx,
            self.resolution_dropdown.posy + self.resolution_dropdown.h + self.h // 25,
            self.resolution_dropdown.panel.font_size,
            self.graphics_title.width // 2
        )
        self.fps_input: Input_box = Input_box(
            self.fps_label.posx + self.graphics_title.width // 2 + self.graphics_title.width // 10,
            self.fps_label.posy,
            self.graphics_title // 2 - self.graphics_title // 5,
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

        back_width: int = (
            int(pr.measure_text_ex(Text.font, back_label, button_font_sz, Text.spacing).x)
        ) + button_padding
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

    def _update_texture_pack(self) -> None:

        self.texture_title: Text = Text(
            "TEXTURES",
            self.w // 3 * 2,
            self.keybind_title.posy,
            self.keybind_title.font_size,
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
        self.texture_dropdown: Dropdown = Dropdown(
            self.texture_title.posx,
            self.texture_title.posy + self.texture_title.font_size + self.h // 25,
            self.w // 3,
            self.texture_title.font_size,
            texture_buttons
        )
        self.preview_label: Text(
            "PREVIEW : ",
            self.texture_dropdown.posx,
            self.texture_dropdown.posy + self.texture_dropdown.h + self.h // 5,
            self.texture_title.font_size
        )
        height_remaining: int = self.h - (self.preview_label.posy + self.preview_label.font_size + self.back_button.h)
        height_remaining -= height_remaining // 4
        self.preview_icon_pacman: AnimIcon = AnimIcon(
            self.preview_label.posx + self.w // 10,
            self.preview_label.posy + self.preview_label.font_size + self.h // 15,
            Texture_pack(self.app.display_config.texture_pack).get_texture("pacman_right"),
            (height_remaining, height_remaining),
            True
        )
        self.preview_icon_ghost: AnimIcon = AnimIcon(
            self.preview_icon_pacman.posx + self.preview_icon_pacman.image.width + self.w // 10,
            self.preview_label.posy + self.preview_label.font_size + self.h // 15,
            Texture_pack(self.app.display_config.texture_pack).get_texture("clyde_left"),
            (height_remaining, height_remaining),
            True
        )
        self.widgets += [self.texture_title, self.preview_label, self.preview_icon_pacman, self.preview_icon_ghost, self.texture_dropdown]

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_keybinds()
        self._update_graphics()
        self._update_texture_pack()
