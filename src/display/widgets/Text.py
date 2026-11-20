import pyray as pr

from pyray import get_screen_width as sw

from .Widget import Widget


DEFAULT_FONT = "assets/fonts/Gohu/GohuFont11NerdFontMono-Regular.ttf"
PACMAN_FONT = "assets/fonts/crackman/Crackman.otf"

TEXT_COLOR = pr.GOLD


class Text(Widget):

    """
    A Text widget for displaying text more easily.

    Attributes
    ----------
    font: pr.Font (default Pyray's default font)
        The font used to write text on the screen.
    spacing: int (default 4)
        The spacing for the font (needed if not using default Pyray font)
    default: bool (default True)
        Indicates whether or not the class is using the Pyray default font.
    init: bool (default False)
        Indicates whether or not a font has been loaded
        (when the resizing class method is used by other classes).
    current_font: str (default "default")
        The current font name used by the class.
    fonts: dict[str, str]
        A dictionary storing the paths of fonts by their name.
    """

    font: pr.Font = pr.get_font_default()
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
        color: pr.Color = TEXT_COLOR,
        width: int = 0
    ) -> None:

        """
        Initializes the main attributes of the text.

        Parameters
        ----------
        label: str
            The text that should be displayed.
        x: int
            The x coordinate of the text.
        y: int
            The y coordinate of the text.
        font_size: int
            The font size for the text.
        max_w: int (default 0 but changed below to screen width)
            The width the text should not go above.
        color: pr.Color (default TEXT_COLOR)
            The color of the text.
        width: int (default 0 but changed below to screen width)
            The total width that the text should be relative to
            (used for centering inside a bigger item for example).
        """

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
        Loads the font given based on its name
        and if it's already a font stored in the class dictionary.

        Parameters
        ----------
        new_font: str (default "default")
            The name of the font to load (replaces current one).
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
        Calculates the correct font size based on the maximum width
        by decreasing the font size already given.

        Parameters
        ----------
        string: str
            The text for which to calculate the font size.
        fontsize: int
            The initial font size, to check if not going above maximum width.
        width: int (default 0 but changed later to screen width)
            The maximum width that the text's width should not overcap.

        Returns
        -------
        int
            The correct font size with the class' current font and spacing.
        """

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
        Returns the width of the Text object instanciated,
        using the class method to measure width.

        Returns
        -------
        int
            The width of the text.
        """

        return type(self).measure_text(self.label, self.font_size)

    @classmethod
    def measure_text(cls, text: str, font_size: int) -> int:

        """
        Measures the width of a text given,
        using the font size given and the class' font and spacing.

        Parameters
        ----------
        text: str
            The text to measure.
        font_size: int
            The font size to use to measure the text.

        Returns
        -------
        int
            The calculated width of the text.
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
        An override of the Widget's parent method,
        using the font size instead of the 'h'
        to get the correct text height.

        Returns
        -------
        int
            The end y coordinate of the text
            (where it ends on the bottom line).
        """

        return self.y + self.font_size

    def display_widget(self) -> None:

        """
        Displays the text using either the Pyray default font
        or the current loaded font (different Pyray drawing functions).
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
