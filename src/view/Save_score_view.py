import pyray as pr
from .View import View
from .widget import Widget, Text, Input_box, Panel


MAX_INPUT_LENGTH: int = 20

MSG_DISPLAY_TIME: int = 120

NAME_CHAR_RANGE: tuple[int, int] = (32, 125)
SCORE_CHAR_RANGE: tuple[int, int] = (48, 57)


class Save_score_view(View):

    def __init__(self, app, game) -> None:

        self.game = game
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
        back_font_sz: int = self.h // 20
        back_padding: int = back_font_sz - 5

        back_width: int = (
            pr.measure_text(back_label, back_font_sz)
        ) + back_padding
        back_height: int = back_font_sz + back_padding

        self.back_button: Panel = Panel(
            self.w - back_width - 10,
            self.h - back_height - 10,
            back_width,
            back_height,
            {back_label: (self.app.return_to_prev_view, None)}
        )
        self.widgets.append(self.back_button)

    def _update_input_box(self) -> None:

        self.input_box: Input_box = Input_box(
            -2,
            -2,
            self.w // 3,
            self.h // 8,
            MAX_INPUT_LENGTH,
            NAME_CHAR_RANGE,
            (self.save_name, None)
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

        if pr.is_key_pressed(pr.KEY_ESCAPE) and not self.show_message:
            self.app.return_to_prev_view()

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_back_button()
        self._update_input_box()

    def save_name(self) -> None:

        self.player_name: str = self.input_box.input
        self.game.scores.add_scores(self.player_name, self.game.player.score)
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

            max_msg: str = max(self.show_message, key=lambda msg: len(msg))
            msg_font_sz: int = Text._resize_font(max_msg, self.h // 25, self.w - self.w // 3)

            msg_y: int = self.input_box.posy + self.input_box.h + self.h // 15

            for msg in self.show_message:

                msg_x: int = (self.w - pr.measure_text(
                    msg,
                    msg_font_sz
                )) // 2
                pr.draw_text(
                    msg,
                    msg_x,
                    msg_y,
                    msg_font_sz,
                    pr.GREEN
                )
                msg_y += msg_font_sz + msg_font_sz // 2

            self.msg_frame_counter += 1

        else:

            self.show_message = []
            self.app.change_view("main_menu")
