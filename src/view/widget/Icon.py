import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from .Widget import Widget
from typing import Any, Callable


BASE_FRAME_DELAY: int = 5


class Icon(Widget):

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        max_size: tuple[int, int]
    ) -> None:

        self.max_size: tuple[int, int] = max_size

        self._load_image(image_path)

        super().__init__(x, y, self.i_w, self.i_h)

    def _resize_image(self, new_width: int, new_height: int) -> None:

        pr.image_resize(self.image, new_width, new_height)
        self.texture: pr.Texture = pr.load_texture_from_image(self.image)

    def _load_image(self, image_path: str) -> None:

        self.image: pr.Image = pr.load_image(image_path)

        new_width: int = self.image.width
        if new_width > self.max_size[0]:
            new_width = self.max_size[0]

        new_height: int = self.image.height
        if new_height > self.max_size[1]:
            new_height = self.max_size[1]

        self._resize_image(new_width, new_height)

    @property
    def i_w(self) -> int:

        return self.texture.width

    @property
    def i_h(self) -> int:

        return self.texture.height

    @property
    def posx(self) -> int:

        return (
            self.x
            if self.x >= 0
            else (sw() - self.i_w) // -(self.x)
        )

    @property
    def posy(self) -> int:

        return (
            self.y
            if self.y >= 0
            else (sh() - self.i_h) // -(self.y)
        )

    @property
    def get_lower_bounds(self) -> tuple[int, int]:

        return (self.posx + self.i_w, self.posy + self.i_h)

    def display_widget(self) -> None:

        self._update_widget()
        pr.draw_texture(self.texture, self.posx, self.posy, pr.WHITE)


class AnimIcon(Icon):

    def _load_image(self, image_path: str) -> None:

        self.frames: Any = pr.ffi.new('int *', 1)
        self.image: pr.Image = pr.load_image_anim(image_path, self.frames)

        self.cur_frame: int = 0
        self.frame_delay: int = BASE_FRAME_DELAY
        self.frame_counter: int = 0

        self.texture: pr.Texture = pr.load_texture_from_image(self.image)
        # new_width: int = self.image.width
        # if new_width > self.max_size[0]:
        #     new_width = self.max_size[0]

        # new_height: int = self.image.height
        # if new_height > self.max_size[1]:
        #     new_height = self.max_size[1]

        # self._resize_image(new_width, new_height)

    def _update_widget(self) -> None:

        self.frame_counter += 1

        if self.frame_counter >= self.frame_delay:

            self.cur_frame += 1

            if self.cur_frame >= self.frames[0]:
                self.cur_frame = 0

            nx_frame_offset: int = (
                self.image.width * self.image.height * 4 * self.cur_frame
            )

            pr.update_texture(
                self.texture,
                self.image.data + nx_frame_offset
            )

            self.frame_counter = 0


class ClickableIcon(Icon):

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        action: tuple[Callable, Any],
        max_size: tuple[int, int]
    ) -> None:

        super().__init__(x, y, image_path, max_size)
        self.action: tuple[Callable, Any] = action
        self.was_in: bool = False

    def _update_widget(self) -> None:

        if self.was_in and not self.is_in:

            self.was_in = False
            self._resize_image(
                self.max_size[0],
                self.max_size[1]
            )

        elif not self.was_in and self.is_in:

            self.was_in = True
            self._resize_image(
                self.max_size[0] + self.max_size[0] // 10,
                self.max_size[1] + self.max_size[1] // 10
            )

        if self.is_pressed:
            self.call_action()
