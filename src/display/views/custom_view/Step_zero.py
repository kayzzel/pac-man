import pyray as pr

from typing import Callable, Any

from .Custom_step import Custom_step
from ..View import View
from ...widgets import Text, ButtonPanel, Dropdown

from src.game.map.Map_storing import get_stored_map_list


class Step_zero(Custom_step):

    """
    A step used for the user to either select an already
    existing custom map to launch, or create a new one from scratch.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step,
        such as its number, all of the custom maps already created,
        and the main view.

        Parameters
        ----------
        main_view: View
            The view overseeing all the steps.
        """

        self.number: int = 0
        self.map_n: list[str] = get_stored_map_list(main_view.app.map_folder)
        self.main_view: View = main_view
        self.is_freed: bool = True
        self._update(True)

    def _update_title(self) -> None:

        """
        Builds the title widget for this step.
        """

        self.title: Text = Text(
            "LOAD EXISTING MAP",
            -2,
            self.h // 4,
            self.h // 8
        )
        self.widgets.append(self.title)

    def _update_buttons(self) -> None:

        """
        Builds the back and next buttons for this step.
        """

        button_w: int = self.w // 7
        button_h: int = self.h // 12
        button_padx: int = self.w // 20
        button_pady: int = self.h // 25
        self.back: ButtonPanel = ButtonPanel(
            (self.w - button_w * 2 - button_padx) // 2,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"back": (self.go_back, None)}
        )
        self.next: ButtonPanel = ButtonPanel(
            self.back.posx + button_w + button_padx,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"new map": (self.go_next, None)}
        )
        self.widgets += [self.back, self.next]

    def _update_dropdown(self) -> None:

        """
        Builds the map dropdown widget that allows
        the user to select an already existing custom map
        to launch directly.
        """

        load_label: str = "Select a map"
        dropdown_buttons: dict[
            str,
            tuple[Callable[..., Any], Any]
        ] = {
            load_label: (lambda: 0, None)
        } | {
            map_name: (self.get_attr("launch_game"), map_name)
            for map_name in self.map_n
        }
        self.map_dropdown: Dropdown = Dropdown(
            -2,
            self.title.y + self.title.font_size + self.h // 15,
            self.w // 4,
            self.h // 15,
            dropdown_buttons
        )
        self.widgets.append(self.map_dropdown)

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the window has been resized or an update is required,
        and updates the widgets if so.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        if not pr.is_window_resized() and not forced:
            return

        super(Custom_step, self)._update(True)
        self._update_title()
        self._update_buttons()
        self._update_dropdown()

    def display_view(self) -> None:

        """
        Calls the grandparent View's method
        to simply update and display the step's widgets.
        """

        super(Custom_step, self).display_view()
