import pyray as pr

from .Custom_step import Custom_step
from ..View import View
from ...widgets import Widget, Text, ButtonPanel

from src.game.map.Map_custom import Map_custom


class Step_seven(Custom_step):

    """
    A last step used for the user to launch their finished custom map
    or instead return to the main menu.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main view and map of the step and updates a first time.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self.main_view: View = main_view
        self.map: Map_custom = self.get_attr("current_map")
        self.is_freed: bool = True
        self._update(True)

    def _update_widgets(self) -> None:

        """
        Builds the yes, no buttons that the user can click on
        to either launch their custom map(s) or return to the main menu.
        Also builds the indicative text widgets 'question' and 'description'.
        """
        button_w: int = self.w // 15
        button_h: int = self.h // 10
        self.yes_button: ButtonPanel = ButtonPanel(
            (self.w - button_w * 3) // 2,
            -2,
            button_w,
            button_h,
            {"yes": (self.get_attr("launch_game"), self.map.map.name)}
        )
        self.no_button: ButtonPanel = ButtonPanel(
            self.yes_button.posx + button_w * 2,
            -2,
            button_w,
            button_h,
            {"no": (self.get_attr("go_to_menu"), None)}
        )
        self.question: Text = Text(
            "Start the game?",
            -2,
            (self.h - self.yes_button.posy) // 3,
            self.h // 10
        )
        self.description: Text = Text(
            "(you can load your map at any time from the menu)",
            -2,
            self.question.lowerbound + self.h // 25,
            self.h // 20
        )
        self.widgets += [
            self.yes_button,
            self.no_button,
            self.question,
            self.description
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
        self._update_widgets()
        self.is_freed = False

    def display_view(self) -> None:

        """
        Calls the grandparent View's display method
        to simply update and display all of the step's widgets.
        """

        super(Custom_step, self).display_view()
