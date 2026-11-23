import pyray as pr

from typing import Callable, Any

from .Widget import Widget
from .Text import Text
from .Button import Button, BUTTON_BASE_COLOR, BUTTON_HOVER_COLOR


PANEL_OUTLINE_COLOR: pr.Color = pr.MAROON
PANEL_FILL_COLOR: pr.Color = pr.BLANK
TEXT_PANEL_COLOR: pr.Color = pr.DARKBLUE


class Panel(Widget):

    """
    Basic template for a panel, but only inheriting classes should be used
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        shape_params: tuple[int, int, float] = (10, 2, 0.1),
        center: int = -2,
        panel_colors: tuple[pr.Color, pr.Color] = (
            PANEL_OUTLINE_COLOR,
            PANEL_FILL_COLOR
        )
    ) -> None:

        """
        Initializes the main attributes for a panel.

        Parameters
        ----------
        x: int
            The x coordinate of the panel.
        y: int
            The y coordinate of the panel.
        width: int
            The width of the panel.
        height: int
            The height of the panel.
        shape_params: tuple[int, int, float] (default 10, 2, 0.1)
            Respectively the padding, line thickness and roundness of the panel
        center: int (default -2)
            The label centering, relative to the panel width.
        panel_colors: tuple[pr.Color, pr.Color]
            (default PANEL_OUTLINE_COLOR, PANEL_FILL_COLOR)
            Respectively the panel's outline color and inside color.
        """

        super().__init__(x, y, width, height)

        self.padding: int
        self.thickness: int
        self.roundness: float
        self.padding, self.thickness, self.roundness = shape_params

        self.center: int = center
        self.outline_color: pr.Color
        self.fill_color: pr.Color
        self.outline_color, self.fill_color = panel_colors

    def calculate_label_spacing(self, labels: list[str]) -> None:

        """
        Calculates both the font size for the labels
        and the space (padding) between each label.

        Parameters
        ----------
        labels: list[str]
            All the labels of the panel.
        """

        if self.padding == 0:
            self.padding = (self.h // (len(labels) * 2 + 1)) // 2

        height_remaining: int = self.h - self.padding * 2
        self.font_size: int = height_remaining // len(labels)
        space_for_labels = (
            height_remaining
            - (len(labels) - 1)
            * (self.font_size // 2)
        )

        max_label: str = max(labels, key=lambda label: len(label))
        self.font_size = Text._resize_font(
            max_label,
            space_for_labels // len(labels),
            self.w
        )

        self.int_pad: int = 0

        if len(labels) > 1:

            self.int_pad = (
                height_remaining
                - self.font_size
                * len(labels)
            ) // (len(labels) - 1)

        total_height: int = (
            self.font_size
            * len(labels)
            + self.int_pad
            * (len(labels) - 1)
        )

        if self.h - total_height > self.padding * 2:
            self.padding = (self.h - total_height) // 2

    def center_label_x(self, label: str) -> int:

        """
        Centers the x position of a certain label
        by measuring its width (using the Text class' method).

        Parameters
        ----------
        label: str
            The text for which to calculate the x.

        Returns
        -------
        int
            The calculated x start position of the label.
        """

        return self.posx + (
            self.w - Text.measure_text(label, self.font_size)
        ) // 2


class TextPanel(Panel):

    """
    Panel which displays basic labels, not clickable buttons
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        labels: list[str],
        shape_params: tuple[int, int, float] = (10, 2, 0.1),
        center: int = -2,
        panel_colors: tuple[pr.Color, pr.Color] = (
            PANEL_OUTLINE_COLOR,
            PANEL_FILL_COLOR
        ),
        label_color: pr.Color = TEXT_PANEL_COLOR
    ) -> None:

        """
        Initializes the main attributes for a text panel.

        Parameters
        ----------
        x: int
            The x coordinate of the panel.
        y: int
            The y coordinate of the panel.
        width: int
            The width of the panel.
        height: int
            The height of the panel.
        labels: list[str]
            All of the labels that should be displayed on the panel.
        shape_params: tuple[int, int, float] (default 10, 2, 0.1)
            Respectively the padding, line thickness and roundness of the panel
        center: int (default -2)
            The label centering, relative to the panel width.
        panel_colors: tuple[pr.Color, pr.Color]
            (default PANEL_OUTLINE_COLOR, PANEL_FILL_COLOR)
            Respectively the panel's outline color and inside color.
        label_color: pr.Color (default TEXT_COLOR)
            The color to use for the labels.
        """

        super().__init__(
            x, y, width, height, shape_params, center, panel_colors
        )

        self.text_color: pr.Color = label_color
        self.init_labels(labels)

    def init_labels(self, labels: list[str]) -> None:

        """
        Initializes all the labels using Text widgets
        and calculating font size and spacing using the parent method.

        Parameters
        ----------
        labels: list[str]
            All of the labels to initialize.
        """

        if not labels:
            return

        self.calculate_label_spacing(labels)

        start_y: int = self.posy + self.padding - self.font_size

        self.labels: dict[str, Text] = {
            label: Text(
                label,
                (
                    self.center_label_x(label)
                    if self.center == -2
                    else self.posx + self.center
                ),
                start_y + self.int_pad * i + self.font_size * (i + 1),
                self.font_size,
                self.w,
                self.text_color
            )
            for i, label in enumerate(labels)
        }

    def display_widget(self) -> None:

        """
        Displays all the text widgets on the panel.
        """

        if not hasattr(self, "labels"):
            return

        for label in self.labels.values():
            label.display_widget()


class ButtonPanel(Panel):

    """
    Panel which displays clickable labels.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        buttons: dict[str, tuple[Callable[..., Any], Any]],
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

        """
        Initializes the main attributes for a text panel.

        Parameters
        ----------
        x: int
            The x coordinate of the panel.
        y: int
            The y coordinate of the panel.
        width: int
            The width of the panel.
        height: int
            The height of the panel.
        buttons: dict[str, tuple[Callable, Any]]
            A dictionary containing the buttons,
            the keys being the buttons' labels,
            and the values being the function and args to associate with them.
        shape_params: tuple[int, int, float] (default 10, 2, 0.1)
            Respectively the padding, line thickness and roundness of the panel
        center: int (default -2)
            The label centering, relative to the panel width.
        panel_colors: tuple[pr.Color, pr.Color]
            (default PANEL_OUTLINE_COLOR, PANEL_FILL_COLOR)
            Respectively the panel's outline color and inside color.
        button_colors: tuple[pr.Color, pr.Color]
            (default BUTTON_BASE_COLOR, BUTTON_HOVER_COLOR)
            Respectively the color of the button label
            when normal and when the mouse hovers over it.
        hover_color: pr.Color (default BLANK)
            The color to use for the button background,
            usually BLANK for button transparency.
        """

        super().__init__(
            x, y, width, height, shape_params, center, panel_colors
        )

        self.button_colors: tuple[pr.Color, pr.Color] = button_colors
        self.hover_color: pr.Color = hover_color

        self.init_buttons(buttons)

    def init_buttons(
        self,
        button_actions: dict[str, tuple[Callable[..., Any], Any]]
    ) -> None:

        """
        Initializes all the buttons using Button widgets
        and calculating font size and spacing using the parent method.
        Also sets the buttons' areas if needed for display
        (for example calling the button's action
        even if not directly on the label).

        Parameters
        ----------
        button_actions: dict[str, tuple[Callable, Any]]
            A dictionary containing the buttons' labels and their actions.
        """

        if not button_actions:
            return

        self.calculate_label_spacing(
            list(button_actions.keys())
        )

        start_y: int = self.posy + self.padding - self.font_size

        self.buttons: dict[str, Button] = {
            label: Button(
                (
                    self.center_label_x(label)
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

        """
        Calculates the total area of a button,
        so not just the label size, but the whole 'rectangle' background size.

        Parameters
        ----------
        button: Button
            The button for which to set the area.
        nb: int
            The index of the button on the panel.
        """

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

        button.set_area((sx, sy, ex - sx, ey - sy))

    def display_widget(self) -> None:

        """
        Draws the panel's outline and inside
        and displays all the buttons (and their areas if needed).
        """

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

        if not hasattr(self, "buttons"):
            return

        for i, button in enumerate(self.buttons.values()):

            if button.is_in_area:

                pr.draw_rectangle_rounded(
                    button.area,
                    self.roundness,
                    4,
                    self.hover_color
                )

            button.display_widget()
