import pyray as pr
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

        return (
            self.posx <= pr.get_mouse_x() <= self.posx + self.w
        ) and (
            self.posy <= pr.get_mouse_y() <= self.posy + self.h
        )

    @property
    def is_pressed(self) -> bool:

        return (
            pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT)
        ) and (
            self.is_in
        )

    def _update_widget(self) -> None:

        if self.is_pressed:

            self.call_action()

    def call_action(self) -> None:

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

        return (
            self.x
            if self.x >= 0
            else (sw() - self.w) // -(self.x)
        )

    @property
    def posy(self) -> int:

        return (
            self.y
            if self.y >= 0
            else (sh() - self.h) // -(self.y)
        )
