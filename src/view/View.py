import pyray as pr
from abc import ABC
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from .widget import Widget, Icon


class View(ABC):
    def __init__(self, app) -> None:
        self.app = app
        self.is_freed: bool = True
        self._update(True)

    def _unload_images(self) -> None:

        if self.is_freed and not hasattr(self, "widgets"):
            return

        for widget in self.widgets:
            if isinstance(widget, Icon):
                widget._unload_image()

        self.is_freed = True

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self._unload_images()
        self.widgets: list[Widget] = []
        self.is_freed = False

    @property
    def w(self) -> int:

        return sw()

    @property
    def h(self) -> int:

        return sh()

    @property
    def x(self) -> int:

        return (sw() - self.w) // 2

    @property
    def y(self) -> int:

        return (sh() - self.h) // 2

    def display_view(self) -> None:

        self._update()
        for widget in self.widgets:
            widget.display_widget()
