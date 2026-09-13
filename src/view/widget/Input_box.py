import pyray as pr
from .Widget import Widget


MAX_INPUT_CHARS: int = 10

DEFAULT_COLOR: pr.Color = pr.RAYWHITE
TEXT_COLOR: pr.Color = pr.MAROON
CURSOR_COLOR: pr.Color = pr.RED


class Input_box(Widget):

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        max_chars: int = MAX_INPUT_CHARS,
        colors: tuple[pr.Color, pr.Color, pr.Color] = (
            DEFAULT_COLOR,
            TEXT_COLOR,
            CURSOR_COLOR
        )
    ) -> None:

        super().__init__(x, y, width, height)

        self.textbox: tuple[int, int, int, int] = (
            self.x, self.y, self.w, self.h
        )
        self.font_size: int = self.h - 5
        self.max_chars: int = max_chars
        self.standin_input: str = "h" * max_chars
        self.box_color: pr.Color
        self.text_color: pr.Color
        self.cursor_color: pr.Color
        self.box_color, self.text_color, self.cursor_color = colors

        self.input: str = ""
        self.enter_input: bool = False
        self.frame_counter: int = 0

        self.calculate_font_size()

    def calculate_font_size(self) -> None:

        while (
            pr.measure_text(
                self.standin_input,
                self.font_size
            ) >= self.w - 5
        ) and self.font_size >= 1:

            self.font_size -= 1

    def update_widget(self) -> None:

        if self.is_pressed and not self.enter_input:
            self.enter_input = True

        if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT) and not self.is_in:
            self.enter_input = False

        if self.enter_input:

            pr.set_mouse_cursor(pr.MOUSE_CURSOR_IBEAM)
            self.frame_counter += 1

            key: int = pr.get_char_pressed()

            while key > 0:

                if key >= 32 and (
                    key <= 125 and len(self.input) < self.max_chars
                ):
                    self.input += chr(key)

                key = pr.get_char_pressed()

            if pr.is_key_pressed(pr.KEY_BACKSPACE) and self.input:
                self.input = self.input[:-1]

            if pr.is_key_pressed(pr.KEY_ESCAPE):
                self.enter_input = False

        else:

            pr.set_mouse_cursor(pr.MOUSE_CURSOR_DEFAULT)
            self.frame_counter = 0

    def display_widget(self) -> None:

        self.update_widget()

        pr.draw_rectangle(*self.textbox, pr.DARKGRAY)

        if self.is_in:
            line_color: pr.Color = self.cursor_color

        else:
            line_color = self.box_color

        pr.draw_rectangle_lines(*self.textbox, line_color)

        text_padding: int = (
            self.w + 5 - pr.measure_text(self.standin_input, self.font_size)
        )
        text_startx: int = self.x + text_padding
        text_starty: int = self.y + (self.h - self.font_size) // 2

        pr.draw_text(
            self.input,
            text_startx,
            text_starty,
            self.font_size,
            self.text_color
        )

        if (
            self.enter_input
        ) and (
            len(self.input) < self.max_chars
        ) and (
            (self.frame_counter // 20) % 2 == 0
        ):
            pr.draw_text(
                "_",
                text_startx + 5 + pr.measure_text(self.input, self.font_size),
                text_starty + 2,
                self.font_size,
                self.cursor_color
            )
