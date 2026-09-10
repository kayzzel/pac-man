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
