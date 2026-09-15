import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from typing import Any
from .View import View
from .widget import Icon
from ..game.Game import Game


LIFE_ICON_PATH: str = "src/view/assets/icons/pac-man_life_icon.png"

MIDDLE_LINE_THICKNESS: int = 10


class Game_view(View):

    def __init__(self, app: Any, game: Game) -> None:

        super().__init__(app)

        self.game: Game = game

    def _update_left_panel(self) -> None:

        self.left_label_width: int = self.w // 4
        self.labels: list[str] = [
            "Highscore: " + str(0),
            "Score: " + str(self.game.player.score),
            "Timer: " + str(self.game.timer)
        ]
        max_label: str = max(self.labels, key=lambda label: len(label))

        self.label_font_sz: int = self.h // 10

        while pr.measure_text(max_label, self.label_font_sz) >= self.left_label_width:
            self.label_font_sz -= 1

        label_x: int = (self.left_label_width - pr.measure_text(max_label, self.label_font_sz)) // 2
        label_starty: int = self.h // 16
        label_spacing: int = self.h // 10

        self.labels_data: dict[str, tuple[int, int]] = {
            self.labels[label]: (
                label_x,
                label_starty + (self.label_font_sz + label_spacing) * label
            ) for label in range(len(self.labels))
        }

        life_label_x: int = self.left_label_width // 10
        self.labels_data["Lives: "] = (
            life_label_x,
            self.h - self.h // 7
        )
        life_label_w: int = pr.measure_text("Lives: ", self.label_font_sz)
        life_icon_sz: int = (
            self.left_label_width - life_label_w - life_label_x
        ) // 3

        self.life_icons: list[Icon] = [Icon(
            life_label_x + life_label_x + life_icon_sz * life,
            self.h - self.h // 7,
            LIFE_ICON_PATH,
            (life_icon_sz, life_icon_sz)
        ) for life in range(self.game.player.nb_lives)]

    def display_view(self) -> None:

        self._update_left_panel()

        pr.draw_line_ex(
            (self.left_label_width, 0),
            (self.left_label_width, self.h),
            MIDDLE_LINE_THICKNESS,
            pr.RAYWHITE
        )

        for label, coor in self.labels_data.items():

            pr.draw_text(label, *coor, pr.RAYWHITE)

        for icon in self.life_icons:

            icon.display_widget()
