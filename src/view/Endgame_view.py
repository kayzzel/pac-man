import pyray as pr
from .View import View
from .Save_score_view import Save_score_view
from .Main_menu import Main_menu
from ..game.Game import Game
from .widget import Panel


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

        self.title: str = (
            "VICTORY" if self.state
            else "GAME OVER"
        )

        self.title_fontsz: int = self._resize_font(self.title, self.h // 10, self.w)
        self.title_y: int = self.h // 25
        self.title_x: int = (self.w - pr.measure_text(self.title, self.title_fontsz)) // 2

        self.score: str = "SCORE: " + str(6969696969)
        self.score_fontsz: int = self._resize_font(self.score, self.h // 15, self.w)
        self.score_y: int = self.title_y + self.title_fontsz + self.h // 25
        self.score_x: int = (self.w - pr.measure_text(self.score, self.score_fontsz)) // 2

        self.high_scores: str = "Highscores"
        self.highscore_fontsz: int = self._resize_font(self.high_scores, self.h // 20, self.w)
        self.highscore_y: int = self.score_y + self.score_fontsz + self.h // 15
        self.highscore_x: int = (self.w - pr.measure_text(self.high_scores, self.highscore_fontsz)) // 2

    def _update_buttons(self) -> None:

        button_fontsz: int = self._resize_font("save", self.h // 20, self.w // 5)
        button_width: int = pr.measure_text("save", button_fontsz) + (button_fontsz - 5)
        button_height: int = button_fontsz + button_fontsz - 5
        space_remaining: int = self.w - (button_width * 2)
        padding: int = space_remaining // 3
        button_y: int = self.h - self.h // 25 - button_height

        self.save_button: Panel = Panel(
            padding,
            button_y,
            button_width,
            button_height,
            {"save": (self.app.change_view, Save_score_view(self.app, self.game))}
        )
        self.exit_button: Panel = Panel(
            self.w - padding - button_width,
            button_y,
            button_width,
            button_height,
            {"exit": (self.app.change_view, Main_menu(self.app))}
        )

    def _update_scores(self) -> None:

        scores_y: int = self.highscore_y + self.highscore_fontsz

        scores_height: int = self.h - scores_y - (self.h - self.save_button.posy)

        padding: int = scores_height // 8
        space_remaining: int = scores_height - padding * 2

        self.scores_y: int = scores_y + padding // 2

        self.scores_font_size: int = space_remaining // (
            len(self.scores) * 2 - 1
        )

        max_score: str = max(self.scores, key=lambda score: len(score))
        self.scores_font_size = self._resize_font(max_score, self.scores_font_size, self.w)

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self._update_title()
        self._update_buttons()
        self._update_scores()

    def display_view(self) -> None:

        self._update()

        pr.draw_text(
            self.title,
            self.title_x,
            self.title_y,
            self.title_fontsz,
            pr.RAYWHITE
        )
        pr.draw_text(
            self.score,
            self.score_x,
            self.score_y,
            self.score_fontsz,
            pr.RAYWHITE
        )
        pr.draw_text(
            self.high_scores,
            self.highscore_x,
            self.highscore_y,
            self.highscore_fontsz,
            pr.RAYWHITE
        )

        for i, score in enumerate(self.scores):

            pr.draw_text(
                score,
                (self.w - pr.measure_text(score, self.scores_font_size)) // 2,
                self.scores_y + self.scores_font_size * i + self.scores_font_size * (i + 1),
                self.scores_font_size,
                pr.RAYWHITE
            )

        self.save_button.display_widget()
        self.exit_button.display_widget()
