import pyray as pr

from .Custom_step import Custom_step, MSG_TIME
from ..View import View
from ...widgets import Widget, Text, ButtonPanel

from src.game.map.Map_custom import Maps_custom, Map_custom


class Step_five(Custom_step):

    """
    A class to ask the user if they wish to create a new map
    or save the map(s) they already finished.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self.main_view: View = main_view
        self.maps: Maps_custom = self.get_attr("maps")
        self.map: Map_custom = self.get_attr("current_map")
        self.frame_counter: int = 0
        self.show_message: str = ""
        self._update(True)

    def go_next(self) -> None:

        """
        Exits this step and goes to the next step (saving and naming the maps),
        adding the current custom map to the collection of maps.
        """

        if not self.maps.add_map(self.map):
            self.show_message = (
                "A problem occured while adding the current map."
            )
            return

        super().go_next()

    def reset(self) -> None:

        """
        Also adds the current map to the collection,
        but instead resets the whole custom creation cycle
        to create a new map.
        """

        if not self.maps.add_map(self.map):
            self.show_message = (
                "A problem occured while adding the current map."
            )
            return

        self.get_attr("reset_steps")()

    def _update_buttons(self) -> None:

        """
        Builds the back/add map/save buttons that the user can click on
        to either start a new custom map or save their collection.
        Also builds the indicative text widget 'description'.
        """
        button_w: int = self.w // 6
        button_h: int = self.h // 10
        self.back_button: ButtonPanel = ButtonPanel(
            (self.w - button_w * 4) // 2,
            ((self.h - button_h) // 3) * 2,
            button_w,
            button_h,
            {"back": (self.go_back, None)}
        )
        self.addmap_button: ButtonPanel = ButtonPanel(
            self.back_button.posx + int(button_w * 1.5),
            self.back_button.y,
            button_w,
            button_h,
            {"add map": (self.reset, None)}
        )
        self.save_button: ButtonPanel = ButtonPanel(
            self.addmap_button.posx + int(button_w * 1.5),
            self.back_button.y,
            button_w,
            button_h,
            {"save": (self.go_next, None)}
        )
        descr1: Text = Text(
            "You can continue",
            -2,
            self.h // 4,
            self.h // 15
        )
        descr2: Text = Text(
            "creating new maps (levels) or save",
            -2,
            (descr1.lowerbound + self.h // 25),
            descr1.font_size
        )
        self.widgets += [
            self.back_button,
            self.addmap_button,
            self.save_button,
            descr1,
            descr2
        ]

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

        self.widgets: list[Widget] = []
        self._update_buttons()
        self.is_freed = False

    def display_view(self) -> None:

        """
        Calls the grandparent View's display method
        to simply update and display all of the step's widgets.
        """

        super(Custom_step, self).display_view()

    def display_message(self) -> None:

        """
        Builds and displays a text message
        if adding the current map has failed,
        if the frame counter has not yet reached the end of the display time.
        """

        if self.frame_counter < MSG_TIME:

            message: Text = Text(
                self.show_message,
                -2,
                self.back_button.posy + self.back_button.h + self.h // 10,
                self.h // 25,
                self.w // 2,
                pr.RED
            )
            message.display_widget()
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.frame_counter = 0
