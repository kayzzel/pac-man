import pyray as pr
from typing import Callable
from .Widget import Widget


class Button(Widget):

    def __init__(
        self,
        x: int,
        y: int,
        label: str,
        action: Callable,
        font_sz: int = 20,
        color: pr.Color = pr.WHITE
    ) -> None:

        super().__init__(x, y, pr.measure_text(label, font_sz), font_sz)
        self.label: str = label
        self.action: Callable = action
        self.color: pr.Color = pr.WHITE

    def is_in(self, posx: int, posy: int) -> bool:

        return (
            self.posx <= posx <= self.posx + self.w
        ) and (
            self.posy <= posy <= self.posy + self.h
        )

    def display_widget(self) -> None:

        self.color = (
            pr.DARKGRAY
            if self.is_in(pr.get_mouse_x(), pr.get_mouse_y())
            else pr.WHITE
        )

        pr.draw_text(self.label, self.posx, self.posy, self.h, self.color)

    @property
    def is_pressed(self) -> bool:

        return (
            pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT)
        ) and (
            self.is_in(pr.get_mouse_x(), pr.get_mouse_y())
        )
