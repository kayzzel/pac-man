import pyray as pr
from .View import View
from .Save_score_view import Save_score_view
from .Main_menu import Main_menu
from ..game.Game import Game
from .widget import Widget, ButtonPanel, TextPanel, Text


class Endgame_view(View):

    def __init__(self, app, game: Game, scores: dict[str, int], state: bool) -> None:

        self.state: bool = state
        self.game: Game = game
        self.scores: list[str] = [
            pl_name + ": " + str(pl_score)
            for pl_name, pl_score in scores.items()
        ]
        super().__init__(app)

    def _update_title(self) -> None:

        self.title: Text = Text(
            (
                "VICTORY" if self.state
                else "GAME OVER"
            ),
            -2,
            self.h // 25,
            self.h // 10
        )

        self.score: Text = Text(
            "SCORE: " + str(6969696969),
            -2,
            self.title.lowerbound + self.h // 25,
            self.h // 15
        )

        self.highscore: Text = Text(
            "Highscores",
            -2,
            self.score.lowerbound + self.h // 15,
            self.h // 20
        )

        self.widgets += [self.title, self.score, self.highscore]

    def _update_buttons(self) -> None:

        button_fontsz: int = Text._resize_font("save", self.h // 20, self.w // 5)
        button_width: int = pr.measure_text("save", button_fontsz) + (button_fontsz - 5)
        button_height: int = button_fontsz + button_fontsz - 5
        space_remaining: int = self.w - (button_width * 2)
        padding: int = space_remaining // 3
        button_y: int = self.h - self.h // 25 - button_height

        self.save_button: ButtonPanel = ButtonPanel(
            padding,
            button_y,
            button_width,
            button_height,
            {"save": (self.app.change_view, Save_score_view(self.app, self.game))},
            ((button_fontsz - 5) // 2, 2, 0.1)
        )
        self.exit_button: ButtonPanel = ButtonPanel(
            self.w - padding - button_width,
            button_y,
            button_width,
            button_height,
            {"exit": (self.app.change_view, Main_menu(self.app))},
            ((button_fontsz - 5) // 2, 2, 0.1)
        )
        self.widgets += [self.save_button, self.exit_button]

    def _update_scores(self) -> None:

        scores_y: int = self.highscore.lowerbound
        scores_height: int = self.h - scores_y - (self.h - self.save_button.posy)
        padding: int = scores_height // 8

        self.score_panel: TextPanel = TextPanel(
            -2,
            scores_y,
            self.w // 3,
            scores_height,
            self.scores,
            (padding, 2, 0.1)
        )
        self.widgets.append(self.score_panel)
        # space_remaining: int = scores_height - padding * 2

        # scores_y: int = scores_y + padding // 2

        # scores_font_size: int = space_remaining // (
        #     len(self.scores) * 2 - 1
        # )

        # max_score: str = max(self.scores, key=lambda score: len(score))
        # scores_font_size = Text._resize_font(max_score, scores_font_size, self.w)

        # for i, score in enumerate(self.scores):

        #     self.widgets.append(Text(
        #         score,
        #         -2,
        #         scores_y + scores_font_size * i + scores_font_size * (i + 1),
        #         scores_font_size
        #     ))

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_buttons()
        self._update_scores()
