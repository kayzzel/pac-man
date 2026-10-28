import pyray as pr
from pyray.MouseButton import MOUSE_BUTTON_LEFT
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from abc import ABC, abstractmethod
from typing import Any


class Widget(ABC):

    def __init__(
        self,
        x: int,
        y: int,
        width: int = 0,
        height: int = 0
    ) -> None:

        self.x: int = x
        self.y: int = y
        self.pos: tuple[int, int] = (x, y)
        self.w: int = width
        self.h: int = height

    @property
    def is_in(self) -> bool:

        # generic property for all widgets to know if mouse in radius

        return (
            self.posx <= pr.get_mouse_x() <= self.posx + self.w
        ) and (
            self.posy <= pr.get_mouse_y() <= self.posy + self.h
        )

    @property
    def is_pressed(self) -> bool:

        # generic property for all widgets to know if widget is pressed
        # mostly used only for clickable widgets

        return (
            pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT)
        ) and (
            self.is_in
        )

    def _update_widget(self) -> None:

        # used only for clickable widgets

        if self.is_pressed:

            self.call_action()

    def call_action(self) -> None:

        # used only for clickable widgets

        if not hasattr(self, "action"):

            return

        args: Any = self.action[1]

        if isinstance(args, tuple):
            self.action[0](*args)

        elif args:
            self.action[0](args)

        else:
            self.action[0]()

    @abstractmethod
    def display_widget(self) -> None:

        ...

    @property
    def posx(self) -> int:

        # calculates relative position or fixed position for x coordinate
        # if x < 0 then the position is calculated by dividing the width by -x
        # example: for x = -2, the widget is centered horizontally
        # else the widget keeps the fixed original position of x

        return (
            self.x
            if self.x >= 0
            else (sw() - self.w) // -(self.x)
        )

    @property
    def posy(self) -> int:

        # calculates relative position or fixed position for y coordinate
        # if y < 0 then the position is calculated by dividing the height by -y
        # example: for y = -2, the widget is centered vertically
        # else the widget keeps the fixed original position of y

        return (
            self.y
            if self.y >= 0
            else (sh() - self.h) // -(self.y)
        )
