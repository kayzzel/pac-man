import pyray as pr
from typing import Any
from .View import View
from .widget import Icon, AnimIcon
from ..game.Game import Game
from .Texture_pack import Texture_pack


LIFE_ICON_PATH: str = "src/view/assets/icons/pac-man_life_icon.png"

MIDDLE_LINE_THICKNESS: int = 10

DIRECTIONS: dict[str, str] = {
    "N": "up",
    "S": "down",
    "W": "left",
    "E": "right"
}

DIR_KEYS: list = [
    pr.KEY_UP,
    pr.KEY_DOWN,
    pr.KEY_RIGHT,
    pr.KEY_LEFT,
    pr.KEY_W,
    pr.KEY_S,
    pr.KEY_A,
    pr.KEY_D
]


class Wall:

    def __init__(self) -> None:

        self.north: bool = False
        self.south: bool = False
        self.west: bool = False
        self.east: bool = False


class Game_view(View):

    def __init__(self, app: Any, game: Game, modal_view: View) -> None:

        super().__init__(app)

        self.game: Game = game
        self.modal_view: View = modal_view
        self.show_as_modal: bool = False

        self.texture_pack: Texture_pack = Texture_pack()

    def _update_score_panel(self) -> None:

        self.left_panel_width: int = self.w // 4
        self.labels: list[str] = [
            "Highscore : " + str(0),
            "Score : " + str(self.game.player.score),
            "Timer : " + str(self.game.timer)
        ]
        max_label: str = max(self.labels, key=lambda label: len(label))

        self.label_font_sz: int = self.h // 10

        while (
            pr.measure_text(max_label, self.label_font_sz)
            >= self.left_panel_width - self.left_panel_width // 3
        ):
            self.label_font_sz -= 1

        label_x: int = (
            self.left_panel_width
            - pr.measure_text(max_label, self.label_font_sz)
        ) // 2
        label_starty: int = self.h // 16
        label_spacing: int = self.h // 10

        self.labels_data: dict[str, tuple[int, int]] = {
            self.labels[label]: (
                label_x,
                label_starty + (self.label_font_sz + label_spacing) * label
            ) for label in range(len(self.labels))
        }

        life_label_x: int = self.left_panel_width // 10
        self.labels_data["Lives : "] = (
            life_label_x,
            self.h - self.h // 5
        )
        life_label_w: int = pr.measure_text("Lives : ", self.label_font_sz)
        life_icon_sz: int = (
            self.left_panel_width - (life_label_x + life_label_w)
        ) // 3 - 10

        self.life_icons: list[Icon] = [Icon(
            10 + life_label_x + life_label_w + life_icon_sz * life,
            self.h - self.h // 5 - 5,
            LIFE_ICON_PATH,
            (life_icon_sz, life_icon_sz),
            True
        ) for life in range(self.game.player.nb_lives)]

    @property
    def map_startx(self) -> int:

        return (
            self.left_panel_width + MIDDLE_LINE_THICKNESS
            + (self.map_panel_width - self.map_width) // 2
        )

    @property
    def map_starty(self) -> int:

        return (self.h - self.map_height) // 2

    def _update_map_panel(self) -> None:

        if pr.is_key_pressed(pr.KEY_UP) or pr.is_key_pressed(pr.KEY_W):
            self.game.player.direction = "N"
        elif pr.is_key_pressed(pr.KEY_DOWN) or pr.is_key_pressed(pr.KEY_S):
            self.game.player.direction = "S"
        elif pr.is_key_pressed(pr.KEY_LEFT) or pr.is_key_pressed(pr.KEY_A):
            self.game.player.direction = "W"
        elif pr.is_key_pressed(pr.KEY_RIGHT) or pr.is_key_pressed(pr.KEY_D):
            self.game.player.direction = "E"

        self.map_panel_width: int = self.w - self.left_panel_width - 10
        self.map_width: int = min(
            self.map_panel_width - self.map_panel_width // 10,
            self.h - self.h // 10
        )
        self.map_height: int = self.map_width
        pac_man_size: int = self.map_width // 16

        self.pacman_sprite: AnimIcon = AnimIcon(
            self.map_startx + (self.map_width - pac_man_size) // 2,
            -2,
            self.texture_pack.get_texture(
                "pac-man_" + DIRECTIONS[self.game.player.direction]
            ),
            (pac_man_size, pac_man_size),
            True
        )
        self.grid: list[list] = self.game.map.cells
        self.insert_rows()
        self.insert_cols()

        nb_cells_row: int = self.map_width // len(self.grid[0])
        nb_cells_col: int = self.map_height // len(self.grid)

        if nb_cells_row > nb_cells_col:
            self.cell_size: int = nb_cells_row
            self.map_height = self.cell_size * len(self.grid)
        else:
            self.cell_size = nb_cells_col
            self.map_width = self.cell_size * len(self.grid[0])

        self.map_outline: tuple[int, int, int, int] = (
            self.map_startx,
            self.map_starty,
            self.map_width,
            self.map_height
        )

    def insert_rows(self) -> None:

        self.north_rows: list[tuple[list, int]] = []
        self.south_rows: list[tuple[list, int]] = []

        for r in range(len(self.grid)):

            row = self.grid[r]

            north_row: list = []
            south_row: list = []

            for cell in range(len(row)):

                if row[cell].walls["N"]:
                    if not north_row:
                        north_row = [
                            Wall()
                            for _ in range(len(row))
                        ]
                    north_row[cell].north = True

                if row[cell].walls["S"]:
                    if not south_row:
                        south_row = [
                            Wall()
                            for _ in range(len(row))
                        ]
                    south_row[cell].south = True

            if north_row:
                self.north_rows.append((north_row, r))
            if south_row:
                self.south_rows.append((south_row, r + 1 + (
                    1 if north_row else 0
                )))

        for n_row, index in self.north_rows:
            self.grid.insert(index, n_row)
        for s_row, index in self.south_rows:
            self.grid.insert(index, s_row)

    def insert_cols(self) -> None:

        self.west_cols: list[tuple[list, int]] = []
        self.east_cols: list[tuple[list, int]] = []

        for c in range(len(self.grid[0])):

            west_col: list = []
            east_col: list = []

            for r in range(len(self.grid)):

                if any(
                    isinstance(cell, Wall)
                    for cell in self.grid[r]
                ):
                    continue

                if self.grid[r][c].walls["W"]:
                    if not west_col:
                        west_col = [
                            Wall()
                            for _ in range(len(self.grid))
                        ]
                    west_col[r].west = True

                if self.grid[r][c].walls["E"]:
                    if not east_col:
                        east_col = [
                            Wall()
                            for _ in range(len(self.grid))
                        ]
                    east_col[r].east = True

            if west_col:
                self.west_cols.append((west_col, c))
            if east_col:
                self.east_cols.append((east_col, c + 1 + (
                    1 if west_col else 0
                )))

        for w_col, index in self.west_cols:
            for row_index in range(len(self.grid)):
                self.grid[row_index].insert(w_col[row_index], index)
        for e_col, index in self.east_cols:
            for row_index in range(len(self.grid)):
                self.grid[row_index].insert(e_col[row_index], index)

    def draw_wall(self) -> None:

        pr.draw_rectangle(
            self.cur_x,
            self.cur_y,
            self.cell_size,
            self.cell_size,
            pr.DARKBLUE
        )

    def draw_cell(self) -> None:

        ...

    def draw_grid(self) -> None:

        self.cur_y: int = self.map_starty

        for row in self.grid:

            self.cur_x: int = self.map_startx

            for square in row:

                if isinstance(square, Wall):
                    self.draw_wall()

                else:
                    self.draw_cell()

                self.cur_x += self.cell_size

            self.cur_y += self.cell_size

    def _update(self) -> None:

        if pr.get_key_pressed() in DIR_KEYS:
            self._update_map_panel()

        if not pr.is_window_resized() and self.is_init:
            return

        self._update_score_panel()
        self._update_map_panel()
        self.is_init = True

    def display_view(self) -> None:

        self._update()

        pr.draw_line_ex(
            (self.left_panel_width, 0),
            (self.left_panel_width, self.h),
            MIDDLE_LINE_THICKNESS,
            pr.RAYWHITE
        )

        pr.draw_rectangle_rounded_lines_ex(
            self.map_outline,
            0.1,
            4,
            3,
            pr.DARKBLUE
        )

        self.pacman_sprite.display_widget()

        self.draw_grid()

        for label, coor in self.labels_data.items():

            pr.draw_text(label, *coor, self.label_font_sz, pr.RAYWHITE)

        for icon in self.life_icons:

            icon.display_widget()

        if pr.is_key_pressed(pr.KEY_ESCAPE):
            self.show_as_modal = not self.show_as_modal

        if self.show_as_modal:
            self.modal_view.display_view()
