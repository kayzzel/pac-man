from .Widget import Widget
from typing import Any
import pyray as pr


BASE_FRAME_DELAY: int = 5


class Icon(Widget):

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        is_gif: bool,
        max_size: tuple[int, int]
    ) -> None:

        self.max_size: tuple[int, int] = max_size

        self.is_gif: bool = is_gif
        if self.is_gif:
            self._load_gif(image_path)
        else:
            self._load_image(image_path)

        self.texture: pr.Texture = pr.load_texture_from_image(self.image)
        super().__init__(x, y, self.i_w, self.i_h)

    def _load_image(self, image_path: str) -> None:

        self.image: pr.Image = pr.load_image(image_path)

        new_width: int = self.image.width
        if new_width > self.max_size[0]:
            new_width = self.max_size[0]

        new_height: int = self.image.height
        if new_height > self.max_size[1]:
            new_height = self.max_size[1]

        pr.image_resize(self.image, new_width, new_height)

    def _load_gif(self, image_path: str) -> None:

        self.frames: Any = pr.ffi.new('int *', 1)
        self.image: pr.Image = pr.load_image_anim(image_path, self.frames)

        self.cur_frame: int = 0
        self.frame_delay: int = BASE_FRAME_DELAY
        self.frame_counter: int = 0

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
            else (pr.get_screen_width() - self.i_w) // -(self.x)
        )

    @property
    def posy(self) -> int:

        return (
            self.y
            if self.y >= 0
            else (pr.get_screen_height() - self.i_h) // -(self.y)
        )

    @property
    def get_lower_bounds(self) -> tuple[int, int]:

        return (self.posx + self.i_w, self.posy + self.i_h)

    def update_frames(self) -> None:

        self.frame_counter += 1

        if self.frame_counter >= self.frame_delay:

            self.cur_frame += 1

            if self.cur_frame >= self.frames[0]:
                self.cur_frame = 0

            self.nx_frame_offset = (
                self.image.width * self.image.height * 4 * self.cur_frame
            )

            pr.update_texture(
                self.texture,
                self.image.data + self.nx_frame_offset
            )

            self.frame_counter = 0

    def display_widget(self) -> None:

        if self.is_gif:
            self.update_frames()

        pr.draw_texture(self.texture, self.posx, self.posy, pr.WHITE)
