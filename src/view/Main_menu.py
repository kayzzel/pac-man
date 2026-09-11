import pyray as pr
from typing import Callable
from .View import View
from .widget.Panel import Panel
from .widget.Icon import Icon


class Main_menu(View):

    def __init__(self, background_path: str) -> None:

        self.background: pr.Texture = pr.load_texture_from_image(
            pr.load_image(background_path)
        )
        self.menu_icon: Icon = Icon(
            -2,
            -5,
            "src/view/assets/icons/pac-man_title.png",
            (pr.get_screen_width() - 10, pr.get_screen_height() // 4)
        )
        self.init_panel()

    def init_panel(self) -> None:

        icon_bottom: int = self.menu_icon.get_lower_bounds[1]

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

        pr.draw_texture(self.background, 0, 0, pr.WHITE)
        self.menu_icon.display_widget()
        self.panel.display_widget()
