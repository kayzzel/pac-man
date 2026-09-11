import pyray as pr
from ..view import Main_menu


pr.init_window(800, 450, "pac-man menu example")

pr.set_target_fps(60)

menu: Main_menu = Main_menu("src/view/assets/gifs/pac-man_bg_gif.gif")

while not pr.window_should_close():

    menu.update()

    pr.clear_background(pr.BLACK)

    pr.begin_drawing()

    menu.display_view()

    pr.end_drawing()

pr.close_window()
