import pyray as pr
from typing import Callable, Any
from .View import View
from .widget.Panel import Panel
from .widget.Icon import Icon, AnimIcon


BACKGROUND_IMAGE_PATH: str = "src/view/assets/gifs/pac-man_bg.gif"
TITLE_IMAGE_PATH: str = "src/view/assets/icons/pac-man_title.png"

BORDER_THICKNESS: int = 7
BORDER_PADDING: int = 3


class Main_menu(View):

    def _update_icons(self) -> None:

        self.menu_icon: Icon = Icon(
            -2,
            min(self.h // 15, 50),
            TITLE_IMAGE_PATH,
            (
                self.w - int(self.w * 0.2),
                self.h // 4
            ),
            True
        )
        self.background: AnimIcon = AnimIcon(
            -2,
            self.menu_icon.lower_bounds[1] + self.h // 20,
            BACKGROUND_IMAGE_PATH,
            (self.w - self.w // 3, self.h // 6),
            True,
            5
        )
        self.outline: tuple[int, int, int, int] = (
            BORDER_PADDING,
            BORDER_PADDING,
            self.w - BORDER_PADDING * 2,
            self.h - BORDER_PADDING * 2
        )

    def _update_panel(self) -> None:

        icon_bottom: int = self.background.lower_bounds[1]

        height_remaining: int = self.h - BORDER_PADDING * 2 - icon_bottom
        panel_height: int = height_remaining - height_remaining // 4
        panel_width: int = self.w // 3

        panel_y: int = icon_bottom + (height_remaining - panel_height) // 2
        panel_x: int = (self.w - panel_width) // 2

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
        button_font_sz: int = self.h // 20

        self.panel: Panel = Panel(
            panel_x,
            panel_y,
            panel_width,
            panel_height,
            button_actions,
            button_font_sz,
            (10, 2, 0.1),
            (pr.RED, pr.BLANK),
            (pr.GRAY, pr.GOLD)
        )

    def _update(self) -> None:

        if not pr.is_window_resized() and self.is_init:
            return

        self._update_icons()
        self._update_panel()
        self.is_init = True

    def display_view(self) -> None:

        self._update()

        pr.draw_rectangle_lines_ex(
            self.outline,
            BORDER_THICKNESS,
            pr.DARKBLUE
        )
        self.background.display_widget()
        self.menu_icon.display_widget()
        self.panel.display_widget()
