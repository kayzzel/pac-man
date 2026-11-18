import pyray as pr

from .Custom_step import Custom_step, MSG_TIME
from ..View import View
from ...widgets import Text, Input_box


class Step_six(Custom_step):

    """
    A step for the user to enter the name of their custom map.
    """

    def __init__(self, main_view: View) -> None:

        """
        Calls the Custom_step's parent method for the main attributes.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        super().__init__(
            5,
            main_view,
            "Choose a name for your map(s)"
        )

    def validate_name(self) -> None:

        """
        Checks and validates the name for the custom map
        entered by the user, setting the 'show_message' value
        to a confirmation/refusal message depending on if it's valid.
        """

        if self.maps.set_name(self.input_box.input):
            self.show_message = (
                f"Saved the name '{self.input_box.input}' for your custom map"
            )
            self.input_box.text_color = pr.GREEN
            self.input_box.cursor_color = pr.DARKGREEN
        else:
            self.show_message = f"Name '{self.input_box.input}' invalid"
            self.input_box.text_color = pr.RED
            self.input_box.cursor_color = pr.MAROON

    def _update_inputbox(self) -> None:

        """
        Builds the input box in which the user enters the name
        of their custom map, only allowing for non-existing name
        and alphabetical characters + '-' and '_'.
        """

        all_characters: list[int] = [45, 95]
        for crange in [(48, 58), (65, 91), (97, 123)]:
            all_characters += [i for i in range(*crange)]

        self.input_box: Input_box = Input_box(
            -2,
            -2,
            self.w // 3,
            self.h // 10,
            (self.validate_name, None),
            20,
            all_characters
        )

        h_rem: int = (
            self.h
            - self.description.lowerbound
            - (self.h - self.input_box.posy)
        )
        self.input_label: Text = Text(
            "enter name (only alphabetical and '_', '-' allowed) :",
            -2,
            self.description.lowerbound + h_rem // 3 * 2 - self.h // 25,
            self.h // 25
        )
        self.widgets += [self.input_label, self.input_box]

    def display_message(self) -> None:

        """
        Builds and displays a text message
        for the confirmation/refusal of the map's name entered,
        if the frame counter has not yet reached the end of the display time.
        """

        if self.frame_counter < MSG_TIME:

            message: Text = Text(
                self.show_message,
                -2,
                self.input_box.posy + self.input_box.h + self.h // 10,
                self.h // 25,
                self.w // 2,
                self.input_box.text_color
            )
            message.display_widget()
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.input_box.text_color = (
                self.input_box.base_colors[1]
            )
            self.input_box.cursor_color = (
                self.input_box.base_colors[2]
            )
            self.frame_counter = 0

    def go_next(self) -> None:

        """
        Exits this step and goes to the next step,
        saving the custom map's layout and information.
        """

        self.maps.save_maps()
        super().go_next()

    def go_back(self) -> None:

        """
        Exits this step and goes back to the previous step,
        resetting the name of the map to undefined.
        """

        self.maps.name_set = False
        super().go_back()

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the user has entered their custom map's name
        and can go to the next step,
        if the window has been resized or an update is required,
        and updates the widgets if so.
        Also changes the label of the 'next' button
        already built by the parent Custom_step's 'update_backnext_buttons'
        to indicate 'save' instead.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        self.show_next = self.maps.name_set

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self.next.buttons["next"].label = "save"
        self._update_inputbox()
