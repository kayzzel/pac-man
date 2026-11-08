import pyray as pr
# from pyray import get_screen_width as sw
# from pyray import get_screen_height as sh
from abc import ABC, abstractmethod
from .View import View
from .widget import Widget, Text, ButtonPanel, Input_box


MSG_TIME: int = 80


class Custom_step(View, ABC):

    def __init__(
        self,
        number: int,
        view: View,
        description: str,
        show_next: bool = False
    ) -> None:

        self.number: int = number
        self.main_view: View = view
        self.description_label: str = description
        self.show_next: bool = show_next
        self._update(True)

    def _update_title(self) -> None:

        label: str = "STEP " + str(self.number)
        self.title: Text = Text(
            label,
            -2,
            self.h // 15,
            self.h // 10,
            self.w // 3 * 2
        )
        self.description: Text = Text(
            self.description_label,
            -2,
            self.title.lowerbound + self.h // 25,
            self.h // 15,
            self.w // 2
        )
        self.widgets += [self.title, self.description]

    def _update_backnext_buttons(self) -> None:

        button_w: int = self.w // 10
        button_h: int = self.h // 12
        button_padx: int = self.w // 18
        button_pady: int = self.h // 25
        self.next: ButtonPanel = ButtonPanel(
            self.w - button_w - button_padx,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"next": (self.main_view.change_step, 1)}
        )
        self.back: ButtonPanel = ButtonPanel(
            self.w - (button_w + button_padx) * 2,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"back": (self.main_view.change_step, -1)}
        )
        self.widgets.append(self.back)

    @property
    def mid_space(self) -> int:

        h_rem: int = self.h - self.description.lowerbound - (
            self.h - self.back.posy
        )
        return h_rem

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_backnext_buttons()

    def display_view(self) -> None:

        for widget in self.widgets:
            widget.display_widget()

        if self.show_next:
            self.next.display_widget()


class Step_one(Custom_step):

    def __init__(self, main_view: View) -> None:

        self.map_width: int = 0
        self.map_height: int = 0
        self.show_message: str = ""
        super().__init__(
            1,
            main_view,
            "Choose map size (min 5x5, max 20x20)"
        )

    def validate_width(self) -> None:

        input_w = self.w_input.input
        if not input_w.isdigit() or not (5 <= int(input_w) <= 20):

            self.show_message = "Width is invalid, try again"
            self.frame_counter: int = 0
            self.w_input.input = ""
            self.map_width = 0
            return

        self.w_input.text_color = pr.GREEN
        self.map_width = int(input_w)

    def validate_height(self) -> None:

        input_h = self.h_input.input
        if not input_h.isdigit() or not (5 <= int(input_h) <= 20):

            self.show_message = "Height is invalid, try again"
            self.frame_counter = 0
            self.h_input.input = ""
            self.map_height = 0
            return

        self.h_input.text_color = pr.GREEN
        self.map_height = int(input_h)

    def _update_inputboxes(self) -> None:

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
        self.widgets += [self.x_sign, self.w_input, self.h_input]

    def display_message(self) -> None:

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

    def _update(self, forced: bool = False) -> None:

        if self.map_width != 0 and self.map_height != 0:
            self.show_next = True

        else:
            self.show_next = False

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_inputboxes()

    def display_view(self) -> None:

        self._update()

        if self.show_message:
            self.display_message()

        super().display_view()


class Custom_view(View):

    def __init__(self, app) -> None:

        self.app = app
        self.steps: list[Custom_step] = [
            Step_one(self)
        ]

        self.cur_step: int = 0

    def create_map(self) -> None:

        ...

    def change_step(self, new: int = 1) -> None:

        if self.cur_step + new == len(self.steps):
            self.create_map()
            return

        if self.cur_step + new == -1:
            self.app.return_to_prev_view()
            self.app.remove_last_view()
            return

        if not (0 <= self.cur_step + new < len(self.steps)):
            return

        self.cur_step += new

    def display_view(self) -> None:

        self.steps[self.cur_step].display_view()
