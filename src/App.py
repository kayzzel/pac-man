from .Config import Config
from .view.View import View


class App:
    def __init__(self) -> None:
        self.__config: Config = Config()
        self.views: dict[str, View] = {}
        self.__current_view: View | None = None
        self.__previous_views: list[View | None] = []
        self.__is_running = False

    def load_config(self, filename: str) -> None:
        self.__config.load_config(filename)

    def add_view(self, new_view: dict[str, View]) -> None:
        self.views.update(new_view)

    def return_to_prev_view(self) -> None:

        if self.__previous_views and self.__previous_views[-1]:

            self.__current_view = self.__previous_views[-1]

    def change_view(self, view: View | str) -> None:

        if isinstance(view, View):
            self.__previous_views.append(self.__current_view)
            self.__current_view = view

        elif isinstance(view, str) and view in self.views.keys():
            self.__previous_views.append(self.__current_view)
            self.__current_view = self.views[view]

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
    def config(self) -> Config:

        return self.__config
