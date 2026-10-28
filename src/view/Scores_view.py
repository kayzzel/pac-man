import pyray as pr
from typing import Callable, Any
from pathlib import Path
from .View import View
from ..game.map.Map_scores import Map_scores
from .widget import Widget, Text, ButtonPanel, TextPanel, Dropdown


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

    def __init__(self, app, map_name: str = "mandatory") -> None:

        self.load_new_scores(map_name, app.map_folder)
        super().__init__(app)

    def _update_title(self) -> None:

        self.title: Text = Text(
            "BEST SCORES",
            -2,
            self.h // 15,
            self.h // 10
        )
        self.widgets.append(self.title)

    def load_new_scores(self, map_name: str, map_folder: Path) -> None:

        print(f"Loading the scores for map '{map_name}'...\n")
        self.map_scores: Map_scores = Map_scores(map_name, map_folder / map_name / "score.json")
        self.scores: list[str] = [
            pl_name + ": " + str(pl_score)
            for pl_name, pl_score in self.map_scores.scores.items()
        ]
        self.map_dropdown.invert_show()

    def _update_buttons(self) -> None:

        back_label: str = "back <-|"
        load_label: str = "Select a map"
        button_font_sz: int = self.h // 20
        button_padding: int = button_font_sz - 5

        back_width: int = (
            int(pr.measure_text_ex(Text.font, back_label, button_font_sz, Text.spacing).x)
        ) + button_padding
        load_width: int = self.w // 5
        button_height: int = button_font_sz + button_padding

        self.back_button: ButtonPanel = ButtonPanel(
            self.w - back_width - 10,
            self.h - button_height - 10,
            back_width,
            button_height,
            {back_label: (self.app.return_to_prev_view, None)},
            (button_padding // 2, 2, 0.1)
        )
        self.widgets.append(self.back_button)

        dropdown_buttons: dict[str, tuple[Callable, Any]] = {
            load_label: (lambda: 0, None)
        } | {
            map_name: (self.load_new_scores, (map_name, self.app.map_folder))
            for map_name in DEFAULT_MAPS
        }
        self.map_dropdown: Dropdown = Dropdown(
            -2,
            self.title.y + self.title.font_size + self.h // 25,
            load_width,
            button_height,
            dropdown_buttons
        )

    def _update_scores(self) -> None:

        scores_start: int = self.map_dropdown.posy + self.map_dropdown.h
        scores_height: int = self.h - scores_start - self.back_button.h - 10
        padding: int = scores_height // 8

        self.score_panel: TextPanel = TextPanel(
            -2,
            scores_start,
            self.w // 3,
            scores_height,
            self.scores,
            (padding, 2, 0.1)
        )
        self.widgets += [self.score_panel, self.map_dropdown]

    def _update(self, forced: bool = False) -> None:

        if pr.is_key_pressed(pr.KEY_ESCAPE):
            self.app.return_to_prev_view()

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_buttons()
        self._update_scores()
