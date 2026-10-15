import pyray as pr
from typing import Callable, Any
from .View import View
from .widget import Widget, Text, Panel, Dropdown


DEFAULT_MAPS: list[str] = ["MANDATORY", "ARCADE", "CUSTOM", "ADDONE", "ADDTWO", "ADDTHREE", "ADDFOUR", "ADDFIVE", "ADDSIX"]

TEST_SCORES: dict[str, int] = {
    "figue": 123456789,
    "banane": 12345678,
    "mirabelle": 1234567,
    "pomme": 123456,
    "pêche": 12345,
    "abricot": 1234
}


class Scores_view(View):

    def __init__(self, app, scores: dict[str, int] = TEST_SCORES) -> None:

        self.scores: list[str] = [
            pl_name + ": " + str(pl_score)
            for pl_name, pl_score in scores.items()
        ]
        super().__init__(app)

    def _update_title(self) -> None:

        self.title: Text = Text(
            "BEST SCORES",
            -2,
            self.h // 15,
            self.h // 10
        )
        self.widgets.append(self.title)

    def load_new_scores(self, map_name: str) -> None:

        print(f"Loading the scores for map '{map_name}'...\n")
        self.map_dropdown.invert_show()

    def _update_buttons(self) -> None:

        back_label: str = "back <-|"
        load_label: str = "Select a map"
        button_font_sz: int = self.h // 20
        button_padding: int = button_font_sz - 5

        back_width: int = (
            pr.measure_text(back_label, button_font_sz)
        ) + button_padding
        load_width: int = self.w // 5
        button_height: int = button_font_sz + button_padding

        self.back_button: Panel = Panel(
            self.w - back_width - 10,
            self.h - button_height - 10,
            back_width,
            button_height,
            {back_label: (self.app.return_to_prev_view, None)}
        )
        self.widgets.append(self.back_button)

        main_button: dict[str, tuple[Callable, Any]] = {
            load_label: (lambda: 0, None)
        }
        dropdown_buttons: dict[str, tuple[Callable, Any]] = {
            map_name: (self.load_new_scores, map_name)
            for map_name in DEFAULT_MAPS
        }
        main_button.update(dropdown_buttons)
        self.map_dropdown: Dropdown = Dropdown(
            -2,
            self.title.y + self.title.font_size + self.h // 25,
            load_width,
            button_height,
            main_button
        )

    def _update_scores(self) -> None:

        scores_start: int = self.map_dropdown.posy + self.map_dropdown.h

        scores_height: int = self.h - scores_start - self.back_button.h - 10

        padding: int = scores_height // 8
        space_remaining: int = scores_height - padding * 2

        score_y: int = scores_start + padding

        max_score: str = max(self.scores, key=lambda score: len(score))
        score_font_sz: int = Text._resize_font(
            max_score,
            space_remaining // (len(self.scores) * 2 - 1)
        )
        score_y -= score_font_sz

        for i, score in enumerate(self.scores):

            self.widgets.append(Text(
                score,
                -2,
                score_y + score_font_sz * i + score_font_sz * (i + 1),
                score_font_sz
            ))

        self.widgets.append(self.map_dropdown)

    def _update(self, forced: bool = False) -> None:

        if pr.is_key_pressed(pr.KEY_ESCAPE):
            self.app.return_to_prev_view()

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_buttons()
        self._update_scores()
