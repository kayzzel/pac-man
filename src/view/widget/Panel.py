import pyray as pr
from typing import Callable
from .Widget import Widget
from .Button import Button


PANEL_BASE_COLOR: pr.Color = pr.RAYWHITE


class Panel(Widget):

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        buttons: dict[str, Callable],
        button_size: int = 10,
        padding: int = 10,
        color: pr.Color = PANEL_BASE_COLOR
    ) -> None:

        super().__init__(x, y, width, height)
        self.color: pr.Color = color
        self.init_buttons(buttons, button_size, padding)

    def calculate_button_spacing(
        self,
        padding: int,
        button_size: int,
        labels: list[str]
    ) -> None:

        self.int_pad: int = padding

        self.font_size: int = button_size

        max_label: str = max(labels, key=lambda label: len(label))
        while (
            pr.measure_text(max_label, self.font_size) >= self.w
        ) and (
            self.font_size > 5
        ):
            self.font_size -= 1

        total_height: int = (
            self.int_pad * (len(labels) - 1)
            + self.font_size * len(labels)
        )
        while total_height > self.h and self.int_pad > 0:
            self.int_pad -= 1
            total_height = (
                self.int_pad * (len(labels) - 1)
                + self.font_size * len(labels)
            )

        self.ext_pad: int = 0
        while total_height + self.ext_pad * 2 < self.h:
            self.ext_pad += 1

    def center_button_x(self, label: str) -> int:

        return self.posx + (
            self.w - pr.measure_text(label, self.font_size)
        ) // 2

    def init_buttons(
        self,
        button_actions: dict[str, Callable],
        button_size: int,
        padding: int
    ) -> None:

        self.calculate_button_spacing(
            padding,
            button_size,
            button_actions.keys()
        )
        start_y: int = self.posy + self.ext_pad // 2
        self.buttons: dict[str, Button] = {
            label: Button(
                self.center_button_x(label),
                start_y + self.int_pad * i + self.font_size * (i + 1),
                label,
                action,
                self.font_size
            )
            for i, (label, action) in enumerate(button_actions.items())
        }

    def display_widget(self) -> None:

        pr.draw_rectangle_rounded_lines(
            (self.posx, self.posy, self.w, self.h),
            0.1,
            4,
            self.color
        )

        for button in self.buttons.values():

            button.display_widget()
