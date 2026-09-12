import pyray as pr
from typing import Callable, Any
from .View import View
from .widget.Panel import OvalPanel, RectPanel
from .widget.Button import Button


BUTTON_FONT_SIZE: int = 20
ELLIPSE_PANEL_PADDING: int = BUTTON_FONT_SIZE + 10
RECT_PANEL_PADDING: int = BUTTON_FONT_SIZE - 5


class Map_choice_menu(View):

    def __init__(self) -> None:

        self._init_panels()
        self.title: str = "CHOOSE THE MAP"
        self.title_font_sz: int = pr.get_screen_height() // 8
        self.title_width: int = pr.measure_text(
            self.title,
            self.title_font_sz
        )

    def _init_panels(self) -> None:

        self.panels: list[OvalPanel] = []

        self.button_actions: dict[str, Callable] = {
            "MANDATORY": (lambda: print(
                "Action for button 'mandatory' is not yet coded\n"
            )),
            "ARCADE": (lambda: print(
                "Action for button 'arcade' is not yet coded\n"
            )),
            "CUSTOM": (lambda: print(
                "Action for button 'custom' is not yet coded\n"
            ))
        }

        self.calculate_panel_spacing()

        self.panels: list[OvalPanel] = [OvalPanel(
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
        self.button_actions[back_label] = (lambda: "main_menu")

        back_width: int = (
            pr.measure_text(back_label, BUTTON_FONT_SIZE)
        ) + RECT_PANEL_PADDING
        back_height: int = BUTTON_FONT_SIZE + RECT_PANEL_PADDING

        self.panels.append(RectPanel(
            pr.get_screen_width() - back_width - 10,
            pr.get_screen_height() - back_height - 10,
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
            pr.get_screen_width() -
            nb_buttons * self.panel_width
        )

        self.spacing: int = width_remaining // (nb_buttons + 1)

    def update(self) -> Any:

        buttons: list[Button] = []
        for panel in self.panels:
            buttons += list(panel.buttons.values())

        for button in buttons:

            if button.is_pressed:
                return button.action()

    def display_view(self) -> None:

        pr.draw_text(
            self.title,
            (pr.get_screen_width() - self.title_width) // 2,
            20,
            self.title_font_sz,
            pr.RAYWHITE
        )
        for panel in self.panels:
            panel.display_widget()
