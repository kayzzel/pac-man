import pyray as pr
from typing import Callable, Any
from .Widget import Widget
from .Text import Text


MAX_INPUT_CHARS: int = 10

DEFAULT_COLOR: pr.Color = pr.GRAY
TEXT_COLOR: pr.Color = pr.LIGHTGRAY
CURSOR_COLOR: pr.Color = pr.RAYWHITE


class Input_box(Widget):

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        action: tuple[Callable, Any] = (lambda: 0, None),
        max_chars: int = MAX_INPUT_CHARS,
        char_range: tuple[int, int] = (32, 125),
        colors: tuple[pr.Color, pr.Color, pr.Color] = (
            DEFAULT_COLOR,
            TEXT_COLOR,
            CURSOR_COLOR
        )
    ) -> None:

        super().__init__(x, y, width, height)

        self.textbox: tuple[int, int, int, int] = (
            self.posx, self.posy, self.w, self.h
        )
        self.char_range: tuple[int, int] = char_range
        self.max_chars: int = max_chars
        self.standin_input: str = "h" * max_chars
        self.base_colors: tuple[pr.Color, pr.Color, pr.Color] = colors
        self.box_color: pr.Color
        self.text_color: pr.Color
        self.cursor_color: pr.Color
        self.box_color, self.text_color, self.cursor_color = colors

        self.input: str = ""
        self.enter_input: bool = False
        self.frame_counter: int = 0

        self.action: tuple[Callable, Any] = action

    def _update_widget(self) -> None:

        if self.is_pressed and not self.enter_input:
            self.enter_input = True

        if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT) and not self.is_in:
            self.enter_input = False

        if self.enter_input:

            pr.set_mouse_cursor(pr.MOUSE_CURSOR_IBEAM)
            self.frame_counter += 1

            self.key: int = pr.get_char_pressed()

            while self.key > 0:

                if self.key >= self.char_range[0] and (
                    self.key <= self.char_range[1]
                    and len(self.input) < self.max_chars
                ):
                    self.input += chr(self.key)

                if len(self.input) > 1:
                    self.key = pr.get_char_pressed()

            if pr.is_key_pressed(pr.KEY_BACKSPACE) and self.input:
                self.input = self.input[:-1]

            if pr.is_key_pressed(pr.KEY_ESCAPE):
                self.enter_input = False

            if pr.is_key_pressed(pr.KEY_ENTER):
                self.call_action()

        else:

            pr.set_mouse_cursor(pr.MOUSE_CURSOR_DEFAULT)
            self.frame_counter = 0

    def display_widget(self) -> None:

        self._update_widget()

        pr.draw_rectangle(*self.textbox, pr.DARKGRAY)

        if self.is_in:
            line_color: pr.Color = self.cursor_color

        else:
            line_color = self.box_color

        pr.draw_rectangle_lines(*self.textbox, line_color)

        text_padding: int = self.w // 8

        user_input: Text = Text(
            self.input,
            self.posx + text_padding,
            self.posy,
            self.h - self.h // 8,
            self.w - text_padding * 2,
            self.text_color
        )
        user_input.y += (self.h - user_input.font_size) // 2
        user_input.display_widget()

        if (
            self.enter_input
        ) and (
            len(self.input) < self.max_chars
        ) and (
            (self.frame_counter // 20) % 2 == 0
        ):
            pr.draw_text_ex(
                Text.font,
                "_",
                (user_input.x + 5 + user_input.width, user_input.y + 2),
                float(user_input.font_size),
                Text.spacing,
                self.cursor_color
            )
