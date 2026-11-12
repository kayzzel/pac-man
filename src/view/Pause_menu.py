import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from typing import Callable, Any
from ..game.Game import Game
from .View import View
from .Scores_view import Scores_view
from .Save_score_view import Save_score_view
from .Options_menu import Options_menu
from .widget import Text, ButtonPanel, TextPanel, ClickableIcon, Input_box


CHEAT_PASSWORD: str = "password"
PASSWORD_MSG_TIME: int = 120

BORDER_THICK: int = 5

LOCK_CLOSED_PATH: str = "src/view/assets/icons/lock_closed.jpg"
LOCK_OPEN_PATH: str = "src/view/assets/icons/lock_open.jpg"


class Pause_menu(View):

    def __init__(self, app, game: Game, global_view: View) -> None:

        self.game: Game = game
        self.global_view: View = global_view
        self.show_cheat_panel: bool = False

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
            "Options": (self.app.change_view, Options_menu(self.app)),
            "Scores": (
                self.app.change_view,
                Scores_view(self.app)
            ),
            "Save and exit": (
                self.app.change_view,
                Save_score_view(self.app, self.game)
            ),
            "Exit": (self.global_view.exit_game, "main_menu")
        }

        self.left_panel: ButtonPanel = ButtonPanel(
            (
                self.x + BORDER_THICK + self.w // 20
                + (self.w // 2 - panel_width) // 2
            ),
            -2,
            panel_width,
            panel_height,
            button_actions,
            (10, 2, 0.1)
        )
        self.widgets.append(self.left_panel)

    @property
    def invincible_state(self) -> str:

        return (
            "on" if self.game.cheats.is_invincible
            else "off"
        )

    @property
    def clipping_state(self) -> str:

        return (
            "on" if self.game.cheats.is_clipping
            else "off"
        )

    def _update_cheat_panel(self) -> None:

        if not self.show_cheat_panel:
            return

        labels: dict[str, str] = {
            "nb_lives": f"number of lives ({self.game.player.nb_lives})",
            "score": f"score ({self.game.player.score})",
            "invincible_mode": f"invincible mode ({self.invincible_state})",
            "nowalls_mode": f"pass through walls ({self.clipping_state})"
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
                {cur_value: (self.change_onoff, parameter)},
                (0, 2, 0.1),
                -2
            ) for parameter, cur_value in {
                "invincible_mode": self.invincible_state,
                "nowalls_mode": self.clipping_state
            }.items()
        }
        self.widgets.append(self.cheat_panel)
        self.widgets += list(self.input_boxes.values())
        self.widgets += list(self.onoff_buttons.values())

    def change_parameter(self, parameter: str) -> None:

        function: Callable
        if parameter == "nb_lives":
            function = self.game.cheats.change_lives
            self.global_view.life_icon_init = False
        elif parameter == "score":
            function = self.game.cheats.change_points
        elif (
            parameter not in self.input_boxes.keys()
            or not self.input_boxes[parameter].input.isdigit()
        ):
            return
        function(int(self.input_boxes[parameter].input))
        self._update_cheat_panel()

    def change_onoff(self, parameter: str) -> None:

        if parameter == "invincible_mode":
            function = self.game.cheats.toggle_invincible
        elif parameter == "nowalls_mode":
            function = self.game.cheats.toggle_clipping
        elif parameter not in self.onoff_buttons.keys():
            return
        function()
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
            (self.validate_password, None),
            20,
            (32, 125)
        )
        self.widgets += [self.lock_icon, self.input_password]
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

        super()._update(True)
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
