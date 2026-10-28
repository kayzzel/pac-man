import pyray as pr
from .Widget import Widget
from typing import Any, Callable


BASE_FRAME_DELAY: int = 8


class Icon(Widget):

    # basic icon template widget, can be instanced by itself

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        max_size: tuple[int, int],
        to_resize: bool = False
    ) -> None:

        self.image_path: str = image_path
        self.max_size: tuple[int, int] = max_size
        self.to_resize: bool = to_resize

        self._load_image(image_path)

        super().__init__(x, y, self.texture.width, self.texture.height)

    def _resize_image(
        self,
        max_w: int,
        max_h: int,
        resize_needed: bool = False
    ) -> None:

        new_width: int = self.image.width
        if new_width > max_w or resize_needed:
            new_width = max_w

        new_height: int = self.image.height
        if new_height > max_h or resize_needed:
            new_height = max_h

        pr.image_resize(self.image, new_width, new_height)

    def _load_image(self, image_path: str) -> None:

        self.image: pr.Image = pr.load_image(image_path)
        self._resize_image(*self.max_size, self.to_resize)
        self.texture: pr.Texture = pr.load_texture_from_image(self.image)

    @property
    def lower_bounds(self) -> tuple[int, int]:

        return (self.posx + self.w, self.posy + self.h)

    def display_widget(self) -> None:

        self._update_widget()
        pr.draw_texture(self.texture, self.posx, self.posy, pr.WHITE)


class AnimIcon(Icon):

    # animated icon such as gifs

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        max_size: tuple[int, int],
        to_resize: bool = False,
        frame_delay: int = BASE_FRAME_DELAY
    ) -> None:

        super().__init__(x, y, image_path, max_size)
        self.to_resize = to_resize

        self.frame_delay: int = frame_delay

    def _load_image(self, image_path: str) -> None:

        self.frames: Any = pr.ffi.new('int *', 0)
        self.image: pr.Image = pr.load_image_anim(image_path, self.frames)
        self.frames_value = self.frames[0]

        self.cur_frame: int = 0
        self.frame_counter: int = 0
        self.loop_finished: bool = False

        self.texture: pr.Texture = pr.load_texture_from_image(self.image)

    def _update_widget(self) -> None:

        # updating frames for the animated image

        self.frame_counter += 1

        if self.frame_counter >= self.frame_delay:

            self.cur_frame += 1
            self.loop_finished = False

            if self.cur_frame >= self.frames_value:
                self.cur_frame = 0
                self.loop_finished = True

            nx_frame_offset: int = (
                self.image.width * self.image.height * 4 * self.cur_frame
            )

            data_ptr = pr.ffi.cast("unsigned char *", self.image.data)
            offset_ptr = pr.ffi.cast("void *", data_ptr + nx_frame_offset)

            pr.update_texture(
                self.texture,
                offset_ptr
            )

            self.frame_counter = 0

    def display_widget(self) -> None:

        if not self.to_resize:
            super().display_widget()
            return

        # different resizing for animated images, using vectors

        self._update_widget()

        src_rect: pr.Rectangle = pr.Rectangle(
            0, 0, self.image.width, self.image.height
        )
        dest_rect: pr.Rectangle = pr.Rectangle(
            self.posx, self.posy, *self.max_size
        )

        pr.draw_texture_pro(
            self.texture, src_rect, dest_rect, pr.Vector2(0, 0), 0, pr.WHITE
        )


class ClickableIcon(Icon):

    # icon that can be pressed and calls a function

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        action: tuple[Callable, Any],
        max_size: tuple[int, int],
        to_resize: bool = False,
        magnify: bool = True
    ) -> None:

        super().__init__(x, y, image_path, max_size, to_resize)

        self.action: tuple[Callable, Any] = action
        # magnifying means the icon becomes bigger when mouse hovers
        self.magnify: bool = magnify
        self.was_in: bool = False

    def _update_widget(self) -> None:

        if self.was_in and not self.is_in:

            self.was_in = False

            if self.magnify:

                self._resize_image(
                    self.max_size[0],
                    self.max_size[1],
                    True
                )
                self.texture = pr.load_texture_from_image(self.image)

        elif not self.was_in and self.is_in:

            self.was_in = True

            if self.magnify:

                self._resize_image(
                    self.max_size[0] + self.max_size[0] // 10,
                    self.max_size[1] + self.max_size[1] // 10,
                    True
                )
                self.texture = pr.load_texture_from_image(self.image)

        if self.is_pressed:
            self.call_action()
