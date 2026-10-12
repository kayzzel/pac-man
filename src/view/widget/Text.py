import pyray as pr
from pyray import get_screen_width as sw
from .Widget import Widget


class Text(Widget):

    def __init__(
        self,
        label: str,
        x: int,
        y: int,
        font_size: int,
        max_w: int = 0,
        color: pr.Color = pr.RAYWHITE,
        width: int = 0
    ) -> None:

        if not max_w:
            max_w = sw()
        if not width:
            width = sw()

        self.label: str = label
        self.font_size: int = self._resize_font(label, font_size, max_w)
        self.x: int = (
            (width - self.w) // (-x)
            if x < 0 else x
        )
        self.y: int = y
        self.color: pr.Color = color

    @staticmethod
    def _resize_font(string: str, fontsize: int, width: int = 0) -> int:

        if not width:
            width = sw()

        while pr.measure_text(string, fontsize) >= width and fontsize >= 5:
            fontsize -= 1
        return fontsize

    @property
    def w(self) -> int:

        return pr.measure_text(self.label, self.font_size)

    @property
    def lowerbound(self) -> int:

        return self.y + self.font_size

    def display_widget(self) -> None:

        pr.draw_text(
            self.label,
            self.x,
            self.y,
            self.font_size,
            self.color
        )
