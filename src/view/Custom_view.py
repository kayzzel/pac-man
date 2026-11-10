import pyray as pr
# from pyray import get_screen_width as sw
# from pyray import get_screen_height as sh
from pyray import MouseButton as mb
from abc import ABC
from ..game.map.Map_custom import Map_custom
from ..game.map.Cell import Cell
from .View import View
from .Texture_pack import Texture_pack
from .Map_renderer import Custom_map_renderer
from .widget import Widget, Text, ButtonPanel, Input_box, ClickableIcon, Icon


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
        self.map_renderer: Custom_map_renderer = Custom_map_renderer()
        self.description_label: str = description
        self.show_next: bool = show_next
        self._update(True)

    def go_next(self) -> None:

        self.main_view.step_forward()

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
            {"next": (self.go_next, None)}
        )
        self.back: ButtonPanel = ButtonPanel(
            self.w - (button_w + button_padx) * 2,
            self.h - button_h - button_pady,
            button_w,
            button_h,
            {"back": (self.main_view.step_back, None)}
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

    @property
    def cell_space(self) -> int:

        return self.map_h // 2

    @property
    def cell_x(self) -> int:

        return (self.w - self.cell_space) // 2

    @property
    def cell_y(self) -> int:

        return self.map_y + (self.map_h - self.cell_space) // 2

    def is_in_cell(self, x: int, y: int) -> Cell | None:

        if not self.is_in_map(x, y):
            return None

        col: int = (x - self.map_x) // self.cell_size
        row: int = (y - self.map_y) // self.cell_size
        if 0 <= row < self.map.rows and 0 <= col < self.map.cols:
            return self.map.map.cells[row][col]
        return None

    def is_in_map(self, x: int, y: int) -> bool:

        if (
            self.map_x <= x <= self.map_x + self.map_w
        ) and (
            self.map_y <= y <= self.map_y + self.map_h
        ):
            return True

        return False

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
            "Choose map size (min 10x10, max 30x30)"
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

        self.show_next = (self.map.cols != 0 and self.map.rows != 0)

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
        self.is_init: bool = False
        super().__init__(
            2,
            main_view,
            cmap,
            "Place the walls (click on each cell)",
            True
        )
        self.is_init = True

    def go_next(self) -> None:

        self.map.walls_set = True
        super().go_next()

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

        if not self.show_cell:
            return

        self.map.change_wall(*self.cur_cell, wall)

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

    def is_in_bigcell(self, x: int, y: int) -> bool:

        return (
            self.cell_x <= x <= self.cell_x + self.cell_space
            and self.cell_y <= y <= self.cell_y + self.cell_space
        )

    def handle_input(self, x: int, y: int) -> None:

        if self.show_cell and not self.is_in_bigcell(x, y):
            self.show_cell = False
            self._update_grid()

        elif not self.show_cell and self.is_in_map(x, y):
            cell: Cell | None = self.is_in_cell(x, y)
            if cell:
                self.set_cur_cell(cell.pos_x, cell.pos_y)

        return

    def _update_grid(self) -> None:

        self.map_renderer.update_grid(
            self.map.map.cells,
            (self.map_w, self.map_h),
            (self.map_x, self.map_y),
            self.cell_size,
            True
        )

    def _update(self, forced: bool = False) -> None:

        if self.is_init and pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT):
            self.handle_input(pr.get_mouse_x(), pr.get_mouse_y())

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_randomize_button()
        self._update_grid()

    def display_view(self) -> None:

        self._update()

        self.map_renderer.display_grid()

        super().display_view()

        if self.show_cell:
            self.display_cell()


class Step_three(Custom_step):

    def __init__(self, main_view: View, cmap: Map_custom) -> None:

        self._init_names()
        self.sprites: list[str] = ["pacman_idle"] + self.consumable_names + self.collectible_names
        super().__init__(
            3,
            main_view,
            cmap,
            "Place the spawn point of PacMan and the Ghosts"
        )

    def _init_names(self) -> None:

        self.show_message: str = ""
        self.texture_pack: Texture_pack = Texture_pack(main_view.app.display_config.texture_pack)
        self.entity_names: list[str] = ["pacman", "blinky", "inky", "pinky", "clyde"]
        self.consumable_names: list[str] = ["cherry", "galaxian", "apple", "orange", "strawberry", "key", "bell", "melon"]
        self.collectible_names: list[str] = self.consumable_names + ["pacgum", "super_pacgum"]
        self.sprites_set: dict[str, Cell] = {}
        self.current_sprite: str = ""

    @property
    def map_x(self) -> int:
        return self.main_view.steps_completed[-1].map_x

    @property
    def map_y(self) -> int:
        return self.main_view.steps_completed[-1].map_y

    @property
    def map_w(self) -> int:
        return self.main_view.steps_completed[-1].map_w

    @property
    def map_h(self) -> int:
        return self.main_view.steps_completed[-1].map_h

    @property
    def cell_size(self) -> int:
        return self.main_view.steps_completed[-1].cell_size

    def calculate_cell_pos(self, x: int, y: int) -> tuple[int, int] | None:

        if x < 0 or x >= self.map.cols:
            return None

        if y < 0 or y >= self.map.rows:
            return None

        return (
            self.map_x + self.cell_size * x,
            self.map_y + self.cell_size * y
        )

    def activate_sprite(self, spr_name: str) -> None:

        self.current_sprite = spr_name

        if spr_name in self.sprites_set.keys():
            self.sprites_set.pop(spr_name)

    def set_sprite(self, x: int, y: int, spr_name: str) -> bool:

        if spr_name == "pacman_idle":
            return self.map.set_pacman_spawn(x, y)
        elif spr_name in self.consumable_names:
            return self.map.set_collectible(x, y, Consumable(spr_name, x, y, 100))
        elif spr_name == "super_pacgum":
            return self.map.set_collectible(x, y, Super_pacgum(x, y, 50))
        elif spr_name == "pacgum":
            return self.map.set_collectible(x, y, Pacgum(x, y, 10))
        return False

    def try_place_sprite(self) -> None:

        if not self.current_sprite:
            return

        if self.current_sprite not in self.textures:
            return

        if self.current_sprite in self.sprites_set:
            return

        cell: Cell | None = self.is_in_cell(
            pr.get_mouse_x(),
            pr.get_mouse_y()
        )
        if not cell:
            return

        if self.set_sprite(cell.pos_x, cell.pos_y, self.current_sprite):

            self.sprites_set[self.current_sprite] = cell
            self.current_sprite = ""

        else:

            self.show_message = f"Cannot place {self.current_sprite.capitalize()} here, try elsewhere"
            self.frame_counter = 0

    def texture_size(self, sprite_name: str) -> int:

        if any(sprite_name.startswith(en_name) for en_name in self.entity_names):
            return self.map_renderer.entity_size
        elif sprite_name in self.consumable_names:
            return self.map_renderer.consumable_size
        elif sprite_name in self.collectible_names:
            return self.map_renderer.collectible_size
        return 0

    def _update_textures(self) -> None:

        if hasattr(self, "textures"):
            for icon in self.textures.values():
                icon._unload_image()

        if hasattr(self, "side_textures"):
            for icon in self.side_textures.values():
                icon._unload_image()

        self.textures: dict[str, Icon] = {
            t_name: Icon(
                0,
                0,
                self.texture_pack.get_texture(t_name),
                (self.texture_size(t_name), self.texture_size(t_name)),
                True
            ) for t_name in self.sprites
        }
        self._update_sidetextures()

    def _update_sidetextures(self) -> None:

        side_text_sz: int = self.map_h // (len(self.collectible_names) // 2 + 1)
        t_pad: int = self.map_h // 50
        side_text_sz = min(side_text_sz - t_pad * 2, self.map_x * 3 // 4)
        t_x: int = (self.map_x - side_text_sz) // 3 * 2
        pacman_icon: ClickableIcon = ClickableIcon(
            (self.map_x - side_text_sz) // 2,
            self.map_y + t_pad,
            self.texture_pack.get_texture("pacman_idle"),
            (self.activate_sprite, "pacman_idle"),
            (side_text_sz, side_text_sz),
            True,
            False
        )
        fst_x: 
        self.side_textures: dict[str, ClickableIcon] = {
            "pacman_idle": pacman_icon
        }
        for {
            t_name: ClickableIcon(
                t_x,
                self.map_y + i * (side_text_sz + t_pad * 2) + t_pad,
                self.texture_pack.get_texture(t_name),
                (self.activate_sprite, t_name),
                (side_text_sz, side_text_sz),
                True,
                False
            ) for i, t_name in enumerate(self.sprites)
        }
        # print(f"### all side textures: {[f"{name}: {icon.x, icon.y}, " for name, icon in self.side_textures.items()]}")

    def display_textures(self) -> None:

        self.map_renderer.display_set_sprites([
            (self.textures[spr_name], cell)
            for spr_name, cell in self.sprites_set.items()
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

            self.map_renderer.display_cur_sprite(self.textures[self.current_sprite], cell)

    def display_message(self) -> None:

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

    def check_next(self) -> None:

        self.show_next = (self.map.pacman_spawn_set and self.map.map.collectible_count > 0)

    def _update(self, forced: bool = False) -> None:

        self.check_next()

        if pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT):
            self.try_place_sprite()

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self.map_renderer.update_grid(
            self.map.map.cells,
            (self.map_w, self.map_h),
            (self.map_x, self.map_y),
            self.cell_size
        )
        self._update_textures()

    def display_view(self) -> None:

        self._update()

        super().display_view()

        self.map_renderer.display_grid()
        self.display_textures()

        if self.show_message:
            self.display_message()


class Step_four(Step_three):

    def __init__(self, view: View, cmap: Map_custom) -> None:

        self._init_names()
        self.spawn_sprites: list[str] = [
            en_name + "_idle" for en_name in self.entity_names if en_name != "pacman"
        ]
        self.scatter_sprites: list[str] = [
            en_name + "_scatter" for en_name in self.entity_names if en_name != "pacman"
        ]
        self.sprites: list[str] = self.spawn_sprites + self.scatter_sprites
        super(Step_three, self).__init__(
            4,
            view,
            cmap,
            "Place the Ghosts spawn and scatter points (spawn first)"
        )

    def activate_sprite(self, spr_name: str) -> None:

        if spr_name in self.scatter_sprites and not self.map.ghost_spawn_set[spr_name.removesuffix("_scatter")]:
            self.show_message = (
                f"Spawn point for {spr_name.removesuffix('_scatter')}"
                " not placed, try again afterwards"
            )
            self.frame_counter = 0
            return

        self.current_sprite = spr_name

        if spr_name in self.sprites_set.keys():
            self.sprites_set.pop(spr_name)

    def set_sprite(self, x: int, y: int, spr_name: str) -> bool:

        if spr_name in self.spawn_sprites:
            return self.map.set_ghost_spawn(x, y, spr_name.removesuffix("_idle"))
        elif spr_name in self.scatter_sprites:
            return self.map.set_ghost_scatter(x, y, spr_name.removesuffix("_scatter"))
        return False

    def _update_sidetextures(self) -> None:

        side_text_sz: int = self.map_h // len(self.sprites)
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
        # print(f"### all side textures: {[f"{name}: {icon.x, icon.y}, " for name, icon in self.side_textures.items()]}")

    def check_next(self) -> None:

        self.show_next = (
            all(self.map.ghost_spawn_set.values())
            and all(self.map.ghost_scatter_set.values())
        )


class Custom_view(View):

    def __init__(self, app) -> None:

        self.app = app
        self.map: Map_custom = Map_custom(self.app.map_folder)
        self.steps: list = [
            Step_one,
            Step_two,
            Step_three
        ]
        self.steps_completed: list[Custom_step] = []

        self.cur_step_index: int = 0
        self.cur_step: Custom_step = self.steps[0](self, self.map)

    def create_map(self) -> None:

        ...

    def step_back(self) -> None:

        if self.cur_step_index == 0:
            self.app.return_to_prev_view()
            self.app.remove_last_view()
            return

        self.cur_step_index -= 1
        self.cur_step = self.steps_completed[-1]
        self.steps_completed.pop()

    def step_forward(self) -> None:

        if self.cur_step_index + 1 == len(self.steps):
            self.create_map()
            return

        self.cur_step_index += 1
        self.steps_completed.append(self.cur_step)
        self.cur_step = self.steps[self.cur_step_index](self, self.map)

    def display_view(self) -> None:

        self.cur_step.display_view()
