import pyray as pr
from ..App import App
from ..view import View, Main_menu, Map_choice_menu, Pause_menu

pr.init_window(800, 450, "pac-man menu example")

pr.set_target_fps(60)

pr.set_exit_key(pr.KEY_NULL)

app: App = App()

menu: Main_menu = Main_menu(app)
map_choice: Map_choice_menu = Map_choice_menu(app)
pause_menu: Pause_menu = Pause_menu(app)

views: dict[str, View] = {
    "main_menu": menu,
    "map_choice_menu": map_choice,
    "pause_menu": pause_menu
}
app.add_view(views)

app.change_view("main_menu")

while not pr.window_should_close():

    pr.clear_background(pr.BLACK)

    pr.begin_drawing()

    app.display_app()

    pr.end_drawing()

pr.close_window()
