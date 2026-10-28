import pyray as pr
from typing import Callable, Any
from .Widget import Widget
from .Text import Text


BUTTON_BASE_COLOR: pr.Color = pr.WHITE
BUTTON_HOVER_COLOR: pr.Color = pr.DARKGRAY


class Button(Widget):

    # clickable label that calls function when pressed

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

        super().__init__(x, y, Text.measure_text(label, font_sz), font_sz)

        self.label: str = label
        self.action: tuple[Callable, Any] = action
        self.color: pr.Color = color
        self.hover_color: pr.Color = hover_color

    @property
    def is_in_area(self) -> bool:

        if not hasattr(self, "area"):
            return False

        return (
            self.area[0] <= pr.get_mouse_x() <= (self.area[0] + self.area[2])
        ) and (
            self.area[1] <= pr.get_mouse_y() <= (self.area[1] + self.area[3])
        )

    def set_area(self, area: tuple[int, int, int, int]) -> None:

        self.area: tuple[int, int, int, int] = area

    def display_widget(self) -> None:

        self._update_widget()

        color: pr.Color = self.color
        if self.is_in or self.is_in_area:
            color = self.hover_color

        pr.draw_text_ex(
            Text.font,
            self.label,
            (self.posx, self.posy),
            float(self.h),
            Text.spacing,
            color
        )
