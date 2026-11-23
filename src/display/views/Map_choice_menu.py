import pyray as pr

from typing import Callable, Any
from pathlib import Path

from .View import View
from .Game_view import Game_view
from .custom_view import Custom_view
from ..widgets import Text, ButtonPanel, Icon

from src.game.Game import custom_game, mandatory_game

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.App import App

MSG_TIME: int = 80

ICON_PATHS: dict[str, str] = {
    "MANDATORY": "assets/icons/mandatory_snapshot.png",
    "ARCADE": "assets/icons/arcade_snapshot.png",
    "CUSTOM": "assets/icons/custom_snapshot.png"
}


class Map_choice_menu(View):

    """
    A view used for the user to select the game mode
    they want to play (mandatory, arcade or custom).
    """

    def __init__(self, app: "App") -> None:

        """
        Initializes the main attributes of the view.

        Parameters
        ----------
        app: App
            The main app that handles everything.
        """

        self.show_message: str = ""
        self.frame_counter: int = 0
        super().__init__(app)

    def _update_title(self) -> None:

        """
        Builds the view's title widget.
        """

        self.title: Text = Text(
            "CHOOSE THE MODE",
            -2,
            self.h // 10,
            self.h // 8
        )
        self.widgets.append(self.title)

    def _update_icons(self) -> None:

        """
        Builds the three icons that show a preview
        of each game mode for the user to select.
        """

        self.icon_width: int = self.w // 4

        height_remaining: int = self.h - self.title.lowerbound
        self.icon_height: int = 2 * (height_remaining // 4)

        self.icon_y: int = self.title.lowerbound + height_remaining // 10
        icon_spacing: int = (self.w - self.icon_width * 3) // 4

        self.icons: dict[str, Icon] = {
            icon_type: Icon(
                i * self.icon_width + (i + 1) * icon_spacing,
                self.icon_y,
                icon_path,
                (self.icon_width, self.icon_height),
                True
            ) for i, (icon_type, icon_path) in enumerate(ICON_PATHS.items())
        }
        self.widgets += list(self.icons.values())

    def _update_panels(self) -> None:

        """
        Builds the three button panels, one for each game mode
        that the user can select, and builds the back button aswell.
        """

        self.button_actions: dict[
            str,
            tuple[Callable[..., Any], Any]
        ] = {
            "MANDATORY": (
                self.launch_game,
                (mandatory_game, self.app.config)
            ),
            "ARCADE": (
                self.launch_game,
                (custom_game, ("arcade", Path("src/arcade")))
            ),
            "CUSTOM": (self.app.change_view, Custom_view(self.app))
        }

        self.calculate_panel_spacing()

        self.widgets += [ButtonPanel(
            self.icons[label].posx + (
                self.icons[label].w - self.panel_width
            ) // 2,
            self.icon_y + (self.icon_height - self.panel_height) // 2,
            self.panel_width,
            self.panel_height,
            {label: action},
            (10, 3, 4.0)
        ) for i, (label, action) in enumerate(self.button_actions.items())
        ]

        back_label: str = "back <-|"
        self.button_actions[back_label] = (
            self.app.return_to_prev_view,
            None
        )

        back_width: int = self.w // 8
        back_height: int = self.h // 15

        self.back_button: ButtonPanel = ButtonPanel(
            self.w - back_width - self.w // 25,
            self.h - back_height - self.h // 40,
            back_width,
            back_height,
            {back_label: self.button_actions[back_label]}
        )
        self.widgets.append(self.back_button)

    def launch_game(
        self,
        game_function: Callable[..., Any],
        args: Any
    ) -> None:

        """
        Launches a custom game using the game function and the args.

        Parameters
        ----------
        game_function: Callable[..., Any]
            The function to start a game with (mandatory/custom).
        args: Any
            The argument(s) to pass to the game creation function.
        """

        game_view: Game_view = Game_view(
            self.app,
            game_function,
            args
        )
        if game_view.game is None:
            self.show_message = (
                "Couldn't load the game, an error occurred."
            )
            return

        self.app.change_view(game_view)

    def calculate_panel_spacing(self) -> None:

        """
        Calculates the panel's font size and spacing
        for the three oval buttons.
        """

        max_label: str = max(
            self.button_actions.keys(),
            key=lambda label: len(label)
        )
        self.button_fontsz: int = Text._resize_font(
            max_label,
            self.h // 15,
            self.w // 5
        )

        self.panel_padding: int = self.button_fontsz + self.button_fontsz // 5
        self.panel_width: int = pr.measure_text(
            max_label,
            self.button_fontsz
        ) + self.panel_padding

        nb_buttons: int = len(self.button_actions.keys())
        width_remaining: int = (
            self.w -
            nb_buttons * self.panel_width
        )

        self.panel_height: int = self.button_fontsz + self.panel_padding

        self.spacing: int = width_remaining // (nb_buttons + 1)

    def display_message(self) -> None:

        """
        Builds and displays a text message
        if the game could not be launched.
        """

        if self.frame_counter < MSG_TIME:

            message: Text = Text(
                self.show_message,
                -2,
                self.back_button.posy - self.h // 25,
                self.h // 25,
                self.w // 2,
                pr.MAROON
            )
            message.display_widget()
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.frame_counter = 0

    def _update(self, forced: bool = False) -> Any:

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
        self._update_icons()
        self._update_panels()

    def display_view(self) -> None:

        """
        Updates and displays the view's widgets,
        and also shows the game failing message if needed.
        """

        super().display_view()

        if self.show_message:
            self.display_message()
