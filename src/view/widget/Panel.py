import pyray as pr
from typing import Callable, Any
from .Widget import Widget
from .Button import Button, BUTTON_BASE_COLOR, BUTTON_HOVER_COLOR


PANEL_OUTLINE_COLOR: pr.Color = pr.DARKGRAY
PANEL_FILL_COLOR: pr.Color = pr.BLANK


class Panel(Widget):

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        buttons: dict[str, tuple[Callable, Any]],
        shape_params: tuple[int, int, float] = (10, 2, 0.1),
        center: int = -2,
        panel_colors: tuple[pr.Color, pr.Color] = (
            PANEL_OUTLINE_COLOR,
            PANEL_FILL_COLOR
        ),
        button_colors: tuple[pr.Color, pr.Color] = (
            BUTTON_BASE_COLOR,
            BUTTON_HOVER_COLOR
        ),
        hover_color: pr.Color = pr.BLANK
    ) -> None:

        super().__init__(x, y, width, height)

        self.padding: int
        self.thickness: int
        self.roundness: float
        self.padding, self.thickness, self.roundness = shape_params
        self.center: int = center
        self.outline_color: pr.Color
        self.fill_color: pr.Color
        self.outline_color, self.fill_color = panel_colors
        self.button_colors: tuple[pr.Color, pr.Color] = button_colors
        self.hover_color: pr.Color = hover_color

        self.init_buttons(buttons)

    def calculate_button_spacing(self, labels: list[str]) -> None:

        if self.padding == 0:
            self.padding = (self.h // (len(labels) * 2 + 1)) // 2

        height_remaining: int = self.h - self.padding * 2
        self.font_size: int = height_remaining // len(labels)
        space_for_labels = height_remaining - (len(labels) - 1) * (self.font_size // 2)

        self.font_size = space_for_labels // len(labels)

        max_label: str = max(labels, key=lambda label: len(label))
        while (
            pr.measure_text(max_label, self.font_size) >= self.w
        ) and (
            self.font_size > 5
        ):
            self.font_size -= 1

        self.int_pad: int = 0
        if len(labels) > 1:
            self.int_pad = (height_remaining - self.font_size * len(labels)) // (len(labels) - 1)

        total_height: int = self.font_size * len(labels) + self.int_pad * (len(labels) - 1)
        if self.h - total_height > self.padding * 2:
            self.padding = (self.h - total_height) // 2

    def center_button_x(self, label: str) -> int:

        return self.posx + (
            self.w - pr.measure_text(label, self.font_size)
        ) // 2

    def init_buttons(
        self,
        button_actions: dict[str, tuple[Callable, Any]]
    ) -> None:

        self.calculate_button_spacing(
            list(button_actions.keys())
        )
        start_y: int = self.posy + self.padding - self.font_size
        self.buttons: dict[str, Button] = {
            label: Button(
                (
                    self.center_button_x(label)
                    if self.center == -2
                    else self.posx + self.center
                ),
                start_y + self.int_pad * i + self.font_size * (i + 1),
                label,
                action,
                self.font_size,
                *self.button_colors
            )
            for i, (label, action) in enumerate(button_actions.items())
        }

        for nb, button in enumerate(self.buttons.values()):
            self.determine_button_area(button, nb)

    def determine_button_area(self, button: Button, nb: int) -> None:

        sx: int = self.posx
        sy: int = self.posy

        ex: int = self.posx + self.w
        ey: int = self.posy + self.padding + self.font_size + self.int_pad // 2

        for i in range(len(self.buttons.values())):

            if i == nb:
                break

            sy = ey
            ey += self.font_size + self.int_pad

        if nb == len(self.buttons.values()) - 1:
            ey -= self.int_pad // 2
            ey += self.padding

        button.area: tuple[int, int, int, int] = (sx, sy, ex - sx, ey - sy)

    def display_widget(self) -> None:

        if self.outline_color != pr.BLANK:
            pr.draw_rectangle_rounded_lines_ex(
                (
                    self.posx - self.thickness,
                    self.posy - self.thickness,
                    self.w + self.thickness * 2,
                    self.h + self.thickness * 2
                ),
                self.roundness,
                4,
                self.thickness,
                self.outline_color
            )
        pr.draw_rectangle_rounded(
            (self.posx, self.posy, self.w, self.h),
            self.roundness,
            4,
            self.fill_color
        )

        for i, button in enumerate(self.buttons.values()):

            if button.is_in_area:
                pr.draw_rectangle_rounded(
                    button.area,
                    self.roundness,
                    4,
                    self.hover_color
                )
            button.display_widget()
