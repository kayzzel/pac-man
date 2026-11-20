import pyray as pr

from abc import ABC
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh

from ..widgets import Widget, Icon

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.App import App

BORDER_THICKNESS: int = 7
BORDER_PADDING: int = 3
BORDER_COLOR: pr.Color = pr.DARKBLUE


class View(ABC):

    """
    A generic abstract class that serves as a template for all views.
    """

    def __init__(self, app: "App") -> None:

        """
        Initializes the main attributes of the view
        and updates it a first time.

        Parameters
        ----------
        app: App
            The app that manages everything.
        """

        self.app: "App" = app
        self.is_freed: bool = True
        self.outline: tuple[int, int, int, int] = (
            BORDER_PADDING,
            BORDER_PADDING,
            self.w - BORDER_PADDING * 2,
            self.h - BORDER_PADDING * 2
        )
        self.show_outline: bool = True
        self._update(True)

    def _unload_images(self) -> None:

        """
        Checks all the icons in the view's widgets,
        and unloads their images and textures if not already done.
        """

        if self.is_freed and not hasattr(self, "widgets"):
            return

        for widget in self.widgets:
            if isinstance(widget, Icon):
                widget._unload_image()

        self.is_freed = True

    def _update(self, forced: bool = False) -> None:

        """
        Updates the view, checking if the window has been resized,
        and re-building the widgets if needed.

        Parameters
        ----------
        forced: bool (default False)
            Whether or not the view MUST be updated.
        """

        if not pr.is_window_resized() and not forced:
            return

        self._unload_images()
        self.widgets: list[Widget] = []
        self.is_freed = False

    @property
    def w(self) -> int:

        """
        Returns the default width of the view,
        which means the current width of the screen.

        Returns
        -------
        int
            The default width of the view.
        """

        return int(sw())

    @property
    def h(self) -> int:

        """
        Returns the default height of the view,
        which means the current height of the screen.

        Returns
        -------
        int
            The default height of the view.
        """

        return int(sh())

    @property
    def x(self) -> int:

        """
        Calculates the x centered coordinate of the view.

        Returns
        -------
        int
            The centered x position of the view.
        """

        return int((sw() - self.w) // 2)

    @property
    def y(self) -> int:

        """
        Calculates the y centered coordinate of the view.

        Returns
        -------
        int
            The centered y position of the view.
        """

        return int((sh() - self.h) // 2)

    def display_view(self) -> None:

        """
        Updates and displays the view and its widgets.
        """

        self._update()

        if self.show_outline:
            pr.draw_rectangle_lines_ex(
                self.outline,
                BORDER_THICKNESS,
                BORDER_COLOR
            )
        for widget in self.widgets:
            widget.display_widget()
