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

    @property
    def is_in_area(self) -> bool:

        if not hasattr(self, "area"):
            return False

        return (
            self.area[0] <= pr.get_mouse_x() <= self.area[0] + self.area[2]
        ) and (
            self.area[1] <= pr.get_mouse_y() <= self.area[1] + self.area[3]
        )

    def display_widget(self) -> None:

        self._update_widget()

        color: pr.Color = self.color
        if self.is_in or self.is_in_area:
            color = self.hover_color

        pr.draw_text(self.label, self.posx, self.posy, self.h, color)
