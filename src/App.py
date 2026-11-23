import pyray as pr

from pathlib import Path
from sys import stderr

from pyray import TraceLogLevel as tr_log_lvl
from pyray import KeyboardKey as kek
from typing import Any

from .Config import Config
from .display import (
    View,
    Main_menu,
    Text,
    PACMAN_FONT,
    TEXTURES_PACK
)


class Display_config:

    """
    A simple storage class used for user configuration
    (changing keybinds, textures...).
    """

    def __init__(self) -> None:

        """
        Initializes default settings for the display.
        """

        self.keybinds: dict[str, Any] = {
            "UP": kek.KEY_W,
            "DOWN": kek.KEY_S,
            "LEFT": kek.KEY_A,
            "RIGHT": kek.KEY_D
        }

        self.texture_pack: str = TEXTURES_PACK["DEFAULT"]


class App:
    """Composition root of the game: config, views and the map folder."""

    def __init__(self) -> None:
        """
            Description:
        Create the app with a default config, an empty current view and
        the folder where every custom map is stored, created if missing.
        """
        self.__config: Config = Config()
        self.views: dict[str, View] = {}
        self.__current_view: View | None = None
        self.__previous_views: list[View | None] = []
        self.__is_running: bool = False
        self.map_folder: Path = Path(".maps")
        self.map_folder.mkdir(parents=True, exist_ok=True)

        self.display_config: Display_config = Display_config()

    def load_config(self, filename: str) -> int:
        """
            Description:
        Load the json config file of the game: any invalid value falls
        back to its default, a missing or unreadable file stops here
        with a clear message.

            Parameters:
            filename -> path of the json config file

            Returns value:
        return 0 on success, 1 if the file could not be loaded
        """
        try:
            self.__config.load_config(filename)
        except ValueError as err:
            print(err, file=stderr)
            return (1)

        def create_mandatory_score(highscore_filename: str) -> int:
            """
                Description:
            Make sure the score file of the mandatory game is usable:
            an existing path must be a readable and writable file (a
            folder or a locked file is refused), a missing file is
            created with an empty score list, and any failure raises
            a ValueError with a clear message.

                Parameters:
            highscore_filename -> path of the score file from the
                                  config

                Returns value:
            return 0 when the score file is ready to use

                Raises:
            ValueError when the path is a directory, unreadable,
            unwritable, or cannot be created
            """
            score_file = Path(highscore_filename)

            if score_file.exists():
                if score_file.is_dir():
                    raise ValueError(
                            f"ERROR: score file {highscore_filename} "
                            "is a directory"
                        )
                try:
                    with open(score_file, "r"):
                        pass
                except OSError as err:
                    raise ValueError(
                            f"ERROR: score file {highscore_filename} "
                            f"is not readable: {err}"
                        ) from err
                try:
                    with open(score_file, "a"):
                        pass
                except OSError as err:
                    raise ValueError(
                            f"ERROR: score file {highscore_filename} "
                            f"is not writable: {err}"
                        ) from err
                return 0

            try:
                score_file.write_text("[]")
            except OSError as err:
                raise ValueError(
                        f"ERROR: couldn't create the score file "
                        f"{highscore_filename}: {err}"
                    ) from err
            return 0

        try:
            create_mandatory_score(self.__config.highscore_filename)
        except ValueError as err:
            print(err, file=stderr)
            return (1)

        return (0)

    def add_view(self, new_view: dict[str, View]) -> None:
        """
        Adds one or more views to the app by name, so they can be
        selected later with change_view.
        """
        self.views.update(new_view)

    def return_to_prev_view(self) -> None:
        """
        Goes back to the view shown before the current one, freeing
        the images of the view left behind.
        """
        if not self.previous_view:
            return

        prev: View | None = self.__previous_views.pop()

        if self.__current_view and not self.__current_view.is_freed:
            self.__current_view._unload_images()

        self.__current_view = prev
        if prev:
            prev._update(True)

    def change_view(self, view: View | str) -> None:
        """
        Replaces the current view with the given one, either the view
        itself or the name of a registered view. The images of the old
        view are freed and the new one is updated once.
        """
        if self.__current_view and not self.__current_view.is_freed:
            self.__current_view._unload_images()

        if not self.__current_view == self.previous_view:
            self.__previous_views.append(self.__current_view)

        if isinstance(view, View):
            self.__current_view = view

        elif isinstance(view, str) and view in self.views.keys():
            self.__current_view = self.views[view]

        if self.__current_view:
            self.__current_view._update(True)

    def start_app(self) -> None:
        """
        Opens the window, loads the font, builds the main menu and
        runs the app until the window is closed.
        """
        # pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
        pr.set_trace_log_level(tr_log_lvl.LOG_ERROR)
        pr.init_window(1920, 1080, "Pac-Man")
        pr.toggle_fullscreen()
        pr.set_target_fps(60)
        pr.set_exit_key(kek.KEY_NULL)
        Text._load_font(PACMAN_FONT)
        self.__is_running = True

        menu: Main_menu = Main_menu(self)
        self.views["main_menu"] = menu
        self.__current_view = menu
        self.__is_running = True

        self.main_loop()

    def main_loop(self) -> None:
        """
        Draws one frame at a time until the window is closed or the
        app is stopped.
        """
        while (
            not pr.window_should_close()
            and self.__is_running
        ):

            pr.begin_drawing()
            pr.clear_background(pr.BLACK)
            self.display_app()
            pr.end_drawing()

        pr.close_window()

    def stop_app(self) -> None:
        """
        Frees every view, then stops the main loop.
        """
        already_checked: set[int] = set()
        for i, view in enumerate(
            [*self.__previous_views, self.__current_view]
        ):
            if view and i not in already_checked:
                already_checked.add(i)
                if not view.is_freed:
                    view._unload_images()

        self.__is_running = False

    def display_app(self) -> None:
        """
        Draws the current view for one frame.
        """
        if self.__current_view:
            self.__current_view.display_view()

    @property
    def current_view(self) -> View | None:
        """
        The view the app is showing right now.
        """
        return self.__current_view

    @property
    def previous_view(self) -> View | None:
        """
        The view shown before the current one, or None.
        """
        if not self.__previous_views:
            return None

        return self.__previous_views[-1]

    @property
    def config(self) -> Config:
        """
        The loaded config of the game.
        """
        return self.__config
