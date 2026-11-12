from .Config import Config
from .view.View import View

from pathlib import Path
from sys import stderr


class App:
    """Composition root of the game: config, views and the map folder."""

    def __init__(self) -> None:
        """
            Description:
        Create the app with a default config, an empty current view and
        the folder where every custom map is stored, created if missing.
        """
        self.__config: Config = Config()
        self.__current_view = View()
        self.__is_running = False
        self.map_folder: Path = Path(".maps")
        self.map_folder.mkdir(parents=True, exist_ok=True)

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

        return (0)

    def change_view(self, view: View) -> None:
        """
            Description:
        Replace the current view of the app (handled by the GUI side).
        """
        ...

    def start_app(self) -> None:
        """
            Description:
        Start the app (handled by the GUI side).
        """
        ...

    def stop_app(self) -> None:
        """
            Description:
        Stop the app (handled by the GUI side).
        """
        ...
