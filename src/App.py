from .Config import Config
from .view.View import View


class App:
    def __init__(self) -> None:
        self.__config: Config = Config()
        self.__current_view = View()
        self.__is_running = False

    def load_config(self, filename: str) -> None:
        self.__config.load_config(filename)

    def change_view(self, view: View) -> None:
        ...

    def start_app(self) -> None:
        ...

    def stop_app(self) -> None:
        ...
