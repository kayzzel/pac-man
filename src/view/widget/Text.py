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
        max_w: int = sw(),
        color: pr.Color = pr.RAYWHITE,
        width: int = sw()
    ) -> None:

        self.label: str = label
        self.font_size: int = self._resize_font(label, font_size, max_w)
        self.x: int = (
            (width - pr.measure_text(self.label, self.font_size)) // 2
            if x == -2 else x
        )
        self.y: int = y
        self.color: pr.Color = color

    @staticmethod
    def _resize_font(string: str, fontsize: int, width: int) -> int:

        while pr.measure_text(string, fontsize) >= width and fontsize >= 5:
            fontsize -= 1
        return fontsize

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
