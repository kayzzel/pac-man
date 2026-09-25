from ..Entity import Entity
from .Ghost import Ghost

class Pinky(Ghost):
    def __init__(self):
        super().__init__()

    def define_target(self, entitys: dict[str, Entity]) -> None:

        if (super().define_target):
            return

        VECTORS: dict[str, tuple[int, int]] = {
                "N": (-4,-4),
                "S": (0,4),
                "E": (4,0),
                "W": (-4,0)
        }

        pacman = entitys["pacman"]
        vector = VECTORS[pacman.direction]

        self.target = (
            int(pacman.pos_x) + vector[0],
            int(pacman.pos_y) + vector[1]
        )
