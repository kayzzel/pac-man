from .Widget import Widget
import pyray as pr


class Icon(Widget):

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        max_size: tuple[int, int]
    ) -> None:

        self.image: pr.Image = pr.load_image(image_path)
        self.texture: pr.Texture = pr.load_texture_from_image(self.image)
        super().__init__(x, y, self.texture.width, self.texture.height)
        self.max_size: tuple[int, int] = max_size
        self._load_image(image_path)

    def _load_image(self, image_path: str) -> None:

        new_width: int = self.i_w
        if self.i_w > self.max_size[0]:
            new_width = self.max_size[0]

        new_height: int = self.i_h
        if self.i_h > self.max_size[1]:
            new_height = self.max_size[1]

        pr.image_resize(self.image, new_width, new_height)
        self.texture = pr.load_texture_from_image(self.image)

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

    def display_widget(self) -> None:

        pr.draw_texture(self.texture, self.posx, self.posy, pr.WHITE)
