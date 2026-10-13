import pyray as pr
from typing import Any
from .View import View
from .Pause_menu import Pause_menu
from .widget import Icon, Text, Widget
from ..game.Game import Game
from ..game.map.Cell import Cell
from .Map_renderer import Map_renderer


LIFE_ICON_PATH: str = "src/view/assets/icons/pac-man_life_icon.png"

MIDDLE_LINE_THICKNESS: int = 10

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


class Game_view(View):

    def __init__(self, app: Any, game: Game) -> None:

        self.game: Game = game
        self.modal_view: Pause_menu = Pause_menu(app, game, self)
        self.show_as_modal: bool = False

        self.game.map.append(self.game.generate_map(10, 10))
        self.game.start_position()

        super().__init__(app)

    def _update_score_panel(self) -> None:

        self.left_w: int = self.w // 4

        self.labels: list[str] = [
            "Highscore : " + str(0),
            "Score : " + str(self.game.player.score),
            "Timer : " + str(self.game.timer)
        ]
        max_label: str = max(self.labels, key=lambda label: len(label))

        label_font_sz: int = Text._resize_font(max_label, self.h // 8, self.left_w - self.left_w // 3)

        self.widgets += [Text(
            label,
            -2,
            self.h // 16 + (label_font_sz + self.h // 10) * i,
            label_font_sz,
            self.left_w - self.left_w // 3,
            pr.RAYWHITE,
            self.left_w
        ) for i, label in enumerate(self.labels)]

        life_label: Text = Text(
            "Lives : ",
            self.left_w // 10,
            self.h - self.h // 5,
            label_font_sz
        )
        self.widgets.append(life_label)
        life_icon_sz: int = (
            self.left_w - (life_label.x + life_label.width)
        ) // 3 - 10

        self.widgets += [Icon(
            10 + life_label.x + life_label.width + life_icon_sz * life,
            life_label.y - 5,
            LIFE_ICON_PATH,
            (life_icon_sz, life_icon_sz),
            True
        ) for life in range(self.game.player.nb_lives)]

    @property
    def map_startx(self) -> int:

        return (
            self.left_w + MIDDLE_LINE_THICKNESS
            + (self.map_panel_width - self.map_width) // 2
        )

    @property
    def map_starty(self) -> int:

        return (self.h - self.map_height) // 2

    def catch_player_input(self) -> None:

        if pr.is_key_pressed(pr.KEY_UP) or pr.is_key_pressed(pr.KEY_W):
            self.game.player.set_next_direction("N")
        elif pr.is_key_pressed(pr.KEY_DOWN) or pr.is_key_pressed(pr.KEY_S):
            self.game.player.set_next_direction("S")
        elif pr.is_key_pressed(pr.KEY_LEFT) or pr.is_key_pressed(pr.KEY_A):
            self.game.player.set_next_direction("W")
        elif pr.is_key_pressed(pr.KEY_RIGHT) or pr.is_key_pressed(pr.KEY_D):
            self.game.player.set_next_direction("E")
        cur_x = int(self.game.player.pos_x)
        cur_y = int(self.game.player.pos_y)
        self.game.player.test_update(self.game.map[self.game.map_index].cells[cur_y][cur_x])

    def _update_map_panel(self) -> None:

        self.grid: list[list[Cell]] = self.game.map[self.game.map_index].cells
        self.map_panel_width: int = self.w - self.left_w - MIDDLE_LINE_THICKNESS - 10
        self.map_width: int = min(
            self.map_panel_width - self.map_panel_width // 10,
            self.h - self.h // 10
        )
        self.map_height: int = self.map_width

        nb_cells_row: int = (self.map_width - 6) // len(self.grid[0])
        nb_cells_col: int = (self.map_height - 6) // len(self.grid)

        if nb_cells_row > nb_cells_col:
            self.cell_size: int = nb_cells_row
            self.map_height = self.cell_size * len(self.grid) + 6
        else:
            self.cell_size = nb_cells_col
            self.map_width = self.cell_size * len(self.grid[0]) + 6

        self.map_renderer: Map_renderer = Map_renderer(
            self.game,
            self.grid,
            (self.map_startx + 3, self.map_starty + 3),
            self.cell_size,
            [self.game.player] + list(self.game.ghosts.values())
        )
        self.map_outline: tuple[int, int, int, int] = (
            self.map_startx,
            self.map_starty,
            self.map_width,
            self.map_height
        )

    def pause_or_resume(self) -> None:

        self.show_as_modal = not self.show_as_modal

        if self.show_as_modal:
            self.game.pause(1)
            self.modal_view.reset_input()
        else:
            self.game.resume()

    def _update(self, forced: bool = False) -> None:

        if pr.get_key_pressed() in DIR_KEYS:
            self.catch_player_input()

        if pr.is_key_pressed(pr.KEY_ESCAPE):
            self.pause_or_resume()

        if not pr.is_window_resized() and not forced:
            return

        self.modal_view._update(True)

        self.widgets: list[Widget] = []
        self._update_score_panel()
        self._update_map_panel()

    def display_view(self) -> None:

        self._update()

        if self.show_as_modal:
            self.modal_view.display_view()
            return

        pr.draw_line_ex(
            (self.left_w, 0),
            (self.left_w, self.h),
            MIDDLE_LINE_THICKNESS,
            pr.RAYWHITE
        )

        pr.draw_rectangle_lines_ex(
            self.map_outline,
            3,
            pr.DARKBLUE
        )

        self.map_renderer.draw_grid()

        for widget in self.widgets:
            widget.display_widget()
