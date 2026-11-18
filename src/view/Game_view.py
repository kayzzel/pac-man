import pyray as pr

from pyray import KeyboardKey as kek

from .View import View
from .Pause_menu import Pause_menu
from .Endgame_view import Endgame_view
from .Map_renderer import Map_renderer
from .widget import Icon, Text, Widget, TextPanel

from ..game.Game import Game
from ..game.map.Cell import Cell
from ..utils.enum_utils import Game_state, Consumable_type

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..App import App


LIFE_ICON_PATH: str = "src/view/assets/icons/pac-man_life_icon.png"
COUNTDOWN_TIME: int = 60
LVL_SHOW_TIME: int = 100

MIDDLE_LINE_THICKNESS: int = 10


class Game_view(View):

    """
    A view used to display the current game playing.
    """

    def __init__(self, app: "App", game: Game) -> None:

        """
        Initializes the main attributes of the view,
        such as the game currently playing, the pause menu
        that serves as a modal view, and the map renderer.

        Parameters
        ----------
        app: App
            The main app handling everything.
        game: Game
            The game started by the user.
        """

        self.game: Game = game
        self.modal_view: Pause_menu = Pause_menu(app, game, self)
        self.map_renderer: Map_renderer = Map_renderer(
            self.game,
            app.display_config.texture_pack
        )
        self.show_as_modal: bool = False
        self.life_icon_init: bool = False

        self.reset_game()
        super().__init__(app)

    def reset_game(self) -> None:

        """
        Resets the game for a new map.
        """

        self.game_start: bool = False
        self.lvl_shown: bool = False
        self.countdown: int = 3
        self.frame_counter: int = 0
        self.map_renderer.end_loop_counter = 0

    def _update_countdown(self) -> None:

        """
        Increments the start countdown,
        resuming the game loop (starting the game)
        if it reaches 0, otherwise creating a Text widget
        to display the current countdown.
        """

        if not self.lvl_shown:

            if self.frame_counter == 0:
                self.countdown_label: Text = Text(
                    f"LEVEL {self.game.map_index + 1}",
                    -2,
                    (self.h - self.h // 4) // 2,
                    self.h // 4
                )

            self.frame_counter += 1

            if self.frame_counter > LVL_SHOW_TIME:
                self.lvl_shown = True

            return

        if self.countdown == -1:

            if self.frame_counter <= COUNTDOWN_TIME:
                self.frame_counter += 1
                return

            self.game_start = True
            self.game.resume()
            self._update(True)
            return

        if self.frame_counter > COUNTDOWN_TIME:
            self.frame_counter = 0

        if self.frame_counter == 0:

            label: str = str(self.countdown)
            if self.countdown == 0:
                label = "START !!!"
            self.countdown_label = Text(
                label,
                -2,
                (self.h - self.h // 6) // 2,
                self.h // 6
            )
            self.countdown -= 1

        self.frame_counter += 1

    def _update_info_panel(self) -> None:

        """
        Builds the information panel, located on the left of the screen,
        with widgets displaying the current score, highscore,
        number of lives, timer, and collectibles collected.
        """

        if not self.is_freed and hasattr(self, "info_widgets"):
            for widget in self.info_widgets:
                if isinstance(widget, Icon):
                    widget._unload_image()

        self.info_widgets: list[Widget] = []

        self.labels: list[str] = [
            "Highscore : " + str(0),
            "Score : " + str(self.game.player.score),
            "Timer : " + str(self.game.timer)
        ]
        self.info_panel: TextPanel = TextPanel(
            0,
            self.h // 16,
            self.w // 4,
            self.h // 3,
            self.labels,
            (self.w // 12 // 2, 2, 0.1)
        )

        self.life_label: Text = Text(
            "Lives : ",
            self.info_panel.w // 10,
            self.info_panel.posy + self.info_panel.h + self.h // 4,
            self.info_panel.font_size
        )

        if not self.life_icon_init:

            self.life_icon_sz: int = (
                self.info_panel.w - (self.life_label.x + self.life_label.width)
            ) // self.game.player.nb_lives - self.info_panel.w // 30
            self.life_icon_init = True

        self.lives: list[Icon] = [Icon(
            (
                self.info_panel.w // 30
                + self.life_label.x
                + self.life_label.width
                + self.life_icon_sz * life
            ),
            self.life_label.y + (
                self.life_label.font_size - self.life_icon_sz
            ) // 2,
            LIFE_ICON_PATH,
            (self.life_icon_sz, self.life_icon_sz),
            True
        ) for life in range(self.game.player.nb_lives)]

        self.info_widgets += [self.info_panel, self.life_label]
        self.info_widgets += [i for i in self.lives]
        self._update_collectibles()

    def _update_collectibles(self) -> None:

        """
        Builds the required collectible icons
        based on if they were already collected or not.
        """

        collect_info: dict[str, str] = {}
        for collectible_name in Consumable_type:
            state: str = (
                "_c" if collectible_name.value in [
                    cons.name for cons in self.game.consumables
                ] else "_nc"
            )
            collect_info[collectible_name.value] = (
                self.map_renderer.texture_pack.get_texture(
                    collectible_name.value + state
                )
            )
        nb_cons: int = len(list(collect_info.keys()))

        self.collectibles: list[Icon] = []

        collectible_label: Text = Text(
            "Collectibles :",
            -2,
            self.life_label.lowerbound + self.h // 15,
            self.info_panel.font_size,
            self.info_panel.w,
            pr.RAYWHITE,
            self.info_panel.w
        )
        self.info_widgets.append(collectible_label)

        height_remaining: int = (
            self.h - collectible_label.lowerbound - self.h // 10
        )
        collect_h: int = height_remaining // 2
        coll_padding: int = self.info_panel.w // 60
        collect_w: int = (
            self.info_panel.w // (nb_cons // 2)
        ) - coll_padding * 2

        if collect_w < collect_h:
            collect_sz: int = collect_w

        else:
            collect_sz = collect_h
            coll_padding = ((
                self.info_panel.w - (collect_sz * (nb_cons // 2))
            ) // (nb_cons // 2)) // 2

        first_y: int = collectible_label.lowerbound + self.h // 30
        second_y: int = first_y + collect_sz + self.h // 30

        for i, (coll_name, coll_texture) in enumerate(collect_info.items()):

            if i == 0:
                coll_y: int = first_y
                coll_x: int = coll_padding

            if i == len(list(collect_info.keys())) // 2:
                coll_y = second_y
                coll_x = coll_padding

            new_coll: Icon = Icon(
                coll_x,
                coll_y,
                coll_texture,
                (collect_sz, collect_sz),
                True
            )
            coll_x += coll_padding * 2 + collect_sz
            self.collectibles.append(new_coll)

        self.info_widgets += self.collectibles

    @property
    def map_startx(self) -> int:

        """
        Calculates the start x coordinate of the grid on the screen.

        Returns
        -------
        int
            The start x coordinate of the grid.
        """

        return (
            self.info_panel.w + MIDDLE_LINE_THICKNESS
            + (self.map_panel_width - self.map_width) // 2
        )

    @property
    def map_starty(self) -> int:

        """
        Calculates the start y coordinate of the grid on the screen.

        Returns
        -------
        int
            The start y coordinate of the grid.
        """

        return (self.h - self.map_height) // 2

    def catch_player_input(self) -> None:

        """
        Handles player input and changes PacMan's direction
        based on the keybind pressed.
        """

        if self.game.state != Game_state.RUNNING:
            return

        if pr.is_key_pressed(self.app.display_config.keybinds["UP"]):
            self.game.player.set_next_direction("N")
        elif pr.is_key_pressed(self.app.display_config.keybinds["DOWN"]):
            self.game.player.set_next_direction("S")
        elif pr.is_key_pressed(self.app.display_config.keybinds["LEFT"]):
            self.game.player.set_next_direction("W")
        elif pr.is_key_pressed(self.app.display_config.keybinds["RIGHT"]):
            self.game.player.set_next_direction("E")

    def _update_map_panel(self) -> None:

        """
        Calculates the grid's position and size aswell as cell size,
        and updates the map renderer's grid to create a new render texture.
        """

        self.grid: list[list[Cell]] = self.game.map[self.game.map_index].cells
        self.map_panel_width: int = (
            self.w - self.info_panel.w - MIDDLE_LINE_THICKNESS - 10
        )
        map_space: int = min(
            self.map_panel_width - self.map_panel_width // 10,
            self.h - self.h // 10
        )

        nb_cells_row: int = map_space // len(self.grid[0])
        nb_cells_col: int = map_space // len(self.grid)

        self.cell_size: int = min(nb_cells_row, nb_cells_col)
        self.map_width = self.cell_size * len(self.grid[0])
        self.map_height = self.cell_size * len(self.grid)

        self.map_renderer.update_grid(
            self.grid,
            (self.map_width, self.map_height),
            (self.map_startx, self.map_starty),
            self.cell_size,
            [self.game.player] + list(self.game.ghosts.values())
        )

    def pause_or_resume(self) -> None:

        """
        Changes the 'show_as_modal' state.
        If activated, the modal view (pause menu) will be shown
        instead of the game view.
        """

        self.show_as_modal = not self.show_as_modal

        if self.show_as_modal:
            self.game.pause()
            if not self.modal_view.show_cheat_panel:
                self.modal_view.reset_input()
        else:
            self.game.resume()

    def exit_game(self, next_view: View) -> None:

        """
        Exits the game view and changes to the given view,
        stopping the current game.

        Parameters
        ----------
        next_view: View
            The next view to display.
        """

        self.game.stop()
        self.app.change_view(next_view)

    def _unload_images(self) -> None:

        """
        Unloads all icons' images and textures if not already done,
        from the information panel,
        the map renderer sprites and grid render texture,
        and the modal view's icons aswell.
        """

        self.modal_view._unload_images()

        if self.is_freed:
            return

        if hasattr(self, "widgets"):
            for widget in self.widgets:
                if isinstance(widget, Icon):
                    widget._unload_image()

        if hasattr(self, "info_widgets"):
            for widget in self.info_widgets:
                if isinstance(widget, Icon):
                    widget._unload_image()

        if hasattr(self, "map_renderer"):
            self.map_renderer._unload_images()

        self.is_freed = True

    def _update(self, forced: bool = False) -> None:

        """
        Updates the game view aswell as the modal view (pause menu).
        Checking for user input (movement keys and escape key),
        if the current map is finished (need reset),
        if the game is over (win or lose),
        if the start countdown has finished being displayed,
        if the window has been resized
        and re-building the widgets if needed.

        Parameters
        ----------
        forced: bool (default False)
            Whether or not the view MUST be updated.
        """

        if pr.get_key_pressed() in self.app.display_config.keybinds.values():
            self.catch_player_input()

        if pr.is_key_pressed(kek.KEY_ESCAPE):
            self.pause_or_resume()

        if self.game.state == Game_state.FINISHED_MAP and self.game_start:
            if self.map_renderer.check_over():
                self.reset_game()
            else:
                return

        if self.game.state in [Game_state.WON, Game_state.LOST]:
            state: bool = self.game.state == Game_state.WON
            if self.map_renderer.check_over():
                self.exit_game(Endgame_view(self.app, self.game, state))
            return

        if not self.game_start:
            self._update_countdown()
            return

        if not forced:
            self._update_info_panel()

        if not pr.is_window_resized() and not forced:
            return

        self.modal_view._update(True)

        self._unload_images()
        self.widgets: list[Widget] = []
        self._update_info_panel()
        self._update_map_panel()
        self.is_freed = False

    def display_view(self) -> None:

        """
        Updates and displays the game view,
        or the modal view (pause menu) if 'show_as_modal' is True.
        Draws the separating line between the information panel
        and the game grid, and draws the grid's outline aswell.
        Draws the grid and sprites via the map renderer
        and displays the information panel widgets.
        """

        self._update()

        if not self.game_start:
            self.countdown_label.display_widget()
            return

        if self.show_as_modal:
            self.modal_view.display_view()
            return

        pr.draw_line_ex(
            (self.info_panel.w, 0),
            (self.info_panel.w, self.h),
            MIDDLE_LINE_THICKNESS,
            pr.RAYWHITE
        )

        self.map_renderer.display_grid()

        for i_widget in self.info_widgets:
            i_widget.display_widget()

        for widget in self.widgets:
            widget.display_widget()
