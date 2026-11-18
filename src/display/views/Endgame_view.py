import pyray as pr

from .View import View
from .Save_score_view import Save_score_view
from ..widgets import ButtonPanel, TextPanel, Text

from src.game.Game import Game

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.App import App


class Endgame_view(View):

    """
    A view displayed at the end of a game (win or lose).
    The user can see the highscores for this map,
    save their own score, or exit.
    """

    def __init__(self, app: "App", game: Game, state: bool = False) -> None:

        """
        Initializes the main attributes of the view
        and updates it a first time, loading the scores
        of the game's map.

        Parameters
        ----------
        app: App
            The app that manages everything.
        game: Game
            The current game the user has started.
        state: bool (default False)
            True if the user has won the game, False otherwise.
        """

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

        elif len(self.scores) < 10:
            self.scores += [" " for _ in range(10 - len(self.scores))]

        super().__init__(app)

    def _update_title(self) -> None:

        """
        Builds the view's title widgets.
        """

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
            "YOUR SCORE: " + str(self.game.player.score),
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

        """
        Builds the save and back buttons of the view.
        """

        button_w: int = self.w // 8
        button_h: int = self.h // 10
        self.save_button: ButtonPanel = ButtonPanel(
            (self.w - button_w * 3) // 2,
            self.h - button_h - self.h // 40,
            button_w,
            button_h,
            {"save": (
                self.app.change_view,
                Save_score_view(self.app, self.game)
            )}
        )
        self.exit_button: ButtonPanel = ButtonPanel(
            self.save_button.posx + button_w * 2,
            self.h - button_h - self.h // 40,
            button_w,
            button_h,
            {"exit": (self.app.change_view, "main_menu")}
        )
        self.widgets += [self.save_button, self.exit_button]

    def _update_scores(self) -> None:

        """
        Builds the text panel containing the game's map scores,
        displaying their place, username and value.
        """

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

        """
        Updates the view, checking if the window has been resized,
        and re-building the widgets if needed.

        Parameters
        ----------
        forced: bool (default False)
            Whether or not the view MUST be updated.
        """

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_title()
        self._update_buttons()
        self._update_scores()
