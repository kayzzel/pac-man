import pyray as pr
from pyray import KeyboardKey as kek
from pyray import MouseButton as mb
from pyray import MouseCursor as mc
from typing import Callable, Any
from .Widget import Widget
from .Text import Text
from .Icon import Icon
from .Dropdown import ARROW_UP_PATH, ARROW_DOWN_PATH


MAX_INPUT_CHARS: int = 10

DEFAULT_COLOR: pr.Color = pr.GRAY
TEXT_COLOR: pr.Color = pr.LIGHTGRAY
CURSOR_COLOR: pr.Color = pr.RAYWHITE

ARROW_LEFT_PATH: str = "src/view/assets/icons/arrow_left.png"
ARROW_RIGHT_PATH: str = "src/view/assets/icons/arrow_right.png"


class Input_box(Widget):

    # a simple input box with a validating function to call at the end

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
        self.standin_input: str = "w" * max_chars
        self.font_size: int = Text._resize_font(
            self.standin_input,
            self.h - self.h // 3,
            self.w - self.w // 8
        )

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

        # if click inside text box for first time, input activated
        if self.is_pressed and not self.enter_input:
            self.enter_input = True

        # if click outside the box, input deactivated

        if pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT) and not self.is_in:
            self.enter_input = False

        if self.enter_input:

            pr.set_mouse_cursor(mc.MOUSE_CURSOR_IBEAM)
            self.frame_counter += 1

            key: int = pr.get_char_pressed()

            while key > 0:

                if key >= self.char_range[0] and (
                    key <= self.char_range[1]
                    and len(self.input) < self.max_chars
                ):
                    self.input += chr(key)

                key = pr.get_char_pressed()

            if pr.is_key_pressed(kek.KEY_BACKSPACE) and self.input:
                self.input = self.input[:-1]

            if pr.is_key_pressed(kek.KEY_ESCAPE):
                self.enter_input = False

            if pr.is_key_pressed(kek.KEY_ENTER):
                self.call_action()

        else:

            pr.set_mouse_cursor(mc.MOUSE_CURSOR_DEFAULT)
            self.frame_counter = 0

    def display_widget(self) -> None:

        self._update_widget()

        pr.draw_rectangle(*self.textbox, pr.DARKGRAY)

        if self.is_in:
            line_color: pr.Color = self.cursor_color

        else:
            line_color = self.box_color

        pr.draw_rectangle_lines(*self.textbox, line_color)

        text_padding: int = (
            self.w + self.w // 8
            - Text.measure_text(self.standin_input, self.font_size)
        )

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

        # displays a blinking cursor in input box

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


class Keybind_input_box(Input_box):

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

        super().__init__(
            x, y, width, height, action, max_chars, char_range, colors
        )
        self._update_keys()

    def _update_keys(self) -> None:

        icon_size: int = self.h - self.h // 3
        icon_x: int = self.posx + (self.w - icon_size) // 2
        icon_y: int = self.posy + (self.h - icon_size) // 2
        self.keys: dict[int, Widget] = {
            kek.KEY_UP: Icon(
                icon_x, icon_y, ARROW_UP_PATH, (icon_size, icon_size), True
            ),
            kek.KEY_DOWN: Icon(
                icon_x, icon_y, ARROW_DOWN_PATH, (icon_size, icon_size), True
            ),
            kek.KEY_RIGHT: Icon(
                icon_x, icon_y, ARROW_RIGHT_PATH, (icon_size, icon_size), True
            ),
            kek.KEY_LEFT: Icon(
                icon_x, icon_y, ARROW_LEFT_PATH, (icon_size, icon_size), True
            )
        }
        self.display_key: int = 0

    def _update_widget(self) -> None:

        # if click inside text box for first time, input activated
        if self.is_pressed and not self.enter_input:
            self.enter_input = True

        # if click outside the box, input deactivated

        if pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT) and not self.is_in:
            self.enter_input = False

        if self.enter_input:

            pr.set_mouse_cursor(mc.MOUSE_CURSOR_IBEAM)
            self.frame_counter += 1

            key: int = pr.get_char_pressed()

            while key > 0:

                if key >= self.char_range[0] and (
                    key <= self.char_range[1]
                    and len(self.input) < self.max_chars
                ):
                    self.display_key = key
                    break

                key = pr.get_char_pressed()

            if pr.is_key_pressed(kek.KEY_BACKSPACE) and self.input:
                self.display_key = 0

            if pr.is_key_pressed(kek.KEY_ESCAPE):
                self.enter_input = False
                self.display_key = 0

            if pr.is_key_pressed(kek.KEY_ENTER):
                self.call_action()
                self.display_key = 0

        else:

            pr.set_mouse_cursor(mc.MOUSE_CURSOR_DEFAULT)
            self.frame_counter = 0

    def display_widget(self) -> None:

        self._update_widget()

        pr.draw_rectangle(*self.textbox, pr.DARKGRAY)

        if self.is_in or self.enter_input:
            line_color: pr.Color = self.cursor_color

        else:
            line_color = self.box_color

        pr.draw_rectangle_lines(*self.textbox, line_color)

        if self.display_key == 0:
            return

        if self.display_key not in self.keys.keys():

            new_key: Text = Text(
                chr(self.display_key),
                self.posx,
                self.posy,
                self.h - self.h // 3,
                self.w - self.w // 8
            )
            new_key.x += (self.w - new_key.width) // 2
            new_key.y += (self.h - new_key.font_size) // 2
            self.keys[self.display_key] = new_key

        self.keys[self.display_key].display_widget()

        # displays a blinking cursor in input box

        # if (
        #     self.enter_input
        # ) and (
        #     len(self.input) < self.max_chars
        # ) and (
        #     (self.frame_counter // 20) % 2 == 0
        # ):
        #     pr.draw_text_ex(
        #         Text.font,
        #         "_",
        #         (user_input.x + 5 + user_input.width, user_input.y + 2),
        #         float(user_input.font_size),
        #         Text.spacing,
        #         self.cursor_color
        #     )
