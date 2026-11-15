import pyray as pr
from typing import Callable, Any
from pathlib import Path
from .View import View
from ..game.map.Map_scores import Map_scores
from ..game.map.Map_storing import get_stored_map_list
from .widget import Text, ButtonPanel, TextPanel, Dropdown


class Scores_view(View):

    """
    A simple view to display the scores for a map.
    If entered via the main menu, the default map is the mandatory map,
    and if entered via the pause menu after a game was started,
    the default map is the current game map.
    Other maps' scores can be loaded via a dropdown.
    """

    def __init__(self, app, map_name: str = "mandatory") -> None:

        """
        Initializes the main attributes of the view
        and updates it a first time, loading the scores
        of the map given.

        Parameters
        ----------
        app: App
            The app that manages everything.
        map_name: str (default 'mandatory')
            The name of the first map
            for which to display the scores.
        """

        self.maps: list[str] = get_stored_map_list(app.map_folder)
        self.init_scores: bool = False
        self.load_new_scores(map_name, app.map_folder)
        self.init_scores = True
        super().__init__(app)

    def _update_title(self) -> None:

        """
        Builds the view's title widget.
        """

        self.title: Text = Text(
            f"BEST SCORES FOR {self.map_scores.map_name.upper()}",
            -2,
            self.h // 15,
            self.h // 10
        )
        self.widgets.append(self.title)

    def load_new_scores(self, map_name: str, map_folder: Path) -> None:

        """
        Loads the scores of a map, searching for them
        in the folder where the scores are stored.

        Parameters
        ----------
        map_name: str
            The name of the map for which to load the scores.
        map_folder: Path
            The path to the folder where the score files are stored.
        """

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

        """
        Builds the back button and the dropdown
        that lists all the available maps for the user to select.
        """

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

        """
        Builds the text panel that displays all the scores,
        with their place, username and value.
        """

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
