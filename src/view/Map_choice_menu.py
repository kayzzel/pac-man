import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from typing import Callable, Any
from .View import View
from .widget import Panel, OvalPanel, RectPanel


BUTTON_FONT_SIZE: int = 20
ELLIPSE_PANEL_PADDING: int = BUTTON_FONT_SIZE + 10
RECT_PANEL_PADDING: int = BUTTON_FONT_SIZE - 5


class Map_choice_menu(View):

    def _update_title(self) -> None:

        self.title: str = "CHOOSE THE MAP"
        self.title_font_sz: int = self.h // 8
        self.title_width: int = pr.measure_text(
            self.title,
            self.title_font_sz
        )

    def _update_panels(self) -> None:

        self.button_actions: dict[str, tuple[Callable, Any]] = {
            "MANDATORY": (self.app.change_view, "game_view"),
            "ARCADE": (self.app.change_view, "game_view"),
            "CUSTOM": (lambda: print(
                "Action for button 'custom' is not yet coded\n"
            ), None)
        }

        self.calculate_panel_spacing()

        self.panels: list[Panel] = [OvalPanel(
            self.spacing * (i + 1) + self.panel_width * i,
            -2,
            self.panel_width,
            BUTTON_FONT_SIZE + ELLIPSE_PANEL_PADDING,
            {label: action},
            BUTTON_FONT_SIZE,
            ELLIPSE_PANEL_PADDING
        ) for i, (label, action) in enumerate(self.button_actions.items())
        ]

        back_label: str = "back <-|"
        self.button_actions[back_label] = (
            self.app.return_to_prev_view,
            None
        )

        back_width: int = (
            pr.measure_text(back_label, BUTTON_FONT_SIZE)
        ) + RECT_PANEL_PADDING
        back_height: int = BUTTON_FONT_SIZE + RECT_PANEL_PADDING

        self.panels.append(RectPanel(
            self.w - back_width - 10,
            self.h - back_height - 10,
            back_width,
            back_height,
            {back_label: self.button_actions[back_label]},
            BUTTON_FONT_SIZE,
            RECT_PANEL_PADDING
        ))

    def calculate_panel_spacing(self) -> None:

        max_label: str = max(
            self.button_actions.keys(),
            key=lambda label: len(label)
        )

        self.panel_width: int = pr.measure_text(
            max_label,
            BUTTON_FONT_SIZE
        ) + ELLIPSE_PANEL_PADDING
        nb_buttons: int = len(self.button_actions.keys())
        width_remaining: int = (
            self.w -
            nb_buttons * self.panel_width
        )

        self.spacing: int = width_remaining // (nb_buttons + 1)

    # def update(self) -> Any:

    #     buttons: list[Button] = []
    #     for panel in self.panels:
    #         buttons += list(panel.buttons.values())

    #     for button in buttons:

    #         if button.is_pressed:
    #             button.call_action()

    def display_view(self) -> None:

        self._update_title()
        self._update_panels()

        pr.draw_text(
            self.title,
            (self.w - self.title_width) // 2,
            20,
            self.title_font_sz,
            pr.RAYWHITE
        )
        for panel in self.panels:
            panel.display_widget()
