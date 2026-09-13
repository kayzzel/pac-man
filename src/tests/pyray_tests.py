import pyray as pr
from typing import Any
from ..view import View, Main_menu, Map_choice_menu, Pause_menu

pr.init_window(800, 450, "pac-man menu example")

pr.set_target_fps(60)

menu: Main_menu = Main_menu()
map_choice: Map_choice_menu = Map_choice_menu()
pause_menu: Pause_menu = Pause_menu()

views: dict[str, View] = {
    "main_menu": menu,
    "map_choice_menu": map_choice,
    "pause_menu": pause_menu
}

cur_view: View = pause_menu

while not pr.window_should_close():

    update_result: Any = cur_view.update()
    if isinstance(update_result, str):
        cur_view = views[update_result]

    pr.clear_background(pr.BLACK)

    pr.begin_drawing()

    cur_view.display_view()

    pr.end_drawing()

pr.close_window()
