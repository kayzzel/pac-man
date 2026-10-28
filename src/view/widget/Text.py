import pyray as pr
from pyray import get_screen_width as sw
from .Widget import Widget


PACMAN_FONT = "src/view/assets/fonts/crackman/Crackman.otf"

TEXT_COLOR = pr.RAYWHITE


class Text(Widget):

    font: pr.Font = pr.get_font_default()
    spacing: float = 2

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

        # these are default values, weirdly did not work when defined above
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

        # easier way of resizing text of fontsize based on max available space

        if not width:
            width = sw()

        if not hasattr(cls, "font"):
            cls._load_font()

        while cls.measure_text(string, fontsize) >= width and fontsize >= 5:

            fontsize -= 1

        return fontsize

    @property
    def width(self) -> int:

        return type(self).measure_text(self.label, self.font_size)

    @classmethod
    def measure_text(cls, text: str, font_size: int) -> int:

        return int(pr.measure_text_ex(
            cls.font, text, float(font_size), cls.spacing
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
