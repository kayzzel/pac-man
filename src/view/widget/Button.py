import pyray as pr
from typing import Callable, Any
from .Widget import Widget


BUTTON_BASE_COLOR: pr.Color = pr.WHITE
BUTTON_HOVER_COLOR: pr.Color = pr.DARKGRAY


class Button(Widget):

    def __init__(
        self,
        x: int,
        y: int,
        label: str,
        action: tuple[Callable, Any],
        font_sz: int = 20,
        color: pr.Color = BUTTON_BASE_COLOR,
        hover_color: pr.Color = BUTTON_HOVER_COLOR
    ) -> None:

        super().__init__(x, y, pr.measure_text(label, font_sz), font_sz)
        self.label: str = label
        self.action: tuple[Callable, Any] = action
        self.color: pr.Color = color
        self.hover_color: pr.Color = hover_color

    def display_widget(self) -> None:

        self._update_widget()

        color: pr.Color = self.color
        if self.is_in:
            color = self.hover_color

        pr.draw_text(self.label, self.posx, self.posy, self.h, color)
