from abc import ABC, abstractmethod
import pyray as pr


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

    @abstractmethod
    def display_widget(self) -> None:

        ...

    @property
    def posx(self) -> int:

        return (
            self.x
            if self.x >= 0
            else (pr.get_screen_width() - self.w) // -(self.x)
        )

    @property
    def posy(self) -> int:

        return (
            self.y
            if self.y >= 0
            else (pr.get_screen_height() - self.h) // -(self.y)
        )
