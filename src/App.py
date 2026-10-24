import pyray as pr
from typing import Any
from .Config import Config
from .view.View import View
fron .view.Texture_pack import TEXTURES_PACK

from sys import stderr


class Display_config:

    def __init__(self) -> None:

        self.keybinds: dict[str, Any] = {
            "UP": pr.KEY_W,
            "DOWN": pr.KEY_S,
            "LEFT": pr.KEY_A,
            "RIGHT": pr.KEY_D
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

        self.change_view(self.previous_view)

    def change_view(self, view: View | str) -> None:

        if isinstance(view, View):
            self.__previous_views.append(self.__current_view)
            self.__current_view = view

        elif isinstance(view, str) and view in self.views.keys():
            self.__previous_views.append(self.__current_view)
            self.__current_view = self.views[view]

        if self.__current_view:
            self.__current_view._update(True)

    def start_app(self) -> None:
        ...

    def stop_app(self) -> None:
        ...

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

    @property
    def config(self) -> Config:

        return self.__config
