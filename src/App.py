import pyray as pr
from pyray import KeyboardKey as kek
from typing import Any
from .Config import Config
from .view.View import View
from .view.Main_menu import Main_menu
from .view.widget.Text import Text, PACMAN_FONT
from .view.Texture_pack import TEXTURES_PACK

from pathlib import Path
from sys import stderr


class Display_config:

    def __init__(self) -> None:

        self.keybinds: dict[str, Any] = {
            "UP": kek.KEY_W,
            "DOWN": kek.KEY_S,
            "LEFT": kek.KEY_A,
            "RIGHT": kek.KEY_D
        }

        self.fps_max: int = 60

        self.texture_pack: str = TEXTURES_PACK["DEFAULT"]


class App:
    def __init__(self) -> None:
        self.__config: Config = Config()
        self.views: dict[str, View] = {}
        self.__current_view: View | None = None
        self.__previous_views: list[View | None] = []
        self.__is_running = False
        self.map_folder: Path = Path(".maps")
        self.map_folder.mkdir(parents=True, exist_ok=True)

        self.display_config: Display_config = Display_config()

    def load_config(self, filename: str) -> int:
        try:
            self.__config.load_config(filename)
        except ValueError as err:
            print(err, file=stderr)
            return (1)

        return (0)

    def add_view(self, new_view: dict[str, View]) -> None:
        self.views.update(new_view)

    def return_to_prev_view(self) -> None:

        if not self.previous_view:
            return

        # if (
        #     hasattr(self.current_view, "show_as_modal")
        # ) and (
        #     self.current_view.show_as_modal
        # ):

        #     self.current_view.show_as_modal = False
        #     return

        if isinstance(self.previous_view, type(self.__current_view)):
            self.remove_last_view()
        self.change_view(self.previous_view)

    def change_view(self, view: View | str) -> None:

        if isinstance(view, View):
            if not isinstance(self.__current_view, type(self.previous_view)):
                self.__previous_views.append(self.__current_view)
            self.__current_view = view

        elif isinstance(view, str) and view in self.views.keys():
            if not self.previous_view == self.__current_view:
                self.__previous_views.append(self.__current_view)
            self.__current_view = self.views[view]

        view_names: list[str] = [type(view) for view in self.__previous_views]
        print(f"### changed to view {type(self.__current_view)}, previous_views: {view_names}\n")
        if self.__current_view:
            self.__current_view._update(True)

    def start_app(self) -> None:

        # pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
        pr.set_trace_log_level(pr.LOG_ERROR)
        pr.init_window(1920, 1080, "pac-man menu example")
        pr.toggle_fullscreen()
        pr.set_target_fps(60)
        pr.set_exit_key(pr.KEY_NULL)
        Text._load_font(PACMAN_FONT)

        menu: Main_menu = Main_menu(self)
        self.views["main_menu"] = menu
        self.__current_view = menu

        while not pr.window_should_close():

            pr.begin_drawing()
            pr.clear_background(pr.BLACK)

            self.display_app()

            pr.end_drawing()

    def stop_app(self) -> None:

        pr.close_window()

    def display_app(self) -> None:

        if self.__current_view:
            self.__current_view.display_view()

    @property
    def current_view(self) -> View | None:

        return self.__current_view

    @property
    def previous_view(self) -> View | None:

        if not self.__previous_views:
            return None

        return self.__previous_views[-1]

    def remove_last_view(self) -> None:

        if not self.__previous_views:
            return

        if self.previous_view == self.views["main_menu"]:
            return

        self.__previous_views.pop()

    @property
    def config(self) -> Config:

        return self.__config
