from ..Entity import Entity
from .Ghost import Ghost


class Blinky(Ghost):
    def __init__(self) -> None:
        super().__init__()

    def define_target(self, entitys: dict[str, Entity]) -> int:
        if (super().define_target(entitys)):
            return 0

        pacman = entitys["pacman"]

        self.target = (int(pacman.pos_x), int(pacman.pos_y))

        return 0
