import pyray as pr
from .View import View
from .Save_score_view import Save_score_view
from ..game.Game import Game
from .widget import ButtonPanel, TextPanel, Text


class Endgame_view(View):

    def __init__(self, app, game: Game, state: bool = False) -> None:

        self.game: Game = game
        self.state: bool = state
        self.scores: list[str] = []
        if self.game.scores.scores:
            self.scores = [
                pl.name + ": " + str(pl.score)
                for pl in self.game.scores.scores
            ]
        if not self.scores:
            self.scores.append("No scores yet")
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
            "SCORE: " + str(self.game.player.score),
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

        button_w: int = self.w // 15
        button_h: int = self.h // 10
        self.save_button: ButtonPanel = ButtonPanel(
            (self.w - button_w * 3) // 2,
            -2,
            button_w,
            button_h,
            {"save": (
                self.app.change_view,
                Save_score_view(self.app, self.game)
            )}
        )
        self.exit_button: ButtonPanel = ButtonPanel(
            self.save_button.posx + button_w * 2,
            -2,
            button_w,
            button_h,
            {"exit": (self.app.change_view, "main_menu")}
        )
        self.widgets += [self.save_button, self.exit_button]

    def _update_scores(self) -> None:

        scores_y: int = self.highscore.lowerbound
        scores_height: int = (
            self.h
            - scores_y
            - (self.h - self.save_button.posy)
        )
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

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_title()
        self._update_buttons()
        self._update_scores()
