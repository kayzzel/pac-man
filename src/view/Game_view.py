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
        self.map_size: int = self.h - self.h // 10
        self.map_startx: int = self.left_panel_width + MIDDLE_LINE_THICKNESS + (self.map_panel_width - self.map_size) // 2
        self.map_starty: int = self.h // 20
        self.map_outline: tuple[int, int, int, int] = (
            self.map_startx,
            self.map_starty,
            self.map_size,
            self.map_size
        )
        pac_man_size: int = self.map_size // 16

        self.pacman_sprite: AnimIcon = AnimIcon(
            self.map_startx + (self.map_size - pac_man_size) // 2,
            -2,
            self.texture_pack.get_texture(
                "pac-man_" + DIRECTIONS[self.game.player.direction]
            ),
            (pac_man_size, pac_man_size),
            True
        )
        self.calculate_cell_size()

    def calculate_cell_size(self) -> None:

        ver_walls: int = 0
        hor_walls: int = 0
        nb_cells: int = len(self.game.map.cells)

        for cell in self.game.map.cells:

            if cell.walls["north"]:
                ver_walls += 1
            if cell.walls["south"]:
                ver_walls += 1
            if cell.walls["west"]:
                hor_walls += 1
            if cell.walls["east"]:
                hor_walls += 1

        map_width: int = nb_cells + hor_walls
        map_height: int = nb_cells + ver_walls

        self.cell_size: int = min(self.map_size // map_width, self.map_size // map_height)

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

        for label, coor in self.labels_data.items():

            pr.draw_text(label, *coor, self.label_font_sz, pr.RAYWHITE)

        for icon in self.life_icons:

            icon.display_widget()

        if pr.is_key_pressed(pr.KEY_ESCAPE):
            self.show_as_modal = not self.show_as_modal

        if self.show_as_modal:
            self.modal_view.display_view()
