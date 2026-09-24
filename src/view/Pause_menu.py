import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from typing import Callable, Any
from .View import View
from .widget import RectPanel, ClickableIcon, Input_box


CHEAT_PASSWORD: str = "password"
PASSWORD_MSG_TIME: int = 120

BUTTON_FONT_SIZE: int = 20
PANEL_PADDING: int = BUTTON_FONT_SIZE - 5

LOCK_CLOSED_PATH: str = "src/view/assets/icons/lock_closed.jpg"
LOCK_OPEN_PATH: str = "src/view/assets/icons/lock_open.jpg"


class Pause_menu(View):

    def __init__(self, app) -> None:

        super().__init__(app)
        self.show_right_panel: bool = False

    @property
    def w(self) -> int:

        return sw() - sw() // 8

    @property
    def h(self) -> int:

        return sh() - sh() // 8

    def _update_left_panel(self) -> None:

        self.button_actions: dict[str, tuple[Callable, Any]] = {
            "Resume": (self.app.return_to_prev_view, None),
            "Options": (lambda: print(
                "Action for button 'options' not yet coded\n"
            ), None),
            "Scores": (lambda: print(
                "Action for button 'scores' not yet coded\n"
            ), None),
            "Save and exit": (self.app.change_view, "save_score_view"),
            "Exit": (self.app.change_view, "main_menu")
        }

        self.calculate_panel_spacing()
        vertical_padding: int = self.h // 12

        self.left_panel: RectPanel = RectPanel(
            self.x + (self.w // 2 - self.left_panel_w) // 2,
            self.y + vertical_padding,
            self.left_panel_w,
            (self.h - vertical_padding * 2),
            self.button_actions,
            self.but_font_sz,
            self.panel_pad
        )

    def calculate_panel_spacing(self) -> None:

        max_label: str = max(
            self.button_actions.keys(),
            key=lambda label: len(label)
        )

        self.but_font_sz: int = BUTTON_FONT_SIZE
        self.panel_pad: int = PANEL_PADDING

        self.left_panel_w: int = pr.measure_text(
            max_label,
            self.but_font_sz,
        ) + self.panel_pad
        while self.left_panel_w >= self.w // 2 and self.but_font_sz >= 5:
            self.but_font_sz -= 1
            self.left_panel_w = pr.measure_text(
                max_label,
                self.but_font_sz,
            ) + self.panel_pad

        self.left_panel_w = max(
            self.left_panel_w,
            self.w // 2 - self.w // 10
        )

    def _update_lock_and_password(self) -> None:

        lock_width: int = self.w // 2 // 3

        self.lock_icon: ClickableIcon = ClickableIcon(
            self.x + self.w // 2 + (self.w // 2 - lock_width) // 2,
            -2,
            LOCK_CLOSED_PATH,
            (self.show_input_box, None),
            (lock_width, lock_width),
            True
        )

        input_width: int = self.w // 2 - self.w // 8

        self.input_password: Input_box = Input_box(
            self.x + self.w // 2 + (self.w // 2 - input_width) // 2,
            self.h // 3 + self.lock_icon.h + 10,
            input_width,
            self.h // 8,
            20,
            (self.validate_password, None)
        )

        self.show_input: bool = False
        self.show_message: str = ""

    def show_input_box(self) -> None:

        self.show_input = not self.show_input

        if not self.show_input:
            self.input_password.input = ""

        self.lock_icon.y = (
            -2
            if self.lock_icon.y == -3
            else -3
        )

    def validate_password(self) -> None:

        self.frame_counter: int = 0

        if self.input_password.input == CHEAT_PASSWORD:

            self.show_right_panel = True
            self.show_message: str = "Well done, little cheater :)"
            self.input_password.text_color = pr.GREEN
            self.input_password.cursor_color = pr.DARKGREEN
            self.lock_icon._load_image(LOCK_OPEN_PATH)

        else:

            self.show_message = "Password incorrect, try again"
            self.input_password.text_color = pr.RED
            self.input_password.cursor_color = pr.MAROON

    def _update(self) -> None:

        if not pr.is_window_resized() and self.is_init:
            return

        self._update_left_panel()
        self._update_lock_and_password()
        self.is_init = True

    def display_view(self) -> None:

        self._update()

        outline: tuple[int, int, int, int] = (
            self.x, self.y, self.w, self.h
        )
        pr.draw_rectangle(*outline, pr.BLACK)
        pr.draw_rectangle_lines_ex(outline, 5, pr.RAYWHITE)

        self.left_panel.display_widget()

        if self.show_right_panel and self.frame_counter >= PASSWORD_MSG_TIME:

            self.show_input = False

        else:

            self.lock_icon.display_widget()

            if self.show_message:

                self.display_message()

            if self.show_input:

                self.input_password.display_widget()

    def display_message(self) -> None:

        if self.frame_counter < PASSWORD_MSG_TIME:

            message_width: int = (self.w // 2 - pr.measure_text(
                self.show_message,
                self.h // 20
            )) // 2
            pr.draw_text(
                self.show_message,
                self.x + self.w // 2 + message_width,
                (
                    self.input_password.posy
                    + self.input_password.h
                    + self.h // 10
                ),
                self.h // 20,
                self.input_password.text_color
            )
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.input_password.text_color = (
                self.input_password.base_colors[1]
            )
            self.input_password.cursor_color = (
                self.input_password.base_colors[2]
            )
            self.lock_icon._load_image(LOCK_CLOSED_PATH)
