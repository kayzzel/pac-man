import pyray as pr
from pyray.MOUSE_BUTTON import MOUSE_BUTTON_LEFT
from typing import Callable, Any
from .Widget import Widget
from .Text import Text
from .Panel import ButtonPanel
from .Icon import ClickableIcon


ARROW_UP_PATH: str = "src/view/assets/icons/arrow_up.png"
ARROW_DOWN_PATH: str = "src/view/assets/icons/arrow_down.png"


class Dropdown(Widget):

    # simple dropdown with an arrow Icon and Buttons

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        buttons: dict[str, tuple[Callable, Any]],
        max_show: int = 5
    ) -> None:

        super().__init__(x, y, width, height)

        self.show: bool = False

        self.buttons: dict[str, tuple[Callable, Any]] = buttons
        self.max_show: int = max_show

        self.arrow_size: int = self.h // 2
        self.arrow_pad: int = self.arrow_size // 3
        self.arrow_icon_path: str = ARROW_DOWN_PATH

        self._init_main_panel()

    def _init_main_panel(self) -> None:

        # this is to initialize the main label, the 'title' of the dropdown

        self.main_button: dict[str, tuple[Callable, Any]] = {
            label: action
            for i, (label, action) in enumerate(self.buttons.items())
            if i == 0
        }

        self.main_panel: ButtonPanel = ButtonPanel(
            self.posx,
            self.posy,
            self.w - self.arrow_size - self.arrow_pad * 2,
            self.h,
            self.main_button,
            (self.w // 12, 0, 0),
            -2,
            (pr.BLANK, pr.DARKGRAY),
            (pr.RAYWHITE, pr.RAYWHITE)
        )

        self.main_label: str = [k for k in self.main_button.keys()][0]

        self.main_panel.center = (
            self.w
            - Text.measure_text(self.main_label, self.main_panel.font_size)
            - self.arrow_size - self.arrow_pad * 2
        ) // 2

        self.main_panel.w = self.w

        self.buttons.pop(self.main_label)
        self.nb_buttons: int = len(self.buttons.values())
        self.max_show = min(self.max_show, self.nb_buttons)
        self.button_range: tuple[int, int] = (0, self.max_show - 1)

    def invert_show(self) -> None:

        # changes the state of the dropdown (shown or hidden)

        self.show = not self.show

        self.arrow_icon_path = (
            ARROW_DOWN_PATH if not self.show
            else ARROW_UP_PATH
        )

        self.button_range = (0, self.max_show - 1)

    def _update_icon(self) -> None:

        arrow_x: int = self.posx + self.w - self.arrow_size - self.arrow_pad

        self.arrow_icon: ClickableIcon = ClickableIcon(
            arrow_x,
            self.posy + (self.h - self.arrow_size) // 2,
            self.arrow_icon_path,
            (self.invert_show, None),
            (self.arrow_size, self.arrow_size),
            True,
            False
        )

    def _update_buttons(self) -> None:

        if not self.show:
            return

        if pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and not self.is_in:
            self.invert_show()
            return

        panel_height: int = self.h * self.max_show

        current_buttons: dict[str, tuple[Callable, Any]] = {
            label: action
            for i, (label, action) in enumerate(self.buttons.items())
            if self.button_range[0] <= i <= self.button_range[1]
        }

        self.panel: ButtonPanel = ButtonPanel(
            self.posx,
            self.posy + self.h,
            self.w,
            panel_height,
            current_buttons,
            (0, 0, 0),
            -2,
            (pr.BLANK, pr.DARKGRAY),
            (pr.RAYWHITE, pr.BLACK),
            pr.LIGHTGRAY
        )

    def _scroll(self, direction: float = 0) -> None:

        if self.nb_buttons <= self.max_show:
            return

        direction = pr.get_mouse_wheel_move()

        if direction == 0 or not self.show or not self.panel.is_in:
            return

        offset: int = 0
        if direction < 0 and self.button_range[1] < self.nb_buttons - 1:
            offset = 1

        elif direction > 0 and self.button_range[0] > 0:
            offset = -1

        self.button_range = (
            self.button_range[0] + offset,
            self.button_range[1] + offset
        )
        self._update_buttons()

    def display_widget(self) -> None:

        self._scroll()
        self._update_icon()
        self.main_panel.display_widget()
        self.arrow_icon.display_widget()

        if self.show:
            self._update_buttons()
            self.panel.display_widget()
