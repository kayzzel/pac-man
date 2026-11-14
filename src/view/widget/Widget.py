import pyray as pr
from pyray import MouseButton as mb
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from abc import ABC, abstractmethod
from typing import Any


class Widget(ABC):

    """
    A generic abstract class used as a template for all widgets.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int = 0,
        height: int = 0
    ) -> None:

        """
        Initializes the main attributes of a widget.

        Parameters
        ----------
        x : int
            The x coordinate of the widget in the window.
        y : int
            The y coordinate of the widget in the window.
        """

        self.x: int = x
        self.y: int = y
        self.pos: tuple[int, int] = (x, y)
        self.w: int = width
        self.h: int = height

    @property
    def is_in(self) -> bool:

        """
        Determines whether or not the mouse is in the widget.
        (used to know if the widget has been pressed)

        Returns
        -------
        bool:
            True if the mouse's coordinates are in the widget area,
            False otherwise.
        """

        if (
            self.posx <= pr.get_mouse_x() <= (self.posx + self.w)
            and self.posy <= pr.get_mouse_y() <= (self.posy + self.h)
        ):
            return True

        return False

    @property
    def is_pressed(self) -> bool:

        """
        Determines whether or not the widget has been pressed by the user.

        Returns
        -------
        bool:
            True if the mouse's coordinates are in the widget area
            and the mouse button is clicked, False otherwise.
        """

        return (
            pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT)
            and self.is_in
        )

    def _update_widget(self) -> None:

        """
        Updates the widget by checking if the widget's action,
        if it has one (clickable widget), needs to be called.
        """

        if self.is_pressed:

            self.call_action()

    def call_action(self) -> None:

        """
        Calls the function associated with the widget
        if it's a clickable widget.
        """

        if not hasattr(self, "action"):

            return

        args: Any = self.action[1]

        if isinstance(args, tuple):
            self.action[0](*args)

        elif args is not None:
            self.action[0](args)

        else:
            self.action[0]()

    @abstractmethod
    def display_widget(self) -> None:

        """
        A method to display the widget,
        must be implemented by all different widgets.
        """
        ...

    @property
    def posx(self) -> int:

        """
        Calculates relative position or fixed position for x coordinate.
        If x < 0 then the position is calculated by dividing the width by -x
        Example: for x = -2, the widget is centered horizontally
        else the widget keeps the fixed original position of x

        Returns
        -------
        int:
            The calculated x coordinate of the widget.
        """

        return (
            self.x
            if self.x >= 0
            else (sw() - self.w) // -(self.x)
        )

    @property
    def posy(self) -> int:

        """
        Calculates relative position or fixed position for y coordinate
        If y < 0 then the position is calculated by dividing the height by -y
        Example: for y = -2, the widget is centered vertically
        else the widget keeps the fixed original position of y

        Returns
        -------
        int:
            The calculated y coordinate of the widget.
        """

        return (
            self.y
            if self.y >= 0
            else (sh() - self.h) // -(self.y)
        )

    @property
    def lowerbound(self) -> int:

        """
        Calculates the bottom y coordinate of the widget
        by adding its y start position and its height.

        Returns
        -------
        int:
            The calculated bottom lowerline y of the widget.
        """

        return self.posy + self.h
