import pyray as pr

from .View import View
from ..widgets import Text, Input_box, ButtonPanel

from src.game.Game import Game

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.App import App


MAX_INPUT_LENGTH: int = 10

MSG_DISPLAY_TIME: int = 80


class Save_score_view(View):

    """
    A view where the user can enter a username of their choice
    to save their current score.
    """

    def __init__(self, app: "App", game: Game) -> None:

        """
        Initializes the main attributes of the view
        and updates it a first time.

        Parameters
        ----------
        app: App
            The app that manages everything.
        game: Game
            The current game the user has started.
        """

        self.game: Game = game
        self.show_message: list[str] = []
        super().__init__(app)

    def _update_title(self) -> None:

        """
        Builds the view's title widget.
        """

        self.title: Text = Text(
            "SAVE SCORE",
            -2,
            self.h // 12,
            self.h // 10
        )
        self.widgets.append(self.title)

    def _update_back_button(self) -> None:

        """
        Builds the back button for the view.
        """

        back_label: str = "back <-|"
        back_width: int = self.w // 8
        back_height: int = self.h // 15

        self.back_button: ButtonPanel = ButtonPanel(
            self.w - back_width - self.w // 25,
            self.h - back_height - self.h // 40,
            back_width,
            back_height,
            {back_label: (self.app.return_to_prev_view, None)}
        )
        self.widgets.append(self.back_button)

    def _update_input_box(self) -> None:

        """
        Builds the input box that is handling the user's input
        of their username to save their score.
        """

        all_characters: list[int] = []
        for crange in [(48, 58), (65, 91), (97, 123)]:
            all_characters += [i for i in range(*crange)]

        self.input_box: Input_box = Input_box(
            -2,
            -2,
            self.w // 3,
            self.h // 8,
            (self.save_name, None),
            MAX_INPUT_LENGTH,
            all_characters
        )
        self.input_box.enter_input = True
        self.widgets.append(self.input_box)

        self.input_text: Text = Text(
            "enter name:",
            -2,
            (
                self.input_box.posy
                - self.h // 16
                - self.h // 20
            ),
            self.h // 16,
            self.w
        )
        self.go_next: bool = False

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
        self._update_back_button()
        self._update_input_box()

    def save_name(self) -> None:

        """
        Stores the name the player has entered in the input box,
        setting the 'show_message' attribute a value
        to display a confirmation message for a few seconds before exiting.
        """

        self.pl_name: str = self.input_box.input
        self.input_text.label = ""
        if (
            self.game.scores.add_score(self.pl_name, self.game.player.score)
            is False
        ):
            self.show_message = ["This score cannot be saved, try again"]
            self.go_next = False
        else:
            self.show_message = [
                "Successfully saved ",
                f"the score {self.game.player.score}",
                f" for player {self.pl_name}!"
            ]
            self.go_next = True
        self.msg_frame_counter: int = 0

    def display_view(self) -> None:

        """
        Updates and displays the view's widgets,
        showing an 'enter name' text above the input box
        if the player has not yet entered anything,
        and also showing the confirmation message.
        """

        self._update()

        if self.input_text.label:
            self.widgets.append(self.input_text)

        for widget in self.widgets:
            widget.display_widget()

        if self.show_message:
            self.display_message()

    def display_message(self) -> None:

        """
        Displays the confirmation message of the view
        if the frame counter has not yet reached the end time,
        and if it did, exiting the view and returning to the main menu.
        """

        if self.msg_frame_counter < MSG_DISPLAY_TIME:

            msg_y: int = self.input_box.posy + self.input_box.h + self.h // 15

            for msg in self.show_message:

                text: Text = Text(
                    msg,
                    -2,
                    msg_y,
                    self.h // 25,
                    self.w - self.w // 3
                )

                text.display_widget()
                msg_y += text.font_size + text.font_size // 2

            self.msg_frame_counter += 1

        else:

            self.show_message = []
            if self.go_next:
                self.app.change_view("main_menu")
