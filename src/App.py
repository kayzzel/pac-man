from .Config import Config
from .view.View import View


class App:
    def __init__(self) -> None:
        self.config: Config = Config()
        self.current_view = View()

    def load_config(self, filename: str) -> None:
        self.config.load_config(filename)

    def change_vue(self, view: View) -> None:
        ...
