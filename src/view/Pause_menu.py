import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from typing import Callable, Any
from .View import View
from .Scores_view import Scores_view
from .Save_score_view import Save_score_view
from .widget import Panel, ClickableIcon, Input_box


CHEAT_PASSWORD: str = "password"
PASSWORD_MSG_TIME: int = 120

BORDER_THICK: int = 5

LOCK_CLOSED_PATH: str = "src/view/assets/icons/lock_closed.jpg"
LOCK_OPEN_PATH: str = "src/view/assets/icons/lock_open.jpg"

TEST_SCORES: dict[str, int] = {
    "figue": 123456789,
    "banane": 12345678,
    "mirabelle": 1234567,
    "pomme": 123456,
    "pêche": 12345,
    "abricot": 1234
}


class Pause_menu(View):

    def __init__(self, app, game, global_view: View) -> None:

        self.game = game
        self.global_view: View = global_view
        self.show_right_panel: bool = False
        super().__init__(app)

    @property
    def w(self) -> int:

        return sw() - sw() // 8

    @property
    def h(self) -> int:

        return sh() - sh() // 8

    def _update_left_panel(self) -> None:

        panel_width: int = self.w // 2 - self.w // 8
        panel_height: int = self.h - self.h // 3

        button_actions: dict[str, tuple[Callable, Any]] = {
            "Resume": (self.global_view.pause_or_resume, None),
            "Options": (lambda: print(
                "Action for button 'options' not yet coded\n"
            ), None),
            "Scores": (
                self.app.change_view,
                Scores_view(self.app, TEST_SCORES)
            ),
            "Save and exit": (self.app.change_view, Save_score_view(self.app, self.game)),
            "Exit": (self.app.change_view, "main_menu")
        }
        button_font_sz: int = panel_height // (len(button_actions.keys()) * 2 - 1)

        self.left_panel: Panel = Panel(
            self.x + BORDER_THICK + self.w // 20 + (self.w // 2 - panel_width) // 2,
            -2,
            panel_width,
            panel_height,
            button_actions,
            (10, 2, 0.1)
        )

    # def calculate_panel_spacing(self) -> None:

    #     max_label: str = max(
    #         self.button_actions.keys(),
    #         key=lambda label: len(label)
    #     )

    #     self.but_font_sz: int = BUTTON_FONT_SIZE
    #     self.panel_pad: int = PANEL_PADDING

    #     self.left_panel_w: int = pr.measure_text(
    #         max_label,
    #         self.but_font_sz,
    #     ) + self.panel_pad
    #     while self.left_panel_w >= self.w // 2 and self.but_font_sz >= 5:
    #         self.but_font_sz -= 1
    #         self.left_panel_w = pr.measure_text(
    #             max_label,
    #             self.but_font_sz,
    #         ) + self.panel_pad

    #     self.left_panel_w = max(
    #         self.left_panel_w,
    #         self.w // 2 - self.w // 10
    #     )

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
            (32, 125),
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
            self.show_message = "Well done, little cheater :)"
            self.input_password.text_color = pr.GREEN
            self.input_password.cursor_color = pr.DARKGREEN
            self.lock_icon._load_image(LOCK_OPEN_PATH)

        else:

            self.show_message = "Password incorrect, try again"
            self.input_password.text_color = pr.RED
            self.input_password.cursor_color = pr.MAROON

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self._update_left_panel()
        self._update_lock_and_password()

    def display_view(self) -> None:

        self._update()

        outline: tuple[int, int, int, int] = (
            self.x, self.y, self.w, self.h
        )
        pr.draw_rectangle(*outline, pr.BLACK)
        pr.draw_rectangle_lines_ex(outline, BORDER_THICK, pr.RAYWHITE)

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
