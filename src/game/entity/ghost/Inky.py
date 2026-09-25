from ..Entity import Entity
from .Ghost import Ghost

class Inky(Ghost):
    def __init__(self):
        super().__init__()

    def define_target(self, entitys: dict[str, Entity]) -> None:

        if super().define_target(entitys):
            return

        VECTORS: dict[str, tuple[int, int]] = {
                "N": (-2,-2),
                "S": (0,2),
                "E": (2,0),
                "W": (-2,0)
        }

        pacman = entitys["pacman"]
        blinky = entitys["blinky"]
        vector = VECTORS[pacman.direction]

        central_x = int(pacman.pos_x) + vector[0]
        central_y = int(pacman.pos_y) + vector[1]

        self.target = (
            2 * central_x - int(blinky.pos_x),
            2 * central_y - int(blinky.pos_y),
        )

