from Ghost import Ghost
from ..Entity import Entity

class Clyde(Ghost):
    def __init__(self):
        super().__init__()

    def define_target(self, entitys: dict[str, Entity]) -> None:
        if (super().define_target):
            return

        pacman = entitys["pacman"]

        distance = (
            abs(int(self.pos_x) - int(pacman.pos_x))
            + abs((self.pos_y) - int(pacman.pos_y))
        )
        if distance > 8:
            self.target = (int(pacman.pos_x), int(pacman.pos_y))

        else:
            self.target = self.scatter_point
