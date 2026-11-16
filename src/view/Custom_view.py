import pyray as pr

from pyray import MouseButton as mb
from abc import ABC
from typing import Callable, Any

from .View import View
from .Texture_pack import Texture_pack
from .Map_renderer import Custom_map_renderer
from .Game_view import Game_view
from .widget import (
    Widget,
    Text,
    ButtonPanel,
    Input_box,
    ClickableIcon,
    Icon,
    Dropdown
)

from ..game.Game import custom_game
from ..game.map.Map_storing import get_stored_map_list
from ..game.map.Map_custom import Map_custom
from ..game.map.Cell import Cell
from ..game.entity.collectible.Consumable import Consumable
from ..game.entity.collectible.Pacgum import Pacgum
from ..game.entity.collectible.Super_Pacgum import Super_Pacgum
from ..utils.enum_utils import Consumable_type

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..App import App


MSG_TIME: int = 120

WALL_VER: str = "src/view/assets/icons/walls/wall_ver"
WALL_HOR: str = "src/view/assets/icons/walls/wall_hor"
WALL_HERE: str = "_h.png"
WALL_NOTHERE: str = "_nh.png"

WALLS: dict[str, str] = {
    "N": WALL_HOR,
    "S": WALL_HOR,
    "E": WALL_VER,
    "W": WALL_VER
}


class Custom_step(View, ABC):

    """
    A class that represents a step in the custom creation process.
    """

    def __init__(
        self,
        number: int,
        view: View,
        description: str,
        show_next: bool = False
    ) -> None:

        """
        Initializes the main attributes of the step.
        Adds the main view (Custom view), the map, a map renderer,
        aswell as the description of the step.

        Parameters
        ----------
        number: int
            The number of the step in the process.
        view: View
            The main view that handles the whole process.
        description: str
            The text describing the purpose of this step to the user.
        show_next: bool (default False)
            True if the next button should be shown
            at the beginning, False otherwise.
        """

        self.number: int = number
        self.main_view: View = view
        self.map: Map_custom = self.get_attr("map")
        self.map_renderer: Custom_map_renderer = Custom_map_renderer()
        self.description_label: str = description
        self.show_next: bool = show_next
        self.show_message: str = ""
        self.frame_counter: int = 0
        self.is_freed: bool = True
        self._update(True)

    def get_attr(self, attribute: str) -> Any:

        """
        For lint errors, checks that the main view
        is a Custom view and returns the attribute needed.

        Parameters
        ----------
        attribute: str
            The attribute/method to return.

        Returns
        -------
        Any
            The main view's attribute or method.
        """

        if (
            isinstance(self.main_view, Custom_view)
            and hasattr(self.main_view, attribute)
        ):
            return getattr(self.main_view, attribute)

    def _unload_images(self) -> None:

        """
        Unloads the images and textures of all icons
        and sets 'is_freed' to True.
        """

        self.is_freed = True

    def go_back(self) -> None:

        """
        Exits this step and goes back to the previous step.
        """

        self.get_attr("step_back")()

    def go_next(self) -> None:

        """
        Exits this step and goes to the next step.
        """

        self.get_attr("step_forward")()

    def _update_title(self) -> None:

        """
        Builds both the title and description text widgets
        for this step.
        """

        label: str = "STEP " + str(self.number)
        self.title: Text = Text(
            label,
            -2,
            self.h // 15,
            self.h // 10,
            self.w // 3 * 2
        )
        self.description: Text = Text(
            self.description_label,
            -2,
            self.title.lowerbound + self.h // 25,
            self.h // 15,
            self.w // 2
        )
        self.widgets += [self.title, self.description]

    def _update_backnext_buttons(self) -> None:

        """
        Builds the back and next buttons for this step.
        """

        button_w: int = self.w // 12
        button_h: int = self.h // 12
        button_padx: int = self.w // 20
        button_pady: int = self.h // 25
        self.next: ButtonPanel = ButtonPanel(
            self.w - button_w - button_padx,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"next": (self.go_next, None)}
        )
        self.back: ButtonPanel = ButtonPanel(
            self.w - (button_w + button_padx) * 2,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"back": (self.go_back, None)}
        )
        self.widgets.append(self.back)

    @property
    def mid_space(self) -> int:

        """
        Calculates the middle space, between the description text
        and the back/next buttons (this space will serve for the map display).

        Returns
        -------
        int
            The amount of space remaining in the middle.
        """

        h_rem: int = self.h - self.description.lowerbound - (
            self.h - self.back.posy
        )
        return h_rem

    @property
    def map_w(self) -> int:

        """
        Calculates the map width depending on number of cols/rows
        and the amount of space remaining in the middle.

        Returns
        -------
        int
            The width of the display map.
        """

        if self.map.cols >= self.map.rows:
            return self.mid_space - self.mid_space // 10

        return (self.map_h // self.map.rows) * self.map.cols

    @property
    def map_h(self) -> int:

        """
        Calculates the map height depending on number of cols/rows
        and the amount of space remaining in the middle.

        Returns
        -------
        int
            The height of the display map.
        """

        if self.map.rows >= self.map.cols:
            return self.mid_space - self.mid_space // 10

        return (self.map_w // self.map.cols) * self.map.rows

    @property
    def map_x(self) -> int:

        """
        Calculates the map's start x coordinate based on its width.

        Returns
        -------
        int
            The x coordinate of the display map.
        """

        return (self.w - self.map_w) // 2

    @property
    def map_y(self) -> int:

        """
        Calculates the map's start y coordinate based on its height.

        Returns
        -------
        int
            The y coordinate of the display map.
        """

        return (
            (self.h - self.map_h - (self.h - self.back.posy))
            + (self.mid_space - self.map_h) // 2
        )

    @property
    def cell_size(self) -> int:

        """
        Calculates the cell size (on the screen).

        Returns
        -------
        int
            The size of a display cell.
        """

        return self.map_w // self.map.cols

    @property
    def cell_space(self) -> int:

        """
        Calculates the space used to display
        the big cell square for the wall customizing step,
        when the user clicks on an individual cell
        to change its walls.

        Returns
        -------
        int
            The size for the individual cell display.
        """

        return self.map_h // 2

    @property
    def cell_x(self) -> int:

        """
        Calculates the start x coordinate
        for the individual cell display square
        during the wall customizing step.

        Returns
        -------
        int
            The x coordinate for the cell display square.
        """

        return (self.w - self.cell_space) // 2

    @property
    def cell_y(self) -> int:

        """
        Calculates the start y coordinate
        for the individual cell display square
        during the wall customizing step.

        Returns
        -------
        int
            The y coordinate for the cell display square.
        """

        return self.map_y + (self.map_h - self.cell_space) // 2

    @property
    def cell_outline(self) -> tuple[int, int, int, int]:

        """
        Determines the big cell square's outline for drawing lines.

        Returns
        -------
        tuple[int, int, int, int]
            Respectively the x, y, width and height of the cell display square.
        """

        return (self.cell_x, self.cell_y, self.cell_space, self.cell_space)

    def is_in_cell(self, x: int, y: int) -> Cell | None:

        """
        Checks whether or not a set of coordinates
        are located inside a cell on the grid displayed.

        Parameters
        ----------
        x: int
            The x coordinate to check for.
        y: int
            The y coordinate to check for.

        Returns
        -------
        Cell | None
            The cell the coordinates are into if found,
            None otherwise.
        """

        if not self.is_in_map(x, y):
            return None

        col: int = (x - self.map_x) // self.cell_size
        row: int = (y - self.map_y) // self.cell_size
        if 0 <= row < self.map.rows and 0 <= col < self.map.cols:
            return self.map.map.cells[row][col]
        return None

    def is_in_map(self, x: int, y: int) -> bool:

        """
        Checks whether or not a set of coordinates
        are located inside the grid displayed on the screen.

        Parameters
        ----------
        x: int
            The x coordinate to check for.
        y: int
            The y coordinate to check for.

        Returns
        -------
        bool
            True if the coordinates are inside the grid,
            False otherwise.
        """

        if (
            self.map_x <= x <= self.map_x + self.map_w
        ) and (
            self.map_y <= y <= self.map_y + self.map_h
        ):
            return True

        return False

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the window has been resized or an update is required,
        and updates the widgets if so.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_title()
        self._update_backnext_buttons()

    def display_message(self) -> None:

        """
        Displays a message on the screen
        if the 'show_message' attribute is not an empty string
        and the frame counter has not yet reached the end
        of the display time.
        """

        ...

    def display_view(self) -> None:

        """
        Updates and displays the step's widgets,
        aswell as the 'show_message' and the next button
        if the next step is available.
        """

        self._update()

        for widget in self.widgets:
            widget.display_widget()

        if self.show_message:
            self.display_message()

        if self.show_next:
            self.next.display_widget()


class Step_zero(Custom_step):

    """
    A step used for the user to either select an already
    existing custom map to launch, or create a new one from scratch.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step,
        such as its number, all of the custom maps already created,
        and the main view.

        Parameters
        ----------
        main_view: View
            The view overseeing all the steps.
        """

        self.number: int = 0
        self.maps: list[str] = get_stored_map_list(main_view.app.map_folder)
        self.main_view: View = main_view
        self.is_freed: bool = True
        self._update(True)

    def _update_title(self) -> None:

        """
        Builds the title widget for this step.
        """

        self.title: Text = Text(
            "LOAD EXISTING MAP",
            -2,
            self.h // 4,
            self.h // 8
        )
        self.widgets.append(self.title)

    def _update_buttons(self) -> None:

        """
        Builds the back and next buttons for this step.
        """

        button_w: int = self.w // 7
        button_h: int = self.h // 12
        button_padx: int = self.w // 20
        button_pady: int = self.h // 25
        self.back: ButtonPanel = ButtonPanel(
            (self.w - button_w * 2 - button_padx) // 2,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"back": (self.go_back, None)}
        )
        self.next: ButtonPanel = ButtonPanel(
            self.back.posx + button_w + button_padx,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"new map": (self.go_next, None)}
        )
        self.widgets += [self.back, self.next]

    def _update_dropdown(self) -> None:

        """
        Builds the map dropdown widget that allows
        the user to select an already existing custom map
        to launch directly.
        """

        load_label: str = "Select a map"
        dropdown_buttons: dict[str, tuple[Callable, Any]] = {
            load_label: (lambda: 0, None)
        } | {
            map_name: (self.get_attr("launch_game"), map_name)
            for map_name in self.maps
        }
        self.map_dropdown: Dropdown = Dropdown(
            -2,
            self.title.y + self.title.font_size + self.h // 15,
            self.w // 4,
            self.h // 15,
            dropdown_buttons
        )
        self.widgets.append(self.map_dropdown)

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the window has been resized or an update is required,
        and updates the widgets if so.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        if not pr.is_window_resized() and not forced:
            return

        super(Custom_step, self)._update(True)
        self._update_title()
        self._update_buttons()
        self._update_dropdown()

    def display_view(self) -> None:

        """
        Calls the grandparent View's method
        to simply update and display the step's widgets.
        """

        super(Custom_step, self).display_view()


class Step_one(Custom_step):

    """
    A step for the user to define the width/height of their custom map.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step,
        setting the width/height values to default,
        and calling the Custom_step's parent method for the other attributes.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self.is_init: bool = False
        self.width_set: bool = True
        self.height_set: bool = True
        super().__init__(
            1,
            main_view,
            "Choose map size (min 10x10, max 30x30)"
        )
        self.w_input.text_color = pr.GREEN
        self.h_input.text_color = pr.GREEN

    def validate_width(self) -> None:

        """
        Checks and validates the height entered by the user,
        setting the 'show_message' value to a refusal message
        if invalid, otherwise setting the map's rows via the Map_custom.
        """

        input_w = self.w_input.input
        if not input_w.isdigit() or not (10 <= int(input_w) <= 30):

            self.show_message = "Width is invalid, try again"
            self.w_input.input = str(self.map.cols)
            self.width_set = False
            return

        self.w_input.text_color = pr.GREEN
        self.map.set_cols(int(input_w))
        self.width_set = True

    def validate_height(self) -> None:

        """
        Checks and validates the height entered by the user,
        setting the 'show_message' value to a refusal message
        if invalid, otherwise setting the map's rows via the Map_custom.
        """

        input_h = self.h_input.input
        if not input_h.isdigit() or not (10 <= int(input_h) <= 30):

            self.show_message = "Height is invalid, try again"
            self.h_input.input = str(self.map.rows)
            self.height_set = False
            return

        self.h_input.text_color = pr.GREEN
        self.map.set_rows(int(input_h))
        self.height_set = True

    def _update_inputboxes(self) -> None:

        """
        Builds the two input boxes in which the user
        enters the width and height of the map they want to create.
        """

        self.x_sign: Text = Text(
            "  X  ",
            -2,
            self.description.lowerbound + (
                self.mid_space - Text.measure_text(
                    "  X  ", self.mid_space // 10
                )
            ) // 2,
            self.mid_space // 10,
            self.mid_space // 6
        )
        box_w: int = self.mid_space // 3
        box_h: int = self.mid_space // 6
        box_y: int = self.x_sign.y + (self.x_sign.font_size - box_h) // 2
        self.w_input: Input_box = Input_box(
            self.x_sign.x - box_w,
            box_y,
            box_w,
            box_h,
            (self.validate_width, None),
            2,
            (48, 57)
        )
        self.h_input: Input_box = Input_box(
            self.x_sign.x + self.x_sign.width,
            box_y,
            box_w,
            box_h,
            (self.validate_height, None),
            2,
            (48, 57)
        )
        self.w_input.input = str(self.map.cols)
        self.h_input.input = str(self.map.rows)
        self.is_init = True
        self.widgets += [self.x_sign, self.w_input, self.h_input]

    def display_message(self) -> None:

        """
        Builds and displays a text widget showing the refusal message
        if an input entered by the user was invalid.
        """

        if self.frame_counter < MSG_TIME:

            message: Text = Text(
                self.show_message,
                -2,
                self.w_input.posy + self.w_input.h + self.mid_space // 8,
                self.mid_space // 10,
                self.mid_space,
                pr.RED
            )
            message.display_widget()
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.frame_counter = 0

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the width/height have finished being set,
        and if so toggling the 'next' button so that the user
        can go to the next step.
        Also checks if the window has been resized or an update is required,
        and updating widgets if needed.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        if self.is_init:
            self.width_set = not self.w_input.enter_input
            self.height_set = not self.h_input.enter_input
        self.show_next = (self.width_set and self.height_set)

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_inputboxes()


class Step_two(Custom_step):

    """
    A step for the user to customize the map's walls.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step,
        setting the 'show_cell' value to False
        (until the user clicks on a specific cell,
        the big square individual cell is not shown),
        and calling the Custom_step's parent method for the other attributes.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self.show_cell: bool = False
        self.is_init: bool = False
        super().__init__(
            2,
            main_view,
            "Place the walls (click on each cell)",
            True
        )
        self.is_init = True

    def go_back(self) -> None:

        """
        Exits this step and goes back to the previous step,
        resetting the map to default (empty walls).
        """

        self.map.reset()
        super().go_back()

    def go_next(self) -> None:

        """
        Exits this step and goes to the next step,
        setting the main view's map properties, so that they
        can be preserved to be used by later views.
        """

        self.map.walls_set = True
        self.get_attr("set_map_properties")(
            self.map_x, self.map_y, self.map_w, self.map_h, self.cell_size
        )
        super().go_next()

    def randomize_walls(self) -> None:

        """
        Randomizes the map's walls.
        """

        self.map.randomize_wall()
        self._update(True)

    def _update_randomize_button(self) -> None:

        """
        Builds the randomize button that allows the user
        to randomize all walls in the map.
        """

        h_rem: int = self.h - (self.map_y + self.map_h)
        button_h: int = h_rem // 2
        self.rand_button: ButtonPanel = ButtonPanel(
            -2,
            self.h - button_h - h_rem // 4,
            self.w // 7,
            button_h,
            {"randomize walls": (self.randomize_walls, None)}
        )
        self.widgets.append(self.rand_button)

    def _unload_images(self) -> None:

        """
        Unloads the images and textures of all icons,
        including the walls' textures, and sets 'is_freed' to True.
        """

        if hasattr(self, "walls") and not self.is_freed:

            for icons in self.walls.values():
                icons[0]._unload_image()
                icons[1]._unload_image()

        super()._unload_images()

    def _update_walls(self) -> None:

        """
        Builds the two wall icons (vertical/horizontal)
        and calculates what their position would be inside
        the big square cell if it's being displayed.
        """

        wall_pad: int = self.cell_space // 12
        wall_w: int = self.cell_space // 8
        wall_h: int = self.cell_space - (wall_pad + wall_w) * 2
        self.wall_pos: dict[str, tuple[int, int, int, int]] = {
            "N": (
                self.cell_x + wall_pad + wall_w, self.cell_y + wall_pad,
                wall_h, wall_w
            ),
            "S": (
                self.cell_x + wall_pad + wall_w,
                self.cell_y + self.cell_space - wall_pad - wall_w,
                wall_h, wall_w
            ),
            "W": (
                self.cell_x + wall_pad, self.cell_y + wall_pad + wall_w,
                wall_w, wall_h
            ),
            "E": (
                self.cell_x + self.cell_space - wall_pad - wall_w,
                self.cell_y + wall_pad + wall_w,
                wall_w, wall_h
            )
        }
        self.walls: dict[str, tuple[ClickableIcon, ClickableIcon]] = {}
        for wall in ["N", "S", "E", "W"]:
            self.walls[wall] = (
                ClickableIcon(
                    self.wall_pos[wall][0],
                    self.wall_pos[wall][1],
                    WALLS[wall] + WALL_HERE,
                    (self.change_wall, wall),
                    (self.wall_pos[wall][2], self.wall_pos[wall][3]),
                    True,
                    False
                ),
                ClickableIcon(
                    self.wall_pos[wall][0],
                    self.wall_pos[wall][1],
                    WALLS[wall] + WALL_NOTHERE,
                    (self.change_wall, wall),
                    (self.wall_pos[wall][2], self.wall_pos[wall][3]),
                    True,
                    False
                )
            )

    def change_wall(self, wall: str) -> None:

        """
        Toggles the wall for the cell
        currently being customized.

        Parameters
        ----------
        wall: str
            The wall (N, S, W, or E) to toggle on/off.
        """

        if not self.show_cell:
            return

        self.map.change_wall(*self.cur_cell, wall)

    def display_cell(self) -> None:

        """
        Displays the big square cell in the middle of the map,
        so that the user can customize the walls for each individual cell.
        """

        if not self.show_cell:
            return

        pr.draw_rectangle(*self.cell_outline, pr.DARKGRAY)
        pr.draw_rectangle_lines(*self.cell_outline, pr.LIGHTGRAY)

        for wall, state in self.map.get_walls(*self.cur_cell).items():

            wall_show: int = 1

            if True in state:
                wall_show = 0

            self.walls[wall][wall_show].display_widget()

    def set_cur_cell(self, x: int, y: int) -> None:

        """
        Sets the value of the current cell being displayed,
        storing its coordinates and updating the walls.

        Parameters
        ----------
        x: int
            The x coordinate of the cell inside the grid.
        y: int
            The y coordinate of the cell inside the grid.
        """

        self.show_cell = True
        self.cur_cell: tuple[int, int] = (x, y)
        self._unload_images()
        self._update_walls()
        self.is_freed = False

    def is_in_bigcell(self, x: int, y: int) -> bool:

        """
        Determines whether or not the coordinates given
        are inside of the big square cell displayed.

        Parameters
        ----------
        x: int
            The x coordinate to check for.
        y: int
            The y coordinate to check for.

        Returns
        -------
        bool
            True if the coordinates are inside, False otherwise.
        """

        return (
            self.cell_x <= x <= self.cell_x + self.cell_space
            and self.cell_y <= y <= self.cell_y + self.cell_space
        )

    def handle_input(self, x: int, y: int) -> None:

        """
        Checks if the user's mouse clicking is on a cell,
        or inside the big cell square displayed.

        Parameters
        ----------
        x: int
            The x coordinate of the user's mouse.
        y: int
            The y coordinate of the user's mouse.
        """

        if self.show_cell and not self.is_in_bigcell(x, y):
            self.show_cell = False
            self._update_grid()

        elif not self.show_cell and self.is_in_map(x, y):
            cell: Cell | None = self.is_in_cell(x, y)
            if cell:
                self.set_cur_cell(cell.pos_x, cell.pos_y)

        return

    def _update_grid(self) -> None:

        """
        Builds the map renderer's grid texture
        by passing it the current grid and its parameters.
        """

        self.map_renderer.update_special_grid(
            self.map.map.cells,
            (self.map_w, self.map_h),
            (self.map_x, self.map_y),
            self.cell_size,
            True
        )
        self.is_freed = False

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the user mouse's left button has been clicked,
        if the window has been resized or an update is required,
        and updates the widgets/textures if so.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        if self.is_init and pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT):
            self.handle_input(pr.get_mouse_x(), pr.get_mouse_y())

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_backnext_buttons()
        self._update_randomize_button()
        self._update_grid()
        self.is_freed = False

    def display_view(self) -> None:

        """
        Updates and displays the step's widgets,
        aswell as the grid texture for the map
        and the big square cell if the user has clicked
        on a specific cell to customize.
        """

        super().display_view()

        self.map_renderer.display_grid()

        if self.show_cell:
            self.display_cell()


class Step_three(Custom_step):

    """
    A step used for the user to place PacMan's spawn point
    and the different collectibles of the game.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step,
        setting all of the sprites/textures' names,
        and calling the Custom_step's parent method for the other attributes.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self._init_names(main_view)
        self.sprites: list[str] = (
            ["pacman_idle"]
            + self.consumable_names
            + self.collectible_names
        )
        super().__init__(
            3,
            main_view,
            "Place PacMan and the collectibles (at least 1 collectible)"
        )

    def _init_names(self, main_view: View) -> None:

        """
        Initializes all of the textures' names
        that the step is going to use in the display,
        aswell as creating the dictionary containing
        the sprites the user has already placed.

        Parameters
        ----------
        main_view: View
            The main view overseeing every step
            (needed to get the correct texture pack before super().__init__).
        """

        self.texture_pack: Texture_pack = Texture_pack(
            main_view.app.display_config.texture_pack
        )
        self.entity_names: list[str] = [
            "pacman", "blinky", "inky", "pinky", "clyde"
        ]
        self.consumable_names: list[str] = [
            "cherry_c", "galaxian_c", "apple_c", "orange_c",
            "strawberry_c", "key_c", "bell_c", "melon_c"
        ]
        self.collectible_names: list[str] = (
            self.consumable_names
            + ["pacgum", "super_pacgum"]
        )
        self.sprites_set: dict[str, tuple[list[Cell], int]] = {}
        self.current_sprite: str = ""

    @property
    def map_x(self) -> int:

        """
        Gets the correct map start x coordinate
        from the main Custom view.

        Returns
        -------
        int
            The map's already defined start x coordinate.
        """

        return int(self.get_attr("map_x"))

    @property
    def map_y(self) -> int:

        """
        Gets the correct map start y coordinate
        from the main Custom view.

        Returns
        -------
        int
            The map's already defined start y coordinate.
        """

        return int(self.get_attr("map_y"))

    @property
    def map_w(self) -> int:

        """
        Gets the correct map width from the main Custom view.

        Returns
        -------
        int
            The map's already defined width.
        """

        return int(self.get_attr("map_w"))

    @property
    def map_h(self) -> int:

        """
        Gets the correct map height from the main Custom view.

        Returns
        -------
        int
            The map's already defined height.
        """

        return int(self.get_attr("map_h"))

    @property
    def cell_size(self) -> int:

        """
        Gets the correct cell size from the main Custom view.

        Returns
        -------
        int
            The map's already defined cell size.
        """

        return int(self.get_attr("cell_size"))

    def calculate_cell_pos(self, x: int, y: int) -> tuple[int, int] | None:

        """
        Calculates the position on the screen of the given
        cell coordinates (the x and y given being the place of the cell
        inside the grid, not on the screen).

        Parameters
        ----------
        x: int
            The cell's x position inside the grid (col index).
        y: int
            The cell's y position inside the grid (row index).

        Returns
        -------
        tuple[int, int] | None
            If found, the x and y coordinates of the cell (but on the screen),
            None otherwise.
        """

        if x < 0 or x >= self.map.cols:
            return None

        if y < 0 or y >= self.map.rows:
            return None

        return (
            self.map_x + self.cell_size * x,
            self.map_y + self.cell_size * y
        )

    def activate_sprite(self, spr_name: str) -> None:

        """
        Activates the placement mode for the given sprite,
        which means that an icon
        of the current activated sprite will now appear
        under the user's mouse cursor when it hovers over the map,
        allowing the user to simply click where they wish to place it
        for it to become set in the corresponding cell.

        Parameters
        ----------
        spr_name: str
            The name of the sprite to activate.
        """

        if (
            spr_name in self.collectible_names
            and self.map.pacman_spawn_set is False
        ):
            self.show_message = "Please place PacMan before collectibles"
            return

        elif spr_name.startswith("pacman"):
            to_remove: list[str] = [
                t_name for t_name in self.sprites_set.keys()
                if t_name in self.collectible_names
            ]
            for spr in to_remove:
                self.sprites_set.pop(spr)

        self.current_sprite = spr_name

        if spr_name in self.sprites_set.keys():
            self.sprites_set.pop(spr_name)

    def get_consumable_type(self, consumable_name: str) -> Consumable_type:

        """
        Gets the correct Consumable_type from the Enum
        based on the name of the consumable.

        Parameters
        ----------
        consumable_name: str
            The name of the consumable as a string,
            to convert into a Consumable_type.

        Returns
        -------
        Consumable_type
            The member of the type which corresponds to the string name.
            If not found, replaces it with the cherry.
        """

        for cons_type in Consumable_type:
            if cons_type.value == consumable_name:
                return cons_type
        return Consumable_type.CHERRY

    def set_sprite(self, x: int, y: int, spr_name: str) -> bool:

        """
        Determines the correct setting function to call
        based on the sprite's name and type, and returns
        the result of the call (validated or refused).

        Parameters
        ----------
        x: int
            The cell x coordinate in which the sprite has to be set.
        y: int
            The cell y coordinate in which the sprite has to be set.
        spr_name: str
            The name of the sprite to place.

        Returns
        -------
        bool
            True if the placement of this entity/collectible
            inside this cell was possible, False otherwise.
        """

        if spr_name == "pacman_idle":
            return self.map.set_pacman_spawn(x, y)
        elif spr_name in self.consumable_names:
            return self.map.set_collectible(
                x, y, Consumable(
                    self.get_consumable_type(spr_name.removesuffix("_c")),
                    x,
                    y
                )
            )
        elif spr_name == "super_pacgum":
            return self.map.set_collectible(x, y, Super_Pacgum(x, y))
        elif spr_name == "pacgum":
            return self.map.set_collectible(x, y, Pacgum(x, y))
        return False

    def try_place_sprite(self) -> None:

        """
        Attempts to place the current sprite inside the cell
        in which the user has clicked, and storing the sprite
        along with the cell and the proper texture size
        as a tuple inside the 'sprites_set' dictionary,
        to be displayed by the map renderer.
        """

        if not self.current_sprite:
            return

        if self.current_sprite not in self.textures:
            return

        if (
            self.current_sprite in self.sprites_set
            and self.current_sprite not in self.collectible_names
        ):
            return

        cell: Cell | None = self.is_in_cell(
            pr.get_mouse_x(),
            pr.get_mouse_y()
        )
        if not cell:
            return

        if self.set_sprite(cell.pos_x, cell.pos_y, self.current_sprite):

            if (
                self.current_sprite in self.collectible_names
                and self.current_sprite in self.sprites_set.keys()
            ):
                self.sprites_set[self.current_sprite][0].append(cell)
            else:
                self.sprites_set[self.current_sprite] = (
                    [cell],
                    self.texture_size(self.current_sprite)
                )
            if self.current_sprite not in self.collectible_names:
                self.current_sprite = ""

        else:

            self.show_message = "Cannot place here, try elsewhere"

    def texture_size(self, sprite_name: str) -> int:

        """
        Determines the correct texture size for the given sprite
        based on its type (entity/collecible/consumable).

        Parameters
        ----------
        sprite_name: str
            The name of the sprite for which to get the texture size.

        Returns
        -------
        int
            The correct size for the sprite's texture.
        """

        if any(sprite_name.startswith(e_name) for e_name in self.entity_names):
            return self.map_renderer.entity_size
        elif sprite_name in self.consumable_names:
            return self.map_renderer.consumable_size
        elif sprite_name in self.collectible_names:
            return self.map_renderer.collectible_size
        return 0

    def _unload_images(self) -> None:

        """
        Unloads the images and textures of all icons,
        including the grid texture of the map renderer,
        and sets 'is_freed' to True.
        """

        if self.is_freed:
            return

        if hasattr(self, "textures"):
            for icon in self.textures.values():
                icon._unload_image()

        if hasattr(self, "side_textures"):
            for icon in self.side_textures.values():
                icon._unload_image()

        if hasattr(self, "map_renderer"):
            self.map_renderer._unload_images()

        super()._unload_images()

    def _update_textures(self) -> None:

        """
        Builds all the needed icons that will be used
        in the display.
        """

        self.textures: dict[str, Icon] = {
            t_name: Icon(
                0,
                0,
                self.texture_pack.get_texture(t_name),
                (self.texture_size(t_name), self.texture_size(t_name)),
                True
            ) for t_name in (self.sprites + list(self.sprites_set.keys()))
        }
        self._update_sidetextures()

    def _update_sidetextures(self) -> None:

        """
        Builds the side icons that the user can click on
        to activate the placement mode for a specific sprite.
        """

        side_text_sz: int = (
            self.map_h // (len(self.collectible_names) // 2 + 1)
        )
        t_pad: int = self.map_h // 50
        side_text_sz = min(side_text_sz - t_pad * 2, self.map_x * 3 // 4)

        pacman_icon: ClickableIcon = ClickableIcon(
            (self.map_x - side_text_sz) // 2,
            self.map_y + t_pad,
            self.texture_pack.get_texture("pacman_idle"),
            (self.activate_sprite, "pacman_idle"),
            (side_text_sz, side_text_sz),
            True,
            False
        )

        w_rem: int = self.map_x - side_text_sz * 2
        fst_x: int = w_rem // 5 * 2
        scd_x: int = fst_x + side_text_sz + w_rem // 5

        self.side_textures: dict[str, ClickableIcon] = {
            "pacman_idle": pacman_icon
        }

        t_x: int = fst_x
        t_y: int = self.map_y + (t_pad + side_text_sz) * 2

        for i, t_name in enumerate(self.collectible_names):

            if i == len(self.collectible_names) // 2:
                t_x = scd_x
                t_y = self.map_y + (t_pad + side_text_sz) * 2

            self.side_textures[t_name] = ClickableIcon(
                t_x,
                t_y,
                self.texture_pack.get_texture(t_name),
                (self.activate_sprite, t_name),
                (side_text_sz, side_text_sz),
                True,
                False
            )
            t_y += side_text_sz + t_pad

    def display_textures(self) -> None:

        """
        Displays all the icons (set sprites, side icons, grid texture, etc).
        """

        self.map_renderer.display_set_sprites([
            (self.textures[spr_name], cells, size)
            for spr_name, (cells, size) in self.sprites_set.items()
        ])

        for side_texture in self.side_textures.values():
            side_texture.display_widget()

        if self.current_sprite:

            cell: Cell | None = self.is_in_cell(
                pr.get_mouse_x(),
                pr.get_mouse_y()
            )
            if not cell:
                return

            self.map_renderer.display_cur_sprite(
                self.textures[self.current_sprite],
                cell,
                self.texture_size(self.current_sprite)
            )

    def display_message(self) -> None:

        """
        Displays a message under the map if needed,
        for example if the user doesn't place the sprites
        in order.
        """

        if self.frame_counter < MSG_TIME:

            msg_h: int = self.h - (
                self.map_y + self.map_h
            )
            message: Text = Text(
                self.show_message,
                -2,
                self.map_y + self.map_h + (msg_h - msg_h // 2) // 2,
                msg_h // 2,
                self.map_w,
                pr.RED
            )
            message.display_widget()
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.frame_counter = 0

    def check_next(self) -> None:

        """
        Checks whether or not PacMan's spawn point
        has been set, aswell as at least one collectible,
        which allows the 'next' button to be shown to the user.
        """

        self.show_next = (
            self.map.pacman_spawn_set
            and self.map.map.collectible_count > 0
        )

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the user can go to the next step,
        if the user has clicked somewhere (trying to place a sprite),
        if the window has been resized or an update is required,
        and updates the textures/icons if so.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        self.check_next()

        if pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT):
            self.try_place_sprite()

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self.map_renderer.update_special_grid(
            self.map.map.cells,
            (self.map_w, self.map_h),
            (self.map_x, self.map_y),
            self.cell_size
        )
        self._update_textures()

    def display_view(self) -> None:

        """
        Updates and displays the step, mainly the grid
        and sprites via the map renderer.
        """

        super().display_view()

        self.map_renderer.display_grid()
        self.display_textures()


class Step_four(Step_three):

    """
    A step used for the user to place the Ghosts' spawn and scatter points.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main attributes of the step,
        setting all of the sprites/textures' names,
        getting the previous view's already placed sprites via the main view,
        and calling the Custom_step's parent method for the other attributes.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self._init_names(main_view)
        self.spawn_sprites: list[str] = [
            en_name + "_idle"
            for en_name in self.entity_names
            if en_name != "pacman"
        ]
        self.scatter_sprites: list[str] = [
            en_name + "_scatter"
            for en_name in self.entity_names
            if en_name != "pacman"
        ]
        self.sprites: list[str] = self.spawn_sprites + self.scatter_sprites
        if isinstance(main_view, Custom_view):
            for step in main_view.steps_completed:
                if step.number == 3 and isinstance(step, Step_three):
                    self.sprites_set = {
                        k: val for k, val in step.sprites_set.items()
                    }

        super(Step_three, self).__init__(
            4,
            main_view,
            "Place the Ghosts spawn and scatter points (spawn first)"
        )

    def activate_sprite(self, spr_name: str) -> None:

        """
        Activates the placement mode for the given sprite,
        which means that an icon
        of the current activated sprite will now appear
        under the user's mouse cursor when it hovers over the map,
        allowing the user to simply click where they wish to place it
        for it to become set in the corresponding cell.
        Also sets the 'show_message' value to display a refusal message
        in case the user tries to place the scatter before the spawn points.

        Parameters
        ----------
        spr_name: str
            The name of the sprite to activate.
        """

        if (
            spr_name in self.scatter_sprites
            and not all(self.map.ghost_spawn_set.values())
        ):
            self.show_message = (
                "Place the spawn points of all ghosts first"
            )
            return

        self.current_sprite = spr_name

        if spr_name in self.sprites_set.keys():
            self.sprites_set.pop(spr_name)

    def set_sprite(self, x: int, y: int, spr_name: str) -> bool:

        """
        Determines the correct setting function to call
        based on the sprite's name (spawn/scatter), and returns
        the result of the call (validated or refused).

        Parameters
        ----------
        x: int
            The cell x coordinate in which the sprite has to be set.
        y: int
            The cell y coordinate in which the sprite has to be set.
        spr_name: str
            The name of the sprite to place.

        Returns
        -------
        bool
            True if the placement of this ghost spawn/scatter
            inside this cell was possible, False otherwise.
        """

        if spr_name in self.spawn_sprites:
            return self.map.set_ghost_spawn(
                x, y, spr_name.removesuffix("_idle").upper()
            )
        elif spr_name in self.scatter_sprites:
            return self.map.set_ghost_scatter(
                x, y, spr_name.removesuffix("_scatter").upper()
            )
        return False

    def _update_sidetextures(self) -> None:

        """
        Builds the side icons that the user can click on
        to activate the placement mode for a specific sprite.
        """

        side_text_sz: int = self.map_h // (len(self.sprites) // 2)
        t_pad: int = self.map_h // 50
        side_text_sz = min(side_text_sz - t_pad * 2, self.map_x * 3 // 4)
        fst_t_x: int = (self.map_x - side_text_sz * 2 - side_text_sz // 2) // 2
        scd_t_x: int = fst_t_x + side_text_sz + side_text_sz // 2

        self.side_textures: dict[str, ClickableIcon] = {
            t_name: ClickableIcon(
                fst_t_x,
                self.map_y + i * (side_text_sz + t_pad * 2) + t_pad,
                self.texture_pack.get_texture(t_name),
                (self.activate_sprite, t_name),
                (side_text_sz, side_text_sz),
                True,
                False
            ) for i, t_name in enumerate(self.spawn_sprites)
        } | {
            t_name: ClickableIcon(
                scd_t_x,
                self.map_y + i * (side_text_sz + t_pad * 2) + t_pad,
                self.texture_pack.get_texture(t_name),
                (self.activate_sprite, t_name),
                (side_text_sz, side_text_sz),
                True,
                False
            ) for i, t_name in enumerate(self.scatter_sprites)
        }

    def check_next(self) -> None:

        """
        Checks whether or not all of the Ghosts' spawn/scatter points
        has been set, which allows the 'next' button to be shown to the user.
        """

        self.show_next = (
            all(self.map.ghost_spawn_set.values())
            and all(self.map.ghost_scatter_set.values())
        )


class Step_five(Custom_step):

    """
    A step for the user to enter the name of their custom map.
    """

    def __init__(self, main_view: View) -> None:

        """
        Calls the Custom_step's parent method for the main attributes.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        super().__init__(
            5,
            main_view,
            "Choose a name for your map"
        )

    def validate_name(self) -> None:

        """
        Checks and validates the name for the custom map
        entered by the user, setting the 'show_message' value
        to a confirmation/refusal message depending on if it's valid.
        """

        if self.map.set_name(self.input_box.input):
            self.show_message = (
                f"Saved the name '{self.input_box.input}' for your custom map"
            )
            self.input_box.text_color = pr.GREEN
            self.input_box.cursor_color = pr.DARKGREEN
        else:
            self.show_message = f"Name '{self.input_box.input}' invalid"
            self.input_box.text_color = pr.RED
            self.input_box.cursor_color = pr.MAROON

    def _update_inputbox(self) -> None:

        """
        Builds the input box in which the user enters the name
        of their custom map, only allowing for non-existing name
        and alphabetical characters + '-' and '_'.
        """

        all_characters: list[int] = [45, 95]
        for crange in [(48, 58), (65, 91), (97, 123)]:
            all_characters += [i for i in range(*crange)]

        self.input_box: Input_box = Input_box(
            -2,
            -2,
            self.w // 3,
            self.h // 10,
            (self.validate_name, None),
            20,
            all_characters
        )

        h_rem: int = (
            self.h
            - self.description.lowerbound
            - (self.h - self.input_box.posy)
        )
        self.input_label: Text = Text(
            "enter name (only alphabetical and '_', '-' allowed) :",
            -2,
            self.description.lowerbound + h_rem // 3 * 2 - self.h // 25,
            self.h // 25
        )
        self.widgets += [self.input_label, self.input_box]

    def display_message(self) -> None:

        """
        Builds and displays a text message
        for the confirmation/refusal of the map's name entered,
        if the frame counter has not yet reached the end of the display time.
        """

        if self.frame_counter < MSG_TIME:

            message: Text = Text(
                self.show_message,
                -2,
                self.input_box.posy + self.input_box.h + self.h // 10,
                self.h // 25,
                self.w // 2,
                self.input_box.text_color
            )
            message.display_widget()
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.input_box.text_color = (
                self.input_box.base_colors[1]
            )
            self.input_box.cursor_color = (
                self.input_box.base_colors[2]
            )
            self.frame_counter = 0

    def go_next(self) -> None:

        """
        Exits this step and goes to the next step,
        saving the custom map's layout and information.
        """

        self.map.save_map()
        super().go_next()

    def go_back(self) -> None:

        """
        Exits this step and goes back to the previous step,
        resetting the name of the map to undefined.
        """

        self.map.name_set = False
        super().go_back()

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the user has entered their custom map's name
        and can go to the next step,
        if the window has been resized or an update is required,
        and updates the widgets if so.
        Also changes the label of the 'next' button
        already built by the parent Custom_step's 'update_backnext_buttons'
        to indicate 'save' instead.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        self.show_next = self.map.name_set

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self.next.buttons["next"].label = "save"
        self._update_inputbox()


class Step_six(Custom_step):

    """
    A last step used for the user to launch their finished custom map
    or instead return to the main menu.
    """

    def __init__(self, main_view: View) -> None:

        """
        Initializes the main view and map of the step and updates a first time.

        Parameters
        ----------
        main_view: View
            The main view that handles the whole process.
        """

        self.main_view: View = main_view
        self.map: Map_custom = self.get_attr("map")
        self.is_freed: bool = True
        self._update(True)

    def _update_widgets(self) -> None:

        """
        Builds the yes, no buttons that the user can click on
        to either launch their custom map or return to the main menu.
        Also builds the indicative text widgets 'question' and 'description'.
        """
        button_w: int = self.w // 15
        button_h: int = self.h // 10
        self.yes_button: ButtonPanel = ButtonPanel(
            (self.w - button_w * 3) // 2,
            -2,
            button_w,
            button_h,
            {"yes": (self.get_attr("launch_game"), self.map.map.name)}
        )
        self.no_button: ButtonPanel = ButtonPanel(
            self.yes_button.posx + button_w * 2,
            -2,
            button_w,
            button_h,
            {"no": (self.get_attr("go_to_menu"), None)}
        )
        self.question: Text = Text(
            "Start the game?",
            -2,
            (self.h - self.yes_button.posy) // 3,
            self.h // 10
        )
        self.description: Text = Text(
            "(you can load your map at any time from the menu)",
            -2,
            self.question.lowerbound + self.h // 25,
            self.h // 20
        )
        self.widgets += [
            self.yes_button,
            self.no_button,
            self.question,
            self.description
        ]

    def _update(self, forced: bool = False) -> None:

        """
        Checks if the window has been resized or an update is required,
        and updates the widgets if so.

        Parameters
        ----------
        forced: bool (default False)
            True if the step MUST be updated, False otherwise.
        """

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_widgets()
        self.is_freed = False

    def display_view(self) -> None:

        """
        Calls the grandparent View's display method
        to simply update and display all of the step's widgets.
        """

        super(Custom_step, self).display_view()


class Custom_view(View):

    """
    A view used to allow the user to load/create their own custom maps,
    by going through a step-by-step process.
    """

    def __init__(self, app: "App") -> None:

        """
        Initializes the main attributes of the view,
        mainly the app, instanciates the Map_custom map,
        and defines the list of steps for the creation process.

        Parameters
        ----------
        app: App
            The main app that handles everything.
        """

        self.app: "App" = app
        self.map: Map_custom = Map_custom(self.app.map_folder)
        self.is_freed: bool = False

        self.steps: list = []

        maps: list[str] = get_stored_map_list(self.app.map_folder)
        if maps != ["mandatory", "arcade"]:
            self.steps.append(Step_zero)

        self.steps += [
            Step_one,
            Step_two,
            Step_three,
            Step_four,
            Step_five,
            Step_six
        ]
        self.steps_completed: list[Custom_step] = []
        self.sprites_set: list[tuple[Icon, Cell]] = []

        self.cur_step_index: int = 0
        self.cur_step: Custom_step = self.steps[0](self)

        self.set_map_properties(0, 0, 0, 0, 0)

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
