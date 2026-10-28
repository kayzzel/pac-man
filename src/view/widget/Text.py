import pyray as pr
from pyray import get_screen_width as sw
from .Widget import Widget


PACMAN_FONT = "src/view/assets/fonts/crackman/Crackman.otf"

TEXT_COLOR = pr.RAYWHITE


class Text(Widget):

    spacing: float = 2
    font: pr.Font = pr.get_font_default()

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
            (width - self.width) // (-x)
            if x < 0 else x
        )
        self.y: int = y
        self.color: pr.Color = color

    @classmethod
    def _load_font(cls) -> None:
        cls.font = pr.load_font(PACMAN_FONT)

    @classmethod
    def _resize_font(cls, string: str, fontsize: int, width: int = 0) -> int:

        if not width:
            width = sw()

        if not hasattr(cls, "font"):
            cls._load_font()

        while int(pr.measure_text_ex(
            cls.font, string, float(fontsize), cls.spacing
        ).x) >= width and fontsize >= 5:

            fontsize -= 1

        return fontsize

    @property
    def width(self) -> int:

        return int(pr.measure_text_ex(
            type(self).font, self.label, float(self.font_size), self.spacing
        ).x)

    @property
    def lowerbound(self) -> int:

        return self.y + self.font_size

    def display_widget(self) -> None:

        pr.draw_text_ex(
            type(self).font,
            self.label,
            (self.x, self.y),
            float(self.font_size),
            self.spacing,
            self.color
        )
