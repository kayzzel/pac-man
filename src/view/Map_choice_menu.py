import pyray as pr
from typing import Callable, Any
from .View import View
from .widget import Widget, Text, ButtonPanel, Icon


ICON_PATHS: dict[str, str] = {
    "MANDATORY": "src/view/assets/icons/placeholder.png",
    "ARCADE": "src/view/assets/icons/pacman_arcade_snapshot.jpg",
    "CUSTOM": "src/view/assets/icons/placeholder.png"
}


class Map_choice_menu(View):

    def _update_title(self) -> None:

        self.title: Text = Text(
            "CHOOSE THE MODE",
            -2,
            self.h // 10,
            self.h // 8
        )
        self.widgets.append(self.title)

    def _update_icons(self) -> None:

        self.icon_width: int = self.w // 5

        height_remaining: int = self.h - self.title.lowerbound
        self.icon_height: int = 2 * (height_remaining // 3)

        self.icon_y: int = self.title.lowerbound + height_remaining // 10
        icon_spacing: int = (self.w - self.icon_width * 3) // 4

        self.icons: dict[str, Icon] = {
            icon_type: Icon(
                i * self.icon_width + (i + 1) * icon_spacing,
                self.icon_y,
                icon_path,
                (self.icon_width, self.icon_height),
                True
            ) for i, (icon_type, icon_path) in enumerate(ICON_PATHS.items())
        }
        self.widgets += list(self.icons.values())

    def _update_panels(self) -> None:

        self.button_actions: dict[str, tuple[Callable, Any]] = {
            "MANDATORY": (self.app.change_view, "game_view"),
            "ARCADE": (self.app.change_view, "game_view"),
            "CUSTOM": (lambda: print(
                "Action for button 'custom' is not yet coded\n"
            ), None)
        }

        self.calculate_panel_spacing()

        self.widgets += [ButtonPanel(
            self.icons[label].posx + (self.icons[label].w - self.panel_width) // 2,
            self.icon_y + (self.icon_height - self.panel_height) // 2,
            self.panel_width,
            self.panel_height,
            {label: action},
            (10, 3, 4.0)
        ) for i, (label, action) in enumerate(self.button_actions.items())
        ]

        back_label: str = "back <-|"
        self.button_actions[back_label] = (
            self.app.return_to_prev_view,
            None
        )

        back_width: int = (
            int(pr.measure_text_ex(Text.font, back_label, self.button_font_sz, Text.spacing).x)
        ) + self.button_font_sz - 5
        back_height: int = self.button_font_sz * 2 - 5

        self.widgets.append(ButtonPanel(
            self.w - back_width - 10,
            self.h - back_height - 10,
            back_width,
            back_height,
            {back_label: self.button_actions[back_label]},
            ((self.button_font_sz - 5)// 2, 2, 0.1)
        ))

    def calculate_panel_spacing(self) -> None:

        max_label: str = max(
            self.button_actions.keys(),
            key=lambda label: len(label)
        )
        self.button_font_sz: int = Text._resize_font(max_label, self.h // 15, self.w // 5)

        self.panel_padding: int = self.button_font_sz + 10
        self.panel_width: int = pr.measure_text(
            max_label,
            self.button_font_sz
        ) + self.panel_padding
        nb_buttons: int = len(self.button_actions.keys())
        width_remaining: int = (
            self.w -
            nb_buttons * self.panel_width
        )

        self.panel_height: int = self.button_font_sz + self.panel_padding

        self.spacing: int = width_remaining // (nb_buttons + 1)

    def _update(self, forced: bool = False) -> Any:

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_icons()
        self._update_panels()
