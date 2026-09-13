import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from typing import Callable, Any
from .View import View
from .widget.Panel import RectPanel
from .widget.Icon import Icon, AnimIcon


BACKGROUND_IMAGE_PATH: str = "src/view/assets/gifs/pac-man_bg_gif.gif"
TITLE_IMAGE_PATH: str = "src/view/assets/icons/pac-man_title.png"

BORDER_THICKNESS: int = 7
BORDER_PADDING: int = 3


class Main_menu(View):

    def __init__(self) -> None:

        self.background: AnimIcon = AnimIcon(
            -2,
            -2,
            BACKGROUND_IMAGE_PATH,
            (sw(), sh())
        )
        self.menu_icon: Icon = Icon(
            -2,
            min(sh() // 5, 50),
            "src/view/assets/icons/pac-man_title.png",
            (
                sw() - int(sw() * 0.2),
                sh() // 4
            )
        )
        self.outline: tuple[int, int, int, int] = (
            BORDER_PADDING,
            BORDER_PADDING,
            sw() - BORDER_PADDING * 2,
            sh() - BORDER_PADDING * 2
        )
        self.init_panel()

    def init_panel(self) -> None:

        icon_bottom: int = self.menu_icon.get_lower_bounds[1] + 100

        panel_height: int = sh() - icon_bottom
        panel_width: int = sw() // 3

        panel_y: int = icon_bottom + panel_height // 6
        panel_x: int = (sw() - panel_width) // 2

        panel_height -= panel_height // 3

        button_actions: dict[str, Callable] = {
            "start game": (lambda: "map_choice_menu"),
            "view highscores": (lambda: print(
                "Action for button 'view highscores' not yet coded\n"
            )),
            "instructions": (lambda: print(
                "Action for button 'instructions' not yet coded\n"
            )),
            "exit": pr.close_window,
        }

        self.panel: RectPanel = RectPanel(
            panel_x,
            panel_y,
            panel_width,
            panel_height,
            button_actions,
            20,
            10,
            (pr.RED, pr.BLANK),
            (pr.GRAY, pr.GOLD)
        )

    def update(self) -> Any:

        for button in self.panel.buttons.values():

            if button.is_pressed:
                return button.action()

    def display_view(self) -> None:

        pr.draw_rectangle_lines_ex(
            self.outline,
            BORDER_THICKNESS,
            pr.DARKBLUE
        )
        self.background.display_widget()
        self.menu_icon.display_widget()
        self.panel.display_widget()
