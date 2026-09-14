from .Config import Config
from .view.View import View

from sys import stderr


class App:
    def __init__(self) -> None:
        self.__config: Config = Config()
        self.__current_view = View()
        self.__is_running = False

    def load_config(self, filename: str) -> int:
        try:
            self.__config.load_config(filename)
        except ValueError as err:
            print(err, file=stderr)
            return (1)

        return (0)

    def change_view(self, view: View) -> None:
        ...

    def start_app(self) -> None:
        ...

    def stop_app(self) -> None:
        ...
