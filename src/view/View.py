from abc import ABC
from pyray import measure_text
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh


class View(ABC):
    def __init__(self, app) -> None:
        self.app = app
        self._update(True)

    def _update(self, forced: bool = False) -> None:
        ...

    @property
    def w(self) -> int:

        return sw()

    @property
    def h(self) -> int:

        return sh()

    @property
    def x(self) -> int:

        return (sw() - self.w) // 2

    @property
    def y(self) -> int:

        return (sh() - self.h) // 2

    @staticmethod
    def _resize_font(string: str, fontsize: int, width: int) -> int:

        while measure_text(string, fontsize) >= width and fontsize >= 5:
            fontsize -= 1
        return fontsize
