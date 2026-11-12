import pyray as pr
from pyray import get_screen_width as sw
from .Widget import Widget


DEFAULT_FONT = "src/view/assets/fonts/Gohu/GohuFont11NerdFontMono-Regular.ttf"
PACMAN_FONT = "src/view/assets/fonts/crackman/Crackman.otf"

TEXT_COLOR = pr.RAYWHITE


class Text(Widget):

    font = pr.get_font_default()
    spacing: int = 4
    default: bool = True
    init: bool = False

    current_font: str = "default"
    fonts: dict[str, str] = {
        "default": DEFAULT_FONT,
        "pac-man": PACMAN_FONT
    }

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

        """
        Parameters
        ----------
        Returns
        -------
        """
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
    def _load_font(cls, new_font: str = "default") -> None:

        """
        Parameters
        ----------
        Returns
        -------
        """
        if new_font not in cls.fonts.keys():
            return

        cls.font = pr.load_font(cls.fonts[new_font])
        cls.current_font = new_font
        cls.spacing = 2
        cls.default = False

    @classmethod
    def _resize_font(cls, string: str, fontsize: int, width: int = 0) -> int:

        """
        Parameters
        ----------
        Returns
        -------
        """
        # easier way of resizing text of fontsize based on max available space

        if not width:
            width = sw()

        if not cls.init:
            cls._load_font()
            cls.init = True

        while cls.measure_text(string, fontsize) >= width and fontsize >= 5:

            fontsize -= 1

        return fontsize

    @property
    def width(self) -> int:

        """
        Parameters
        ----------
        Returns
        -------
        """
        return type(self).measure_text(self.label, self.font_size)

    @classmethod
    def measure_text(cls, text: str, font_size: int) -> int:

        """
        Parameters
        ----------
        Returns
        -------
        """
        if not cls.init:
            cls._load_font()
            cls.init = True

        if not cls.default:
            return int(pr.measure_text_ex(
                cls.font, text, float(font_size), cls.spacing
            ).x)
        return int(pr.measure_text(text, font_size))

    @property
    def lowerbound(self) -> int:

        """
        Parameters
        ----------
        Returns
        -------
        """
        return self.y + self.font_size

    def display_widget(self) -> None:

        """
        Parameters
        ----------
        Returns
        -------
        """
        if not type(self).default:
            pr.draw_text_ex(
                type(self).font,
                self.label,
                (self.x, self.y),
                float(self.font_size),
                self.spacing,
                self.color
            )
        else:
            pr.draw_text(
                self.label,
                self.x,
                self.y,
                self.font_size,
                self.color
            )
