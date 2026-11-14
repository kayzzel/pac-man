import pyray as pr
from pyray import get_screen_width as sw
from pyray import get_screen_height as sh
from .Widget import Widget
from typing import Any, Callable


BASE_FRAME_DELAY: int = 8


class Icon(Widget):

    """
    Basic icon template widget, can be instanced by itself
    """

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        max_size: tuple[int, int],
        to_resize: bool = False
    ) -> None:

        """
        Initializes the main attributes of an Icon,
        loads the image, and resizes it if needed.

        Parameters
        ----------
        x: int
            The x coordinate of the icon.
        y: int
            The y coordinate of the icon.
        image_path: str
            The path to the icon's image.
        max_size: tuple[int, int]
            The max size the icon can have,
            or the size it MUST have (if 'to_resize' is True).
        to_resize: bool (default False)
            Indicates if the icon must be resized to fit max size.
        """

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

        """
        Resizes the icon's image to fit the size given
        if 'resize_needed' is True or the image's size is too big.

        Parameters
        ----------
        max_w: int
            Either the width the icon MUST have (if 'resize_needed' is True),
            or the width the icon must not go over.
        max_h: int
            Either the height the icon MUST have (if 'resize_needed' is True),
            or the height the icon must not go over.
        resize_needed: bool (default False)
            Indicates whether or not the icon should be resized no matter what.
        """

        new_width: int = self.image.width
        if new_width > max_w or resize_needed:
            new_width = max_w

        new_height: int = self.image.height
        if new_height > max_h or resize_needed:
            new_height = max_h

        pr.image_resize(self.image, new_width, new_height)

    def _load_image(self, image_path: str) -> None:

        """
        Loads the image of the icon with the path given.

        Parameters
        ----------
        image_path: str
            The path to the image the icon has to load.
        """

        self._unload_image()
        self.image: pr.Image = pr.load_image(image_path)
        self._resize_image(*self.max_size, self.to_resize)
        self.texture: pr.Texture = pr.load_texture_from_image(self.image)

    def _unload_image(self) -> None:

        """
        Unloads both the image and the texture of the icon,
        if they have not already been unloaded.
        """

        if hasattr(self, "texture") and self.texture is not None:
            pr.unload_texture(self.texture)
            self.texture = None
        if hasattr(self, "image") and self.image is not None:
            pr.unload_image(self.image)
            self.image = None

    def _ensure_loaded(self) -> None:

        """
        Checks whether or not the icon has unloaded image or texture,
        and reloads them if it's the case.
        """

        if self.texture is None or self.image is None:
            self._load_image(self.image_path)

    @property
    def i_w(self) -> int:

        """
        Returns the correct width of the icon,
        based on if it has been resized to fit 'max_size'.

        Returns
        -------
        int
            The width of the icon.
        """

        self._ensure_loaded()
        return (
            self.texture.width
            if not self.to_resize
            else self.max_size[0]
        )

    @property
    def i_h(self) -> int:

        """
        Returns the correct height of the icon,
        based on if it has been resized to fit 'max_size'.

        Returns
        -------
        int
            The height of the icon.
        """

        self._ensure_loaded()
        return (
            self.texture.height
            if not self.to_resize
            else self.max_size[1]
        )

    @property
    def posx(self) -> int:

        """
        An override of the Widget's parent method,
        just using the 'i_w' method instead of 'w'
        for the width calculation.

        Returns
        -------
        int
            The calculated x coordinate of the icon.
        """

        return (
            self.x
            if self.x >= 0
            else (sw() - self.i_w) // -(self.x)
        )

    @property
    def posy(self) -> int:

        """
        An override of the Widget's parent method,
        just using the 'i_h' method instead of 'h'
        for the height calculation.

        Returns
        -------
        int
            The calculated y coordinate of the icon.
        """

        return (
            self.y
            if self.y >= 0
            else (sh() - self.i_h) // -(self.y)
        )

    @property
    def lower_bounds(self) -> tuple[int, int]:

        """
        Same as the Widget's parent method 'lowerbound',
        but also giving the end x of the icon, not just hte end y,
        and using the 'i_w' and 'i_h' methods instead of 'w' and 'h'
        for the calculation.

        Returns
        -------
        tuple[int, int]
            The calculated end x and y coordinates of the icon.
        """

        return (self.posx + self.i_w, self.posy + self.i_h)

    def display_widget(self) -> None:

        """
        Updates and displays the icon on the screen.
        """

        self._update_widget()
        self._ensure_loaded()
        pr.draw_texture(self.texture, self.posx, self.posy, pr.RAYWHITE)


class AnimIcon(Icon):

    """
    Animated icon for images such as gifs.
    """

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        max_size: tuple[int, int],
        to_resize: bool = False,
        frame_delay: int = BASE_FRAME_DELAY
    ) -> None:

        """
        Initializes the main attributes of an AnimIcon,
        loads the image, and resizes it if needed.

        Parameters
        ----------
        x: int
            The x coordinate of the icon.
        y: int
            The y coordinate of the icon.
        image_path: str
            The path to the icon's image.
        max_size: tuple[int, int]
            The max size the icon can have,
            or the size it MUST have (if 'to_resize' is True).
        to_resize: bool (default False)
            Indicates if the icon must be resized to fit max size.
        frame_delay: int (default BASE_FRAME_DELAY)
            The rate at which the icon cycles through frames
            (basically the speed of the animation).
        """

        super().__init__(x, y, image_path, max_size)
        self.to_resize = to_resize

        self.frame_delay: int = frame_delay

    def _load_image(self, image_path: str) -> None:

        """
        Loads the image of the icon with the path given,
        first initializing frames by C casting,
        then (re)setting all the animation variables.

        Parameters
        ----------
        image_path: str
            The path to the image the icon has to load.
        """

        self._unload_image()
        self.frames: Any = pr.ffi.new('int *', 0)
        self.image: pr.Image = pr.load_image_anim(image_path, self.frames)
        self.frames_value = self.frames[0]

        self.cur_frame: int = 0
        self.frame_counter: int = 0
        self.loop_finished: bool = False

        self.texture: pr.Texture = pr.load_texture_from_image(self.image)

    def reset_loop(self) -> None:

        """
        Resets the animation loop for the AnimIcon (return to first frame).
        """

        self.frame_counter = 0
        self.cur_frame = 0
        self.loop_finished = False

    def _update_widget(self) -> None:

        """
        Updates the icon's frame and its texture
        by using C casting and a frame offset.
        """

        self._ensure_loaded()
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

        """
        Updates and displays the AnimIcon,
        but also (if needed) resizes the current frame texture
        by moving it from a source rectangle with old size
        to a new rectangle with new size (vectors).
        """

        if not self.to_resize:
            super().display_widget()
            return

        self._update_widget()
        super()._ensure_loaded()

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

    """
    Icon that can be pressed and calls a function.
    """

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

        """
        Initializes the main attributes of a ClickableIcon,
        loads the image, and resizes it if needed.

        Parameters
        ----------
        x: int
            The x coordinate of the icon.
        y: int
            The y coordinate of the icon.
        image_path: str
            The path to the icon's image.
        action: tuple[Callable, Any]
            Contains the function and its arguments
            that the Icon needs to call when pressed.
        max_size: tuple[int, int]
            The max size the icon can have,
            or the size it MUST have (if 'to_resize' is True).
        to_resize: bool (default False)
            Indicates if the icon must be resized to fit max size.
        magnify: bool (default True)
            Indicates whether or not the icon is a bit enlarged
            when the mouse hovers over it.
        """

        super().__init__(x, y, image_path, max_size, to_resize)

        self.action: tuple[Callable, Any] = action
        self.magnify: bool = magnify
        self.was_in: bool = False

    def _update_widget(self) -> None:

        """
        Updates the widget by checking whether or not
        the icon should be enlarged (mouse hovers)
        and if the icon's function should be called.
        """

        if self.was_in and not self.is_in:

            self.was_in = False

            if self.magnify:

                self._resize_image(
                    self.max_size[0],
                    self.max_size[1],
                    True
                )
                pr.unload_texture(self.texture)
                self.texture = pr.load_texture_from_image(self.image)

        elif not self.was_in and self.is_in:

            self.was_in = True

            if self.magnify:

                self._resize_image(
                    self.max_size[0] + self.max_size[0] // 10,
                    self.max_size[1] + self.max_size[1] // 10,
                    True
                )
                pr.unload_texture(self.texture)
                self.texture = pr.load_texture_from_image(self.image)

        if self.is_pressed:
            self.call_action()
