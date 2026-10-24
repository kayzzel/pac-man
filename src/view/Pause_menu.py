import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from typing import Callable, Any
from .View import View
from .Main_menu import Main_menu
from .Scores_view import Scores_view
from .Save_score_view import Save_score_view
from .widget import Text, ButtonPanel, TextPanel, ClickableIcon, Input_box


CHEAT_PASSWORD: str = "password"
PASSWORD_MSG_TIME: int = 120

BORDER_THICK: int = 5

LOCK_CLOSED_PATH: str = "src/view/assets/icons/lock_closed.jpg"
LOCK_OPEN_PATH: str = "src/view/assets/icons/lock_open.jpg"


class Pause_menu(View):

    def __init__(self, app, game, global_view: View) -> None:

        self.game = game
        self.global_view: View = global_view
        self.show_cheat_panel: bool = False

        self.nb_lives: int = self.game.config.lives
        self.pts_per_pacgum: int = self.game.config.point_per_pacgum
        self.pts_per_spacgum: int = self.game.config.point_per_super_pacgum
        self.pts_per_ghost: int = self.game.config.point_per_ghost
        self.invicible_mode: bool = False
        self.nowalls_mode: bool = False

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
                Scores_view(self.app)
            ),
            "Save and exit": (self.app.change_view, Save_score_view(self.app, self.game)),
            "Exit": (self.global_view.exit_game, Main_menu(self.app))
        }
        # button_font_sz: int = panel_height // (len(button_actions.keys()) * 2 - 1)

        self.left_panel: ButtonPanel = ButtonPanel(
            self.x + BORDER_THICK + self.w // 20 + (self.w // 2 - panel_width) // 2,
            -2,
            panel_width,
            panel_height,
            button_actions,
            (10, 2, 0.1)
        )

    def _update_cheat_panel(self) -> None:

        if not self.show_cheat_panel:
            return

        labels: dict[str, str] = {
            "nb_lives": f"number of lives ({self.nb_lives})",
            "pts_per_pacgum": f"points per pacgum ({self.pts_per_pacgum})",
            "pts_per_spacgum": f"points per super pacgum ({self.pts_per_spacgum})",
            "pts_per_ghost": f"points per ghost ({self.pts_per_ghost})",
            "invicible_mode": "invicible mode",
            "nowalls_mode": "pass through walls"
        }

        panel_width: int = self.w - self.left_panel.w - BORDER_THICK
        panel_height: int = self.left_panel.h

        self.cheat_panel: TextPanel = TextPanel(
            self.left_panel.posx + self.left_panel.w + BORDER_THICK,
            -2,
            panel_width // 2,
            panel_height,
            list(labels.values()),
            (0, 2, 0.1),
            panel_width // 12
        )
        self.input_boxes: dict[str, Input_box] = {
            parameter: Input_box(
                self.cheat_panel.posx + self.cheat_panel.w + panel_width // 8,
                self.cheat_panel.labels[labels[parameter]].posy,
                panel_width // 8,
                self.cheat_panel.font_size,
                (self.change_parameter, parameter),
                10,
                (48, 57)
            ) for parameter in list(labels.keys())[:-2]
        }
        self.onoff_buttons: dict[str, ButtonPanel] = {
            parameter: ButtonPanel(
                self.cheat_panel.posx + self.cheat_panel.w + panel_width // 8,
                self.cheat_panel.labels[labels[parameter]].posy,
                panel_width // 12,
                self.cheat_panel.font_size,
                {("off" if not getattr(self, parameter) else "on"): (self.change_onoff_button, parameter)},
                (0, 2, 0.1),
                -2
            ) for parameter in ["invicible_mode", "nowalls_mode"]
        }

    def change_parameter(self, parameter: str) -> None:

        if not hasattr(self, parameter):
            return
        setattr(self, parameter, self.input_boxes[parameter].input)
        self._update_cheat_panel()

    def change_onoff_button(self, parameter: str) -> None:

        if not hasattr(self, parameter):
            return
        setattr(self, parameter, not getattr(self, parameter))
        self._update_cheat_panel()

    def reset_input(self) -> None:

        self.show_input: bool = False
        self.show_message: str = ""
        self.lock_icon.y = -2

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
        self.reset_input()

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

            self.show_cheat_panel = True
            self.show_message = "Well done, little cheater :)"
            self.input_password.text_color = pr.GREEN
            self.input_password.cursor_color = pr.DARKGREEN
            self.lock_icon._load_image(LOCK_OPEN_PATH)
            self._update_cheat_panel()

        else:

            self.show_message = "Password incorrect, try again"
            self.input_password.text_color = pr.RED
            self.input_password.cursor_color = pr.MAROON

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self._update_left_panel()
        self._update_cheat_panel()
        self._update_lock_and_password()

    def display_view(self) -> None:

        self._update()

        outline: tuple[int, int, int, int] = (
            self.x, self.y, self.w, self.h
        )
        pr.draw_rectangle(*outline, pr.BLACK)
        pr.draw_rectangle_lines_ex(outline, BORDER_THICK, pr.RAYWHITE)

        self.left_panel.display_widget()

        if self.show_cheat_panel and self.frame_counter >= PASSWORD_MSG_TIME:

            self.show_input = False
            self.cheat_panel.display_widget()
            for input_box in self.input_boxes.values():
                input_box.display_widget()
            for button in self.onoff_buttons.values():
                button.display_widget()

        else:

            self.lock_icon.display_widget()

            if self.show_message:

                self.display_message()

            if self.show_input:

                self.input_password.display_widget()

    def display_message(self) -> None:

        if self.frame_counter < PASSWORD_MSG_TIME:

            message: Text = Text(
                self.show_message,
                self.x + self.w // 2,
                (
                    self.input_password.posy
                    + self.input_password.h
                    + self.h // 10
                ),
                self.h // 15,
                self.w // 2 - self.w // 6,
                self.input_password.text_color
            )
            message.x += (self.w // 2 - message.width) // 2
            message.display_widget()
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
