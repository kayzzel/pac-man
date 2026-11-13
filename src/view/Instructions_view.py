import pyray as pr
from pyray import KeyboardKey as kek
from pyray import MouseButton as mb
from typing import Callable, Any
from .View import View
from .widget import Text, ButtonPanel


TEXTS: dict[str, list[str]] = {
    "CONTROLS": [
        "WASD ........ move Pac-Man",
        "ESC ......... pause / resume the game",
        " ",
        "A move is applied when Pac-Man reaches the center of the next cell:",
        "presses are queued, so you can steer slightly in advance."
    ],
    "GAME RULES": [
        "- Eat every pacgum of a level to complete it,",
        "and every level (10 by default) to win the game.",
        " ",
        "- Touching a ghost costs one life; at zero lives the game is over.",
        "Each level also has a time limit (90 seconds by default):",
        "when it runs out, the game is lost, regardless of remaining lives.",
        " ",
        "- Eating a super-pacgum (the big dots in the corners)",
        "makes the ghosts edible for a short time;",
        "they blink when it is about to end.",
        "Eating a ghost sends it back to its spawn and awards points.",
        " ",
        "- Score and remaining lives are kept between levels.",
        " ",
        "- At the end of a game (win or lose),",
        "your score can be saved with your name,"
        "and the best scores are readable from the main menu."
    ],
    "POINTS": [
        "Pacgum ............. 10 points (config: point_per_pacgum)",
        "Super-pacgum ....... 50 points (config: point_per_super_pacgum)",
        "Collectibles ....... 100 points",
        "Edible ghost ....... 200 points (config: point_per_ghost)"
    ],
    "OPTIONS (CHEAT)": [
        "Available to facilitate the review / to play around:",
        " ",
        "- Invincible: ghosts cannot kill you.",
        " ",
        "- Clipping: move through walls (never outside the maze).",
        " ",
        "- Add or remove lives (never below 1).",
        " ",
        "- Add or remove points (never below 0)."
    ],
    "CONFIGURATION": [
        "The game takes exactly one argument, a configuration file:",
        "       python pac-man.py config.json",
        " ",
        "All keys are optional, invalid values fall back to defaults,",
        "and unknown keys are ignored:",
        " ",
        "highscore_filename ...... file of the mandatory game's scores",
        "                          (default 'highscore.json')",
        "nb_level ................. number of levels, minimum 10",
        "                           (default 10)",
        "levels_dimensions ........ [width, height] of the levels, 10 to 50",
        "                           (default [15, 15])",
        "lives ..................... starting lives (default 3)",
        "point_per_pacgum .......... pacgum value (default 10)",
        "point_per_super_pacgum .... super-pacgum value (default 50)",
        "point_per_ghost ........... eaten ghost value (default 200)",
        "seed ...................... seed of the first level's maze",
        "                            (default 42)",
        "level_max_time ............ seconds per level (default 90)"
    ]
}


class Instructions_view(View):

    def __init__(self, app) -> None:

        self.show_instruction_panel: bool = False
        super().__init__(app)

    def show_instruction(self, category: str) -> None:

        if category not in self.all_instr.keys():
            return

        self.show_instruction_panel = True
        self.cur_instr: tuple[
            list[str],
            tuple[int, int]
        ] = self.all_instr[category]

    @property
    def font_sz(self) -> int:

        return self.h // 40

    @property
    def outline(self) -> tuple[int, int, int, int]:

        if not self.show_instruction_panel:
            return (0, 0, 0, 0)

        t_w, t_h = self.cur_instr[1]
        return (
            (self.w - t_w) // 2,
            (self.h - t_h) // 2,
            t_w,
            t_h
        )

    @property
    def is_in_instruction(self) -> bool:

        x, y, w, h = self.outline
        return ((
            x <= pr.get_mouse_x() <= x + w
            and y <= pr.get_mouse_y() <= y + h
        ))

    def _update_instructions(self) -> None:

        self.all_instr: dict[str, tuple[list[Text], tuple[int, int]]] = {}

        for category, text in TEXTS.items():

            font_sz: int = self.font_sz
            t_h: int = font_sz * (len(text) * 2 + 3)
            while t_h >= self.h:
                font_sz -= 1
                t_h = font_sz * (len(text) * 2 + 3)

            max_label: str = max(text, key=lambda t: len(t))
            font_sz = Text._resize_font(
                max_label,
                font_sz,
                self.w - self.w // 10
            )
            t_h = font_sz * (len(text) * 2 + 3)
            t_w: int = Text.measure_text(max_label, font_sz) + self.w // 20
            starty: int = (self.h - t_h) // 2 + font_sz

            texts: list[Text] = [
                Text(
                    txt,
                    -2,
                    starty + font_sz * (i + 1) + font_sz * i,
                    font_sz,
                    t_w
                ) for i, txt in enumerate(text)
            ]
            self.all_instr[category] = (texts, (t_w, t_h))

    def _update_menu_panel(self) -> None:

        self.title: Text = Text(
            "PAC-MAN - INSTRUCTIONS",
            -2,
            self.h // 9,
            self.h // 10
        )

        buttons: dict[str, tuple[Callable, Any]] = {
            label: (self.show_instruction, label)
            for label in TEXTS.keys()
        }

        self.menu_panel: ButtonPanel = ButtonPanel(
            -2,
            self.h // 3,
            self.w // 3,
            self.h // 2,
            buttons,
            (0, 2, 0.1)
        )
        self.widgets += [self.title, self.menu_panel]

    def _update_back_button(self) -> None:

        back_label: str = "back <-|"
        back_width: int = self.w // 8
        back_height: int = self.h // 15

        self.back_button: ButtonPanel = ButtonPanel(
            self.w - back_width - self.w // 25,
            self.h - back_height - self.h // 40,
            back_width,
            back_height,
            {back_label: (self.app.return_to_prev_view, None)}
        )
        self.widgets.append(self.back_button)

    def _update(self, forced: bool = False) -> None:

        if pr.is_key_pressed(kek.KEY_ESCAPE) and self.show_instruction_panel:
            self.show_instruction = False

        if (
            pr.is_mouse_button_pressed(mb.MOUSE_BUTTON_LEFT)
            and self.show_instruction_panel and not self.is_in_instruction
        ):
            self.show_instruction_panel = False

        if not pr.is_window_resized() and not forced:
            return

        super()._update(True)
        self._update_menu_panel()
        self._update_back_button()
        self._update_instructions()

    def display_view(self) -> None:

        super().display_view()

        if self.show_instruction_panel:

            pr.draw_rectangle_rounded_lines_ex(
                self.outline,
                0.1,
                4,
                2,
                pr.LIGHTGRAY
            )
            pr.draw_rectangle_rounded(
                self.outline,
                0.1,
                4,
                pr.DARKGRAY
            )
            for instr in self.cur_instr[0]:
                instr.display_widget()
