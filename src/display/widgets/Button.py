import pyray as pr

from pyray import MouseButton as mb
from typing import Callable, Any

from .Widget import Widget
from .Text import Text


BUTTON_BASE_COLOR: pr.Color = pr.WHITE
BUTTON_HOVER_COLOR: pr.Color = pr.DARKGRAY


class Button(Widget):

    """
    Clickable label that calls an associated function
    with its arguments when pressed.
    """

    def __init__(
        self,
        x: int,
        y: int,
        label: str,
        action: tuple[Callable[..., Any], Any],
        font_sz: int = 20,
        color: pr.Color = BUTTON_BASE_COLOR,
        hover_color: pr.Color = BUTTON_HOVER_COLOR
    ) -> None:

        """
        Initializes the main attributes of a button.

        Parameters
        ----------
        x: int
            The x coordinate of the button.
        y: int
            The y coordinate of the button.
        label: str
            The name of the button.
        action: tuple[Callable, Any]
            The function to call and its arguments.
        font_sz: int (default 20)
            The font size of the button's label.
        color: pr.Color (default BUTTON_BASE_COLOR)
            The color of the button's label.
        hover_color: pr.Color (default BUTTON_HOVER_COLOR)
            The color of the button's label when the mouse hovers over it.
        """

        super().__init__(x, y, Text.measure_text(label, font_sz), font_sz)

        self.label: str = label
        self.action: tuple[Callable[..., Any], Any] = action
        self.color: pr.Color = color
        self.hover_color: pr.Color = hover_color
        self.whole_area_activated: bool = False

    @property
    def is_pressed(self) -> bool:

        """
        An override of the parent Widget's method,
        but adjusted to also consider clicks that are inside
        the button's whole area but not necessarily directly on the label.

        Returns
        -------
        bool:
            True if the button has been pressed, False otherwise.
        """

        return (
            pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT)
            and (self.is_in or (self.whole_area_activated and self.is_in_area))
        )

    @property
    def is_in_area(self) -> bool:

        """
        Checks whether or not the mouse is in the button's area.

        Returns
        -------
        bool:
            True if the mouse coordinates are in the button's area.
        """

        if not hasattr(self, "area"):
            return False

        if (
            self.area[0] <= pr.get_mouse_x() <= (self.area[0] + self.area[2])
            and (
                self.area[1] <= pr.get_mouse_y()
                <= (self.area[1] + self.area[3])
            )
        ):
            return True

        return False

    def set_area(self, area: tuple[int, int, int, int]) -> None:

        """
        Defines the button's whole area (basically the background 'rectangle').

        Parameters
        ----------
        area: tuple[int, int, int, int]
            The area of the button (x, y, width, height).
        """

        self.area: tuple[int, int, int, int] = area

    def display_widget(self) -> None:

        """
        Updates and displays the button, based on whether
        the mouse hovers over it or not.
        """

        self._update_widget()

        color: pr.Color = self.color
        if self.is_in or (self.is_in_area and self.whole_area_activated):
            color = self.hover_color

        pr.draw_text_ex(
            Text.font,
            self.label,
            (self.posx, self.posy),
            float(self.h),
            Text.spacing,
            color
        )
