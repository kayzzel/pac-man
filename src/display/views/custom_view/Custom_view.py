from .Custom_step import Custom_step
from .Step_zero import Step_zero
from .Step_one import Step_one
from .Step_two import Step_two
from .Step_three import Step_three
from .Step_four import Step_four
from .Step_five import Step_five
from .Step_six import Step_six
from .Step_seven import Step_seven

from ..View import View
from ..Game_view import Game_view
from ...widgets import Icon

from src.game.map.Cell import Cell
from src.game.map.Map_custom import Maps_custom, Map_custom
from src.game.map.Map_storing import get_stored_map_list
from src.game.Game import custom_game

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.App import App


class Custom_view(View):

    """
    A view used to allow the user to load/create their own custom maps,
    by going through a step-by-step process.
    """

    def __init__(self, app: "App") -> None:

        """
        Initializes the main attributes of the view, mainly the app,
        instanciates the Maps_custom maps and Map_custom current map,
        and defines the list of steps for the creation process.

        Parameters
        ----------
        app: App
            The main app that handles everything.
        """

        self.app: "App" = app
        self.current_map: Map_custom = Map_custom()
        self.maps: Maps_custom = Maps_custom(self.app.map_folder)
        self.is_freed: bool = False

        self.steps: list[
            type[Step_zero]
            | type[Step_one]
            | type[Step_two]
            | type[Step_three]
            | type[Step_four]
            | type[Step_five]
            | type[Step_six]
            | type[Step_seven]
        ] = []

        maps: list[str] = get_stored_map_list(self.app.map_folder)
        if maps != ["mandatory", "arcade"]:
            self.steps.append(Step_zero)

        self.steps += [
            Step_one,
            Step_two,
            Step_three,
            Step_four,
            Step_five,
            Step_six,
            Step_seven
        ]
        self.steps_completed: list[Custom_step] = []
        self.sprites_set: list[tuple[Icon, Cell]] = []

        self.cur_step_index: int = 0
        self.cur_step: Custom_step = self.steps[0](self)

        self.set_map_properties(0, 0, 0, 0, 0)

    def reset_steps(self) -> None:

        """
        Resets the cycle of steps for the custom creation,
        when the user wants to create a new map.
        """

        self.steps_completed.append(self.cur_step)
        self._unload_images()
        self.steps_completed = []
        self.cur_step_index = 0
        if self.steps[self.cur_step_index] == Step_zero:
            self.cur_step_index += 1
        self.current_map = Map_custom()
        self.cur_step = self.steps[self.cur_step_index](self)

    def set_map_properties(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        cell_sz: int
    ) -> None:

        """
        Sets the map properties (x, y, width, height and cell size)
        to be accessed by the current step
        and keep display consistency from one step to another.

        Parameters
        ----------
        x: int
            The start x coordinate of the map on the screen.
        y: int
            The start y coordinate of the map on the screen.
        w: int
            The width of the map on the screen.
        h: int
            The height of the map on the screen.
        cell_size: int
            The size of a single map cell on the screen.
        """

        self.map_x, self.map_y, self.map_w, self.map_h, self.cell_size = (
            x, y, w, h, cell_sz
        )

    def _unload_images(self) -> None:

        """
        Unloads the images and textures of all icons in all steps
        and sets 'is_freed' to True.
        """

        if self.is_freed:
            return

        for step in [*self.steps_completed, self.cur_step]:
            if not step.is_freed:
                step._unload_images()
        self.is_freed = True

    def launch_game(self, map_name: str) -> None:

        """
        Launches a custom game using the name of the map to load.

        Parameters
        ----------
        map_name: str
            The name of the map to load and start a game with.
        """

        game = custom_game(map_name, self.app.map_folder)
        if game:
            self.app.change_view(Game_view(self.app, game))

    def go_to_menu(self) -> None:

        """
        Goes back to the main menu.
        """

        self.app.change_view("main_menu")

    def step_back(self) -> None:

        """
        Steps back in the loading/creation process,
        changing the step index and unloading images/textures.
        Also goes back to the view before the Custom_view
        if the user goes back before the first step.
        """

        if self.cur_step_index == 0:
            self.app.return_to_prev_view()
            return

        self.cur_step_index -= 1
        if not self.cur_step.is_freed:
            self.cur_step._unload_images()
        self.cur_step = self.steps_completed[-1]
        self.steps_completed.pop()

    def step_forward(self) -> None:

        """
        Steps forward in the loading/creation process,
        saving the completed step in a list,
        and instanciating the next step as the current step.
        """

        if self.cur_step_index + 1 == len(self.steps):
            return

        self.cur_step_index += 1
        self.steps_completed.append(self.cur_step)
        self.cur_step = self.steps[self.cur_step_index](self)

    def display_view(self) -> None:

        """
        Displays the current step of the loading/creation process.
        """

        self.cur_step.display_view()
