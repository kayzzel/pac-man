import pyray as pr
from pyray import MouseButton as mb
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from abc import ABC, abstractmethod
from typing import Any


class Widget(ABC):
    """Base of every widget: position, hover, click and actions."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int = 0,
        height: int = 0
    ) -> None:
        """
            Description:
        Create a widget at a fixed position (x and y >= 0) or at a
        relative position (x or y < 0) computed against the screen
        size, for example -2 to center it on the axis.

            Parameters:
        x -> fixed column, or -n for a relative position on x
        y -> fixed row, or -n for a relative position on y
        width -> width of the widget, used by the relative positions
                 and the hover detection
        height -> height of the widget, same use as the width
        """
        self.x: int = x
        self.y: int = y
        self.pos: tuple[int, int] = (x, y)
        self.w: int = width
        self.h: int = height

    @property
    def is_in(self) -> bool:
        """
            Description:
        Tell whether the mouse currently hovers the widget.

            Returns value:
        return True when the mouse is inside the widget's area
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
            Description:
        Tell whether the left mouse button is pressed on the widget,
        mostly used by the clickable widgets.

            Returns value:
        return True when the widget is being pressed
        """
        return (
            pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT)
            and self.is_in
        )

    def _update_widget(self) -> None:
        """
            Description:
        Trigger the widget's action when it is pressed, called by the
        display of the clickable widgets.
        """
        if self.is_pressed:

            self.call_action()

    def call_action(self) -> None:
        """
            Description:
        Call the widget's action with its argument: a tuple argument
        is unpacked as positional arguments, a single value is given
        as is, and no argument calls the action without any. A widget
        without action does nothing.
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
            Description:
        Draw the widget on the screen for one frame, defined by every
        concrete widget.
        """
        ...

    @property
    def posx(self) -> int:
        """
            Description:
        Give the x position of the widget on the screen: a fixed
        position for x >= 0, else a position computed by dividing
        the screen by -x (x = -2 centers the widget horizontally).

            Returns value:
        return the x column where the widget is drawn
        """
        return (
            self.x
            if self.x >= 0
            else (sw() - self.w) // -(self.x)
        )

    @property
    def posy(self) -> int:
        """
            Description:
        Give the y position of the widget on the screen: a fixed
        position for y >= 0, else a position computed by dividing
        the screen by -y (y = -2 centers the widget vertically).

            Returns value:
        return the y row where the widget is drawn
        """
        return (
            self.y
            if self.y >= 0
            else (sh() - self.h) // -(self.y)
        )
