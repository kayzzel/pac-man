import pyray as pr
from .View import View
from .widget import Input_box, Panel


MAX_INPUT_LENGTH: int = 20

MSG_DISPLAY_TIME: int = 120

NAME_CHAR_RANGE: tuple[int, int] = (32, 125)
SCORE_CHAR_RANGE: tuple[int, int] = (48, 57)


class Save_score_view(View):

    def __init__(self, app, game) -> None:

        super().__init__(app)
        self.game = game

        self.show_message: list[str] = []

    def _update_title(self) -> None:

        self.title: str = "SAVE SCORE"
        self.title_font_sz: int = self.h // 10
        self.title_y: int = self.h // 12
        self.title_x: int = (
            self.w - pr.measure_text(self.title, self.title_font_sz)
        ) // 2

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
            {back_label: (self.app.return_to_prev_view, None)},
            back_font_sz,
            (back_padding, 2, 0.1)
        )

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
        self.input_text: str = "enter name : "
        self.input_box.enter_input = True
        self.input_font_sz: int = self.h // 16
        self.input_x: int = (self.w - pr.measure_text(
            self.input_text,
            self.input_font_sz
        )) // 2
        self.input_y: int = (
            self.input_box.posy
            - self.input_font_sz
            - self.h // 20
        )

    def _update(self) -> None:

        if not pr.is_window_resized() and self.is_init:
            return

        self._update_title()
        self._update_back_button()
        self._update_input_box()
        self.is_init = True

    def save_name(self) -> None:

        self.player_name: str = self.input_box.input
        self.game.scores.add_scores(self.player_name, self.game.player.score)
        self.input_text = ""
        self.show_message = [
            "Successfully saved ",
            f"the score {self.game.player.score}",
            f" for player {self.player_name}!"
        ]
        self.msg_frame_counter: int = 0

    def display_view(self) -> None:

        self._update()

        pr.draw_text(
            self.title,
            self.title_x,
            self.title_y,
            self.title_font_sz,
            pr.RAYWHITE
        )

        if self.input_text:
            pr.draw_text(
                self.input_text,
                self.input_x,
                self.input_y,
                self.input_font_sz,
                pr.LIGHTGRAY
            )

        self.back_button.display_widget()

        self.input_box.display_widget()

        if self.show_message:
            self.display_message()

    def display_message(self) -> None:

        if self.msg_frame_counter < MSG_DISPLAY_TIME:

            msg_font_sz: int = self.h // 25
            max_msg: str = max(self.show_message, key=lambda msg: len(msg))

            while (
                pr.measure_text(max_msg, msg_font_sz) > self.w - self.w // 3
                and msg_font_sz >= 5
            ):
                msg_font_sz -= 1

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
