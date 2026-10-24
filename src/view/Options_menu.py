import pyray as pr
from .View import View
from .widget import Widget, Text, ButtonPanel, Dropdown
from typing import Callable, Any


class Options_menu(View):

    def __init__(self, app) -> None:

        super().__init__(app)

    def _update_title(self) -> None:

        self.title: Text = Text(
            "OPTIONS",
            -2,
            self.h // 15,
            self.h // 10
        )
        self.widgets.append(self.title)

    def _update_options(self) -> None:

        buttons: dict[str, tuple[Callable, Any]] = {
            "read instructions": (self.app.change_view, Instructions_view(self.app))
        }
        dropdown_buttons: dict[str, tuple[Callable, Any]] = {
            texture_path: (self.change_texture_pack, texture_path)
            for texture_path in ["src/view/assets/default_texture_pack", "src/view/assets/luigi_texture_pack"]
        }
        self.options_panel: ButtonPanel = ButtonPanel(
            -2,
            self.title.y + self.title.font_size + self.h // 15,
            self.w // 3,
            self.h // 3,
            buttons
        )
        self.texture_dropdown: Dropdown = Dropdown(
            -2,
            self.options_panel.y + self.options_panel.h - self.options_panel.padding,
            self.w // 3,
            self.options_panel.font_size * 2,
            dropdown_buttons
        )
        self.back_button: ButtonPanel = ButtonPanel(
            -2,
            self.texture_dropdown.y + self.texture_dropdown.h,
            self.w // 3,
            self.options_panel.font_size * 2,
            {"go back to main menu": (self.app.return_to_prev_view, None)}
        )
        self.widgets += [self.options_panel, self.texture_dropdown, self.back_button]

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_options()
