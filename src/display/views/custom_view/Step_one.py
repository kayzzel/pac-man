import pyray as pr

from .Custom_step import Custom_step, MSG_TIME
from ..View import View
from ...widgets import Text, Input_box


class Step_one(Custom_step):

    """
    A step for the user to define the width/height of their custom map.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step,
        setting the width/height values to default,
        and calling the Custom_step's parent method for the other attributes.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self.is_init: bool = False
        self.width_set: bool = True
        self.height_set: bool = True
        super().__init__(
            1,
            main_view,
            "Choose map size (min 10x10, max 30x30)"
        )
        self.w_input.text_color = pr.GREEN
        self.h_input.text_color = pr.GREEN

    def validate_width(self) -> None:

        """
        Checks and validates the height entered by the user,
        setting the 'show_message' value to a refusal message
        if invalid, otherwise setting the map's rows via the Map_custom.
        """

        input_w = self.w_input.input
        if not input_w.isdigit() or not (10 <= int(input_w) <= 30):

            self.show_message = "Width is invalid, try again"
            self.w_input.input = str(self.map.cols)
            self.width_set = False
            return

        self.w_input.text_color = pr.GREEN
        self.map.set_cols(int(input_w))
        self.width_set = True

    def validate_height(self) -> None:

        """
        Checks and validates the height entered by the user,
        setting the 'show_message' value to a refusal message
        if invalid, otherwise setting the map's rows via the Map_custom.
        """

        input_h = self.h_input.input
        if not input_h.isdigit() or not (10 <= int(input_h) <= 30):

            self.show_message = "Height is invalid, try again"
            self.h_input.input = str(self.map.rows)
            self.height_set = False
            return

        self.h_input.text_color = pr.GREEN
        self.map.set_rows(int(input_h))
        self.height_set = True

    def _update_inputboxes(self) -> None:

        """
        Builds the two input boxes in which the user
        enters the width and height of the map they want to create.
        """

        self.x_sign: Text = Text(
            "  X  ",
            -2,
            self.description.lowerbound + (
                self.mid_space - Text.measure_text(
                    "  X  ", self.mid_space // 10
                )
            ) // 2,
            self.mid_space // 10,
            self.mid_space // 6
        )
        box_w: int = self.mid_space // 3
        box_h: int = self.mid_space // 6
        box_y: int = self.x_sign.y + (self.x_sign.font_size - box_h) // 2
        self.w_input: Input_box = Input_box(
            self.x_sign.x - box_w,
            box_y,
            box_w,
            box_h,
            (self.validate_width, None),
            2,
            (48, 57)
        )
        self.h_input: Input_box = Input_box(
            self.x_sign.x + self.x_sign.width,
            box_y,
            box_w,
            box_h,
            (self.validate_height, None),
            2,
            (48, 57)
        )
        self.w_input.input = str(self.map.cols)
        self.h_input.input = str(self.map.rows)
        self.is_init = True
        self.widgets += [self.x_sign, self.w_input, self.h_input]

    def display_message(self) -> None:

        """
        Builds and displays a text widget showing the refusal message
        if an input entered by the user was invalid.
        """

        if self.frame_counter < MSG_TIME:

            message: Text = Text(
                self.show_message,
                -2,
                self.w_input.posy + self.w_input.h + self.mid_space // 8,
                self.mid_space // 10,
                self.mid_space,
                pr.RED
            )
            message.display_widget()
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.frame_counter = 0

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the width/height have finished being set,
        and if so toggling the 'next' button so that the user
        can go to the next step.
        Also checks if the window has been resized or an update is required,
        and updating widgets if needed.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        if self.is_init:
            self.width_set = not self.w_input.enter_input
            self.height_set = not self.h_input.enter_input
        self.show_next = (self.width_set and self.height_set)

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_inputboxes()
