import pyray as pr

from pyray import MouseButton as mb

from .Custom_step import Custom_step, MSG_TIME
from ..View import View
from ...widgets import Widget, Text, ButtonPanel, ClickableIcon

from src.game.map.Cell import Cell


WALL_VER: str = "assets/icons/walls/wall_ver"
WALL_HOR: str = "assets/icons/walls/wall_hor"
WALL_HERE: str = "_h.png"
WALL_NOTHERE: str = "_nh.png"

WALLS: dict[str, str] = {
    "N": WALL_HOR,
    "S": WALL_HOR,
    "E": WALL_VER,
    "W": WALL_VER
}


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

        try:
            self.map.randomize_wall()
        except ValueError:
            self.show_message = "Couldn't randomize the walls"
            return
        self._update(True)

    def _update_randomize_button(self) -> None:

        """
        Builds the randomize button that allows the user
        to randomize all walls in the map.
        """

        h_rem: int = self.h - (self.map_y + self.map_h)
        button_h: int = min(self.h // 12, h_rem // 2)
        self.rand_button: ButtonPanel = ButtonPanel(
            -2,
            self.h - h_rem + (h_rem - button_h) // 2,
            self.w // 6,
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

    def display_message(self) -> None:

        """
        Builds and displays a text widget showing the refusal message
        if an error occurred when setting the walls.
        """

        if self.frame_counter < MSG_TIME:

            message: Text = Text(
                self.show_message,
                -2,
                self.description.lowerbound + self.h // 40,
                self.h // 25,
                self.w // 2,
                pr.MAROON
            )
            message.display_widget()
            self.frame_counter += 1

        else:

            self.show_message = ""
            self.frame_counter = 0

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
