from ..Entity import Entity
from .Ghost import Ghost


class Blinky(Ghost):
    def __init__(self) -> None:
        super().__init__("blinky")

    def define_target(self, entities: dict[str, Entity]) -> int:
        if (super().define_target(entities)):
            return 0

        pacman = entities["pacman"]

        self.target = (int(pacman.pos_x), int(pacman.pos_y))

        return 0
