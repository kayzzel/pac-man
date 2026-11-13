import pyray as pr
from pyray import KeyboardKey as kek
from typing import Callable, Any
from pathlib import Path
from .View import View
from ..game.map.Map_scores import Map_scores
from ..game.map.Map_storing import get_stored_map_list
from .widget import Text, ButtonPanel, TextPanel, Dropdown


class Scores_view(View):

    def __init__(self, app, map_name: str = "mandatory") -> None:

        self.maps: list[str] = get_stored_map_list(app.map_folder)
        self.init_scores: bool = False
        self.load_new_scores(map_name, app.map_folder)
        self.init_scores = True
        super().__init__(app)

    def _update_title(self) -> None:

        self.title: Text = Text(
            f"BEST SCORES FOR {self.map_scores.map_name.upper()}",
            -2,
            self.h // 15,
            self.h // 10
        )
        self.widgets.append(self.title)

    def load_new_scores(self, map_name: str, map_folder: Path) -> None:

        self.map_scores: Map_scores = Map_scores(
            map_name,
            map_folder / map_name / "score.json"
        )
        self.scores: list[str] = [
            f"{i}. {pl.name} --- {pl.score}"
            for i, pl in enumerate(self.map_scores.scores)
        ]
        if not self.scores:
            self.scores.append("No scores yet")
        elif len(self.scores) < 10:
            self.scores += [" " for _ in range(10 - len(self.scores))]
        if self.init_scores:
            self.map_dropdown.invert_show()
            self._update(True)

    def _update_buttons(self) -> None:

        back_label: str = "back <-|"
        load_label: str = "Select a map"
        button_h: int = self.h // 20
        button_pad: int = button_h - button_h // 5

        back_w: int = (
            Text.measure_text(back_label, button_h)
        ) + button_pad
        load_w: int = self.w // 5

        self.back_button: ButtonPanel = ButtonPanel(
            self.w - back_w - self.w // 30,
            self.h - button_h - self.h // 40,
            back_w,
            button_h,
            {back_label: (self.app.return_to_prev_view, None)}
        )
        self.widgets.append(self.back_button)

        dropdown_buttons: dict[str, tuple[Callable, Any]] = {
            load_label: (lambda: 0, None)
        } | {
            map_name: (self.load_new_scores, (map_name, self.app.map_folder))
            for map_name in self.maps
        }
        self.map_dropdown: Dropdown = Dropdown(
            -2,
            self.title.y + self.title.font_size + self.h // 25,
            load_w,
            button_h,
            dropdown_buttons
        )

    def _update_scores(self) -> None:

        scores_start: int = self.map_dropdown.posy + self.map_dropdown.h
        scores_height: int = (
            self.h - scores_start
            - self.back_button.h - self.h // 30
        )
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

        if pr.is_key_pressed(kek.KEY_ESCAPE):
            self.app.return_to_prev_view()

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_title()
        self._update_buttons()
        self._update_scores()
