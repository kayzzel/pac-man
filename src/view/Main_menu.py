import pyray as pr
from typing import Callable
from .View import View
from .widget.Button import Button
from .widget.Icon import Icon


class Main_menu(View):

    def __init__(self) -> None:

        self.menu_icon: Icon = Icon(
            -2,
            -5,
            "src/view/assets/icons/pac-man_title.png",
            (pr.get_screen_width() - 10, pr.get_screen_height() // 4)
        )
        self.init_buttons()

    def init_buttons(self) -> None:

        icon_bottom: int = self.menu_icon.get_lower_bounds[1]

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

        self.buttons: dict[str, Button] = {
            label: Button(
                -2,
                icon_bottom + ((i + 1) * 20) + (i * 20),
                label,
                action
            )
            for i, (label, action) in enumerate(button_actions.items())
        }

    def update(self) -> None:

        for button in self.buttons.values():

            if button.is_pressed:
                button.action()

    def display_view(self) -> None:

        self.menu_icon.display_widget()

        for button in self.buttons.values():
            button.display_widget()
