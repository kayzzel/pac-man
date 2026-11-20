import pyray as pr

from typing import Any
from abc import ABC

from ..View import View
from ..renderer.Map_renderer import Custom_map_renderer
from ...widgets import Text, ButtonPanel

from src.game.map.Cell import Cell
from src.game.map.Map_custom import Maps_custom, Map_custom


MSG_TIME: int = 120


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
        self.maps: Maps_custom = self.get_attr("maps")
        self.map: Map_custom = self.get_attr("current_map")
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
        has the attribute and returns the attribute needed.

        Parameters
        ----------
        attribute: str
            The attribute/method to return.

        Returns
        -------
        Any
            The main view's attribute or method.
        """

        if hasattr(self.main_view, attribute):
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
            self.description.lowerbound + (self.mid_space - self.map_h) // 2
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

    def display_view(self) -> None:

        """
        Updates and displays the step's widgets,
        including the next button if the step is completed.
        """

        super().display_view()
        if self.show_next:
            self.next.display_widget()

    def display_message(self) -> None:

        """
        Displays a message on the screen
        if the 'show_message' attribute is not an empty string
        and the frame counter has not yet reached the end
        of the display time.
        """

        ...
