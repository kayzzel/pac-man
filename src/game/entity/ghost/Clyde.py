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
            self.target = (int(pacman.pos_x), int(pacman.pos_y))

        else:
            self.target = (
                        int(self.scatter_point[0]),
                        int(self.scatter_point[1])
                   )

        return 0
