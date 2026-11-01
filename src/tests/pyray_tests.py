import pyray as pr
from ..App import App
from ..view import View, Main_menu, Map_choice_menu
from ..view.widget.Text import Text, PACMAN_FONT

# pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
pr.set_trace_log_level(pr.LOG_ERROR)

pr.init_window(1920, 1080, "pac-man menu example")

pr.set_target_fps(60)

pr.set_exit_key(pr.KEY_NULL)

app: App = App()

map_choice: Map_choice_menu = Map_choice_menu(app)
# Text._load_font(PACMAN_FONT)

views: dict[str, View] = {
    "map_choice_menu": map_choice
}
app.add_view(views)

app.change_view(Main_menu(app))

while not pr.window_should_close():

    pr.clear_background(pr.BLACK)

    pr.begin_drawing()

    app.display_app()

    pr.end_drawing()

pr.close_window()
