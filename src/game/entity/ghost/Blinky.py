from ..Entity import Entity
from .Ghost import Ghost, Ghost_state

class Blinky(Ghost):
    def __init__(self):
        super().__init__()

    def define_target(self, entitys: dict[str, Entity]) -> None:
        if (super().define_target):
            return

        pacman = entitys["pacman"]

        self.target = (int(pacman.pos_x), int(pacman.pos_y))

