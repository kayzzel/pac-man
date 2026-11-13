import pyray as pr
from pyray import KeyboardKey as kek
from ..game.Game import Game
from .View import View
from .widget import Text, Input_box, ButtonPanel


MAX_INPUT_LENGTH: int = 20

MSG_DISPLAY_TIME: int = 80


class Save_score_view(View):

    def __init__(self, app, game: Game) -> None:

        self.game: Game = game
        self.show_message: list[str] = []
        super().__init__(app)

    def _update_title(self) -> None:

        self.title: Text = Text(
            "SAVE SCORE",
            -2,
            self.h // 12,
            self.h // 10
        )
        self.widgets.append(self.title)

    def _update_back_button(self) -> None:

        back_label: str = "back <-|"
        back_width: int = self.w // 8
        back_height: int = self.h // 15

        self.back_button: ButtonPanel = ButtonPanel(
            self.w - back_width - self.w // 25,
            self.h - back_height - self.h // 40,
            back_width,
            back_height,
            {back_label: (self.app.return_to_prev_view, None)}
        )
        self.widgets.append(self.back_button)

    def _update_input_box(self) -> None:

        all_characters: list[int] = []
        for crange in [(48, 58), (65, 91), (97, 123)]:
            all_characters += [i for i in range(*crange)]

        self.input_box: Input_box = Input_box(
            -2,
            -2,
            self.w // 3,
            self.h // 8,
            (self.save_name, None),
            MAX_INPUT_LENGTH,
            all_characters
        )
        self.input_box.enter_input = True
        self.widgets.append(self.input_box)

        self.input_text: Text = Text(
            "enter name : ",
            -2,
            (
                self.input_box.posy
                - self.h // 16
                - self.h // 20
            ),
            self.h // 16,
            self.w,
            pr.LIGHTGRAY
        )

    def _update(self, forced: bool = False) -> None:

        if pr.is_key_pressed(kek.KEY_ESCAPE) and not self.show_message:
            self.app.return_to_prev_view()

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_title()
        self._update_back_button()
        self._update_input_box()

    def save_name(self) -> None:

        self.player_name: str = self.input_box.input
        self.game.scores.add_score(self.player_name, self.game.player.score)
        self.input_text.label = ""
        self.show_message = [
            "Successfully saved ",
            f"the score {self.game.player.score}",
            f" for player {self.player_name}!"
        ]
        self.msg_frame_counter: int = 0

    def display_view(self) -> None:

        self._update()

        if self.input_text.label:
            self.widgets.append(self.input_text)

        for widget in self.widgets:
            widget.display_widget()

        if self.show_message:
            self.display_message()

    def display_message(self) -> None:

        if self.msg_frame_counter < MSG_DISPLAY_TIME:

            msg_y: int = self.input_box.posy + self.input_box.h + self.h // 15

            for msg in self.show_message:

                text: Text = Text(
                    msg,
                    -2,
                    msg_y,
                    self.h // 25,
                    self.w - self.w // 3
                )

                text.display_widget()
                msg_y += text.font_size + text.font_size // 2

            self.msg_frame_counter += 1

        else:

            self.show_message = []
            self.app.change_view("main_menu")
