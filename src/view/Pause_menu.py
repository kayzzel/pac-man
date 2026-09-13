import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from typing import Callable, Any
from .View import View
from .widget.Panel import RectPanel


BUTTON_FONT_SIZE: int = 20
PANEL_PADDING: int = BUTTON_FONT_SIZE - 5


class Pause_menu(View):

    def __init__(self) -> None:

        self.w: int = sw() - sw() // 8
        self.h: int = sh() - sh() // 8
        self.x: int = (sw() - self.w) // 2
        self.y: int = (sh() - self.h) // 2
        self._init_left_panel()

    def _init_left_panel(self) -> None:

        self.button_actions: dict[str, Callable] = {
            "Resume": lambda: print(
                "Action for button 'resume' not yet coded\n"
            ),
            "Options": lambda: print(
                "Action for button 'options' not yet coded\n"
            ),
            "Scores": lambda: print(
                "Action for button 'scores' not yet coded\n"
            ),
            "Save and exit": lambda: print(
                "Action for button 'save and exit' not yet coded\n"
            ),
            "Exit": lambda: print(
                "Action for button 'exit' not yet coded\n"
            )
        }

        self.calculate_panel_spacing()
        vertical_padding: int = self.h // 12

        self.left_panel: RectPanel = RectPanel(
            (self.w // 2 - self.left_panel_w) // 2,
            self.y + vertical_padding,
            self.left_panel_w,
            (self.h - vertical_padding * 2),
            self.button_actions,
            self.but_font_sz,
            self.panel_pad
        )

    def calculate_panel_spacing(self) -> None:

        max_label: str = max(
            self.button_actions.keys(),
            key=lambda label: len(label)
        )

        self.but_font_sz: int = BUTTON_FONT_SIZE
        self.panel_pad: int = PANEL_PADDING

        self.left_panel_w: int = pr.measure_text(
            max_label,
            self.but_font_sz,
        ) + self.panel_pad
        while self.left_panel_w >= self.w // 2 and self.but_font_sz >= 5:
            self.but_font_sz -= 1
            self.left_panel_w = pr.measure_text(
                max_label,
                self.but_font_sz,
            ) + self.panel_pad

        self.left_panel_w = max(
            self.left_panel_w,
            self.w // 2 - self.w // 10
        )

    def update(self) -> Any:

        for button in self.left_panel.buttons.values():

            if button.is_pressed:
                return button.action()

        return None

    def display_view(self) -> None:

        self.left_panel.display_widget()
