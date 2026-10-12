from .Ghost import Ghost
from ..Entity import Entity


class Clyde(Ghost):
    def __init__(self) -> None:
        super().__init__("clyde")

    def define_target(self, entities: dict[str, Entity]) -> int:
        if (super().define_target(entities)):
            return 0

        pacman = entities["pacman"]

        distance = (
            abs(int(self.pos_x) - int(pacman.pos_x))
            + abs(int(self.pos_y) - int(pacman.pos_y))
        )
        if distance > 8:
            if self.target != (int(pacman.pos_x), int(pacman.pos_y)):
                self.path = []
                self.target = (int(pacman.pos_x), int(pacman.pos_y))

        else:
            if self.target != self.scatter_point:
                self.path = []
                self.target = self.scatter_point

        return 0
