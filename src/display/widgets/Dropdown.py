import pyray as pr

from pyray import MouseButton as mb
from typing import Callable, Any

from .Widget import Widget
from .Text import Text
from .Panel import ButtonPanel
from .Icon import ClickableIcon


ARROW_UP_PATH: str = "assets/icons/arrow_up.png"
ARROW_DOWN_PATH: str = "assets/icons/arrow_down.png"


class Dropdown(Widget):

    """
    Simple dropdown with an arrow Icon and Buttons.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        buttons: dict[str, tuple[Callable[..., Any], Any]],
        max_show: int = 5
    ) -> None:

        """
        Initializes the main attributes of a dropdown.

        Parameters
        ----------
        x: int
            The x coordinate of the dropdown.
        y: int
            The y coordinate of the dropdown.
        width: int
            The width of the dropdown.
        height: int
            The height of the dropdown.
        buttons: dict[str, tuple[Callable, Any]]
            A dictionary containing the buttons' labels
            and the actions (function + arguments) associated with them.
        max_show: int (default 5)
            The number of buttons to show in the slide
            when the dropdown is activated.
        """

        super().__init__(x, y, width, height)

        self.show: bool = False

        self.buttons: dict[str, tuple[Callable[..., Any], Any]] = dict(buttons)
        self.max_show: int = max_show

        self.arrow_size: int = self.h // 2
        self.arrow_pad: int = self.arrow_size // 3
        self.arrow_icon_path: str = ARROW_DOWN_PATH

        self._init_main_panel()
        self._init_icons()

    def _init_main_panel(self) -> None:

        """
        Initializes the main label of the dropdown,
        the one shown at the top that indicates what it's for.
        """

        if not self.buttons:
            return

        self.main_button: dict[str, tuple[Callable[..., Any], Any]] = {
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
            (0, 0, 0),
            0,
            (pr.BLANK, pr.DARKGRAY),
            (pr.LIGHTGRAY, pr.LIGHTGRAY)
        )

        self.main_label: str = [k for k in self.main_button.keys()][0]
        self.main_panel.buttons[self.main_label].x += (
            self.w
            - Text.measure_text(self.main_label, self.main_panel.font_size)
            - self.arrow_size - self.arrow_pad * 2
        ) // 2 + self.arrow_pad
        self.main_panel.w = self.w

        self.buttons.pop(self.main_label)
        self.nb_buttons: int = len(self.buttons.values())
        self.max_show = min(self.max_show, self.nb_buttons)
        self.button_range: tuple[int, int] = (0, self.max_show - 1)

    def invert_show(self) -> None:

        """
        Updates the dropdown's state (shown or hidden)
        and sets which arrow icon to show.
        """

        self.show = not self.show

        self.arrow_icon_path = (
            ARROW_DOWN_PATH if not self.show
            else ARROW_UP_PATH
        )

        self.button_range = (0, self.max_show - 1)

    def _init_icons(self) -> None:

        """
        Initializes the two clickable arrow icons that will be used
        for the different states of the dropdown (shown or hidden),
        and that the user can click on to deploy or hide the dropdown.
        """

        arrow_x: int = self.posx + self.w - self.arrow_size - self.arrow_pad

        self.arrow_icons: dict[str, ClickableIcon] = {
            path: ClickableIcon(
                arrow_x,
                self.posy + (self.h - self.arrow_size) // 2,
                path,
                (self.invert_show, None),
                (self.arrow_size, self.arrow_size),
                True,
                False
            ) for path in [ARROW_DOWN_PATH, ARROW_UP_PATH]
        }

    def _update_buttons(self) -> None:

        """
        Updates the dropdown's buttons, the ones that you can select
        when the dropdown is deployed.
        """

        if not self.buttons or not self.show:
            return

        if pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT) and not self.is_in:
            self.invert_show()
            return

        panel_height: int = self.h * self.max_show

        current_buttons: dict[str, tuple[Callable[..., Any], Any]] = {
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
            (pr.RAYWHITE, pr.GOLD),
            pr.LIGHTGRAY
        )
        for button in self.panel.buttons.values():
            button.whole_area_activated = True

    def _scroll(self) -> None:

        """
        Checks whether or not the mouse scrolled inside the dropdown,
        and updates the buttons that should be shown if it's the case.
        """

        if not self.buttons:
            return

        if self.nb_buttons <= self.max_show:
            return

        direction: float = pr.get_mouse_wheel_move()

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

        """
        Updates and displays the dropdown, showing the buttons if deployed.
        """

        self._scroll()
        self.main_panel.display_widget()
        self.arrow_icons[self.arrow_icon_path].display_widget()

        if self.show and self.buttons:
            self._update_buttons()
            self.panel.display_widget()
