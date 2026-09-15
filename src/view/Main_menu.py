import pyray as pr
from typing import Callable, Any
from .View import View
from .widget.Panel import RectPanel
from .widget.Icon import Icon, AnimIcon


BACKGROUND_IMAGE_PATH: str = "src/view/assets/gifs/pac-man_bg_gif.gif"
TITLE_IMAGE_PATH: str = "src/view/assets/icons/pac-man_title.png"

BORDER_THICKNESS: int = 7
BORDER_PADDING: int = 3


class Main_menu(View):

    def _update_icons(self) -> None:

        self.background: AnimIcon = AnimIcon(
            -2,
            -2,
            BACKGROUND_IMAGE_PATH,
            (self.w, self.h)
        )
        self.menu_icon: Icon = Icon(
            -2,
            min(self.h // 5, 50),
            TITLE_IMAGE_PATH,
            (
                self.w - int(self.w * 0.2),
                self.h // 4
            )
        )
        self.outline: tuple[int, int, int, int] = (
            BORDER_PADDING,
            BORDER_PADDING,
            self.w - BORDER_PADDING * 2,
            self.h - BORDER_PADDING * 2
        )

    def _update_panel(self) -> None:

        icon_bottom: int = self.menu_icon.get_lower_bounds[1] + 100

        panel_height: int = self.h - icon_bottom
        panel_width: int = self.w // 3

        panel_y: int = icon_bottom + panel_height // 6
        panel_x: int = (self.w - panel_width) // 2

        panel_height -= panel_height // 3

        button_actions: dict[str, tuple[Callable, Any]] = {
            "start game": (self.app.change_view, "map_choice_menu"),
            "view highscores": (lambda: print(
                "Action for button 'view highscores' not yet coded\n"
            ), None),
            "instructions": (lambda: print(
                "Action for button 'instructions' not yet coded\n"
            ), None),
            "exit": (pr.close_window, None),
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

    # def update(self) -> None:

    #     for button in self.panel.buttons.values():

    #         if button.is_pressed:
    #             button.call_action()

    def display_view(self) -> None:

        self._update_icons()
        self._update_panel()

        if pr.is_key_pressed(pr.KEY_ESCAPE):
            self.app.change_view("pause_menu")
            return

        pr.draw_rectangle_lines_ex(
            self.outline,
            BORDER_THICKNESS,
            pr.DARKBLUE
        )
        self.background.display_widget()
        self.menu_icon.display_widget()
        self.panel.display_widget()
