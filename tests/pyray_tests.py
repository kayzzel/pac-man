import pyray as pr

SCR_WIDTH = 800
SCR_HEIGHT = 450

BUTTON_TEXT_SIZE = 20

NB_BUTTONS = 4


class Button:

    def __init__(self, x: int, y: int, label: str, font_sz: int) -> None:

        self.x: int = x
        self.y: int = y
        self.pos: tuple[int, int] = (self.x, self.y)
        self.label: str = label
        self.w: int = pr.measure_text(self.label, font_sz)
        self.h: int = font_sz
        self.size: tuple[int, int] = (self.w, self.h)
        self.color: pr.Color = pr.WHITE

    def is_in(self, posx: int, posy: int) -> bool:

        return (
            self.x <= posx <= self.x + self.w
        ) and (
            self.y <= posy <= self.y + self.h
        )

    def draw_button(self) -> None:

        self.color = (
            pr.DARKGRAY
            if self.is_in(pr.get_mouse_x(), pr.get_mouse_y())
            else pr.WHITE
        )

        pr.draw_text(self.label, *self.pos, self.h, self.color)

    @property
    def is_pressed(self) -> bool:

        return (
            pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT)
        ) and (
            self.is_in(pr.get_mouse_x(), pr.get_mouse_y())
        )


class Title:

    def __init__(self, y: int, texture_path: str) -> None:

        self.texture = self._load_new_image(texture_path)
        self.y: int = y

    @property
    def get_x(self) -> int:

        return (SCR_WIDTH - self.texture.width) // 2

    @property
    def get_lower_bounds(self) -> tuple[int, int]:

        return (self.get_x + self.texture.width, self.y + self.texture.height)

    def _load_new_image(self, image_path: str) -> pr.Texture:

        image: pr.Image = pr.load_image(image_path)
        pr.image_resize(image, min(image.width, SCR_WIDTH - 40), min(image.height, SCR_HEIGHT // 3))
        return pr.load_texture_from_image(image)

    def draw_title(self) -> None:

        pr.draw_texture(self.texture, self.get_x, self.y, pr.WHITE)


def get_x_centered(width: int) -> int:

    return (SCR_WIDTH - width) // 2


pr.init_window(SCR_WIDTH, SCR_HEIGHT, "pac-man menu example")

pr.set_target_fps(60)

game_title: Title = Title(SCR_HEIGHT // 5, "pac-man_title.png")

button_st_y = game_title.get_lower_bounds[1] + 20
print(f"start y for buttons: {button_st_y}\n")

buttons: dict[str, Button] = {}

for button_label in ["start game", "view highscores", "instructions", "exit"]:

    cur_button = Button(
        get_x_centered(pr.measure_text(button_label, BUTTON_TEXT_SIZE)),
        button_st_y,
        button_label,
        BUTTON_TEXT_SIZE
    )
    print(f"width of the button: {pr.measure_text(button_label, BUTTON_TEXT_SIZE)}\n")
    buttons[button_label] = cur_button
    print(f"button {button_label} position : {cur_button.x, cur_button.y}\n")
    button_st_y += BUTTON_TEXT_SIZE + 10

while not pr.window_should_close():

    if buttons["exit"].is_pressed:
        break

    pr.begin_drawing()

    pr.clear_background(pr.BLACK)

    game_title.draw_title()

    for button in buttons.values():
        button.draw_button()

    pr.end_drawing()

pr.unload_texture(game_title.texture)
pr.close_window()
