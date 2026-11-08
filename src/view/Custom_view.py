import pyray as pr
# from pyray import get_screen_width as sw
# from pyray import get_screen_height as sh
from pyray import MouseButton as mb
from abc import ABC
from ..game.map.Map_custom import Map_custom
from .View import View
from .Map_renderer import Custom_map_renderer
from .widget import Widget, Text, ButtonPanel, Input_box, ClickableIcon


MSG_TIME: int = 80

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

    def __init__(
        self,
        number: int,
        view: View,
        cmap: Map_custom,
        description: str,
        show_next: bool = False
    ) -> None:

        self.number: int = number
        self.main_view: View = view
        self.map: Map_custom = cmap
        self.description_label: str = description
        self.show_next: bool = show_next
        self._update(True)

    def _update_title(self) -> None:

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

        button_w: int = self.w // 12
        button_h: int = self.h // 12
        button_padx: int = self.w // 20
        button_pady: int = self.h // 25
        self.next: ButtonPanel = ButtonPanel(
            self.w - button_w - button_padx,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"next": (self.main_view.change_step, 1)}
        )
        self.back: ButtonPanel = ButtonPanel(
            self.w - (button_w + button_padx) * 2,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"back": (self.main_view.change_step, -1)}
        )
        self.widgets.append(self.back)

    @property
    def mid_space(self) -> int:

        h_rem: int = self.h - self.description.lowerbound - (
            self.h - self.back.posy
        )
        return h_rem

    @property
    def map_w(self) -> int:

        if self.map.cols >= self.map.rows:
            return self.mid_space - self.mid_space // 10

        return (self.map_h // self.map.rows) * self.map.cols

    @property
    def map_h(self) -> int:

        if self.map.rows >= self.map.cols:
            return self.mid_space - self.mid_space // 10

        return (self.map_w // self.map.cols) * self.map.rows

    @property
    def map_x(self) -> int:

        return (self.w - self.map_w) // 2

    @property
    def map_y(self) -> int:

        return (
            (self.h - self.map_h - (self.h - self.back.posy))
            + (self.mid_space - self.map_h) // 2
        )

    @property
    def cell_size(self) -> int:

        return self.map_w // self.map.cols

    def _update(self, forced: bool = False) -> None:

        if not pr.is_window_resized() and not forced:
            return

        self.widgets: list[Widget] = []
        self._update_title()
        self._update_backnext_buttons()

    def display_view(self) -> None:

        for widget in self.widgets:
            widget.display_widget()

        if self.show_next:
            self.next.display_widget()


class Step_one(Custom_step):

    def __init__(self, main_view: View, cmap: Map_custom) -> None:

        self.show_message: str = ""
        super().__init__(
            1,
            main_view,
            cmap,
            "Choose map size (min 5x5, max 20x20)"
        )

    def validate_width(self) -> None:

        input_w = self.w_input.input
        if not input_w.isdigit() or not (10 <= int(input_w) <= 30):

            self.show_message = "Width is invalid, try again"
            self.frame_counter: int = 0
            self.w_input.input = str(self.map.cols)
            return

        self.w_input.text_color = pr.GREEN
        self.map.set_cols(int(input_w))

    def validate_height(self) -> None:

        input_h = self.h_input.input
        if not input_h.isdigit() or not (10 <= int(input_h) <= 30):

            self.show_message = "Height is invalid, try again"
            self.frame_counter = 0
            self.h_input.input = str(self.map.rows)
            return

        self.h_input.text_color = pr.GREEN
        self.map.set_rows(int(input_h))

    def _update_inputboxes(self) -> None:

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
        self.widgets += [self.x_sign, self.w_input, self.h_input]

    def display_message(self) -> None:

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

    def _update(self, forced: bool = False) -> None:

        if self.map.cols != 0 and self.map.rows != 0:
            self.show_next = True

        else:
            self.show_next = False

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_inputboxes()

    def display_view(self) -> None:

        self._update()

        if self.show_message:
            self.display_message()

        super().display_view()


class Step_two(Custom_step):

    def __init__(self, main_view: View, cmap: Map_custom) -> None:

        self.show_cell: bool = False
        self.map_renderer: Custom_map_renderer = Custom_map_renderer()
        super().__init__(
            2,
            main_view,
            cmap,
            "Place the walls (click on each cell)",
            True
        )

    def is_in_cell(self, x: int, y: int) -> bool:

        cell_y: int = self.map_y
        for row_i, row in enumerate(self.map.map.cells):

            cell_x: int = self.map_x
            for cell_i, cell in enumerate(row):

                if (
                    cell_x <= x < cell_x + self.cell_size
                ) and (
                    cell_y <= y < cell_y + self.cell_size
                ):
                    return True

            cell_x += self.cell_size
        cell_y += self.cell_size

        return False

    def is_in_map(self, x: int, y: int) -> bool:

        if (
            self.map_x <= x <= self.map_x + self.map_w
        ) and (
            self.map_y <= y <= self.map_y + self.map_h
        ):
            return True

        return False

    @property
    def cell_space(self) -> int:

        return self.map_h // 2

    @property
    def cell_x(self) -> int:

        return (self.w - self.cell_space) // 2

    @property
    def cell_y(self) -> int:

        return self.map_y + (self.map_h - self.cell_space) // 2

    def randomize_walls(self) -> None:

        self.map.randomize_wall()
        self._update(True)

    def _update_randomize_button(self) -> None:

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

    def _update_walls(self) -> None:

        if hasattr(self, "walls"):

            for icons in self.walls.values():
                icons[0]._unload_image()
                icons[1]._unload_image()

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
                self.cell_x + self.cell_space - wall_pad - wall_w,
                wall_h, wall_w
            ),
            "E": (
                self.cell_x + wall_pad, self.cell_y + wall_pad + wall_w,
                wall_w, wall_h
            ),
            "W": (
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
                    (self.map.change_wall, (wall, *self.cur_cell)),
                    (self.wall_pos[wall][2], self.wall_pos[wall][3]),
                    True,
                    False
                ),
                ClickableIcon(
                    self.wall_pos[wall][0],
                    self.wall_pos[wall][1],
                    WALLS[wall] + WALL_NOTHERE,
                    (self.map.change_wall, (wall, *self.cur_cell)),
                    (self.wall_pos[wall][2], self.wall_pos[wall][3]),
                    True,
                    False
                )
            )

    def display_cell(self) -> None:

        if not self.show_cell:
            return

        pr.draw_rectangle(self.cell_x, self.cell_y, self.cell_space, self.cell_space, pr.DARKGRAY)
        pr.draw_rectangle_lines(self.cell_x, self.cell_y, self.cell_space, self.cell_space, pr.LIGHTGRAY)

        for wall, state in self.map.get_walls(*self.cur_cell).items():

            wall_show: int = 1

            if True in state:
                wall_show = 0

            self.walls[wall][wall_show].display_widget()

    def set_cur_cell(self, x: int, y: int) -> None:

        self.show_cell = True
        self.cur_cell: tuple[int, int] = (x, y)
        self._update_walls()

    def handle_input(self, x: int, y: int) -> None:

        if self.show_cell and not self.is_in_cell(x, y):
            self.show_cell = False
            self._update(True)

        elif not self.show_cell and self.is_in_map(x, y):
            self.set_cur_cell(x, y)

        return

    def _update(self, forced: bool = False) -> None:

        if pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT):
            self.handle_input(pr.get_mouse_x(), pr.get_mouse_y())

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_randomize_button()
        self.map_renderer.update_grid(
            self.map.map.cells,
            (self.map_w, self.map_h),
            (self.map_x, self.map_y),
            self.cell_size
        )

    def display_view(self) -> None:

        self._update()

        self.map_renderer.display_grid()

        super().display_view()

        if self.show_cell:
            self.display_cell()


class Custom_view(View):

    def __init__(self, app) -> None:

        self.app = app
        self.map: Map_custom = Map_custom(self.app.map_folder)
        self.steps: list[Custom_step] = [
            Step_one(self, self.map),
            Step_two(self, self.map)
        ]

        self.cur_step: int = 0

    def create_map(self) -> None:

        ...

    def change_step(self, new: int = 1) -> None:

        if self.cur_step + new == len(self.steps):
            self.create_map()
            return

        if self.cur_step + new == -1:
            self.app.return_to_prev_view()
            self.app.remove_last_view()
            return

        if not (0 <= self.cur_step + new < len(self.steps)):
            return

        self.cur_step += new

    def display_view(self) -> None:

        self.steps[self.cur_step].display_view()
