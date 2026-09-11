import pyray as pr
from typing import Callable
from .View import View
from .widget.Panel import Panel
from .widget.Icon import Icon


class Main_menu(View):

    def __init__(self) -> None:

        self.background: Icon = Icon(
            -2,
            -2,
            "src/view/assets/gifs/pac-man_bg_gif.gif",
            True,
            (pr.get_screen_width(), pr.get_screen_height())
        )
        self.menu_icon: Icon = Icon(
            -2,
            min(pr.get_screen_height() // 5, 50),
            "src/view/assets/icons/pac-man_title.jpeg",
            False,
            (pr.get_screen_width() - int(pr.get_screen_width() * 0.2), pr.get_screen_height() // 4)
        )
        self.init_panel()

    def init_panel(self) -> None:

        icon_bottom: int = self.menu_icon.get_lower_bounds[1] + 100

        panel_height: int = pr.get_screen_height() - icon_bottom
        panel_width: int = pr.get_screen_width() // 3

        panel_y: int = icon_bottom + panel_height // 6
        panel_x: int = (pr.get_screen_width() - panel_width) // 2

        panel_height -= panel_height // 3

        button_actions: dict[str, Callable] = {
            "start game": (lambda: print(
                "Action for button 'start game' not yet coded\n"
            )),
            "view highscores": (lambda: print(
                "Action for button 'view highscores' not yet coded\n"
            )),
            "instructions": (lambda: print(
                "Action for button 'instructions' not yet coded\n"
            )),
            "exit": pr.close_window,
        }

        self.panel: Panel = Panel(
            panel_x,
            panel_y,
            panel_width,
            panel_height,
            button_actions,
            20,
            10
        )

    def update(self) -> None:

        for button in self.panel.buttons.values():

            if button.is_pressed:
                button.action()

    def display_view(self) -> None:

        self.background.display_widget()
        self.menu_icon.display_widget()
        self.panel.display_widget()
