from ..entity.collectible.Collectible import Collectible

class Cell:
    def __init__(self, pos_x: int, pos_y: int) -> None:
        self.pos_x: int = pos_x
        self.pos_y: int = pos_y
        self.collectible: Collectible | None = None
        self.walls: dict[str, bool] = {
                "north": False,
                "south": False,
                "east": False,
                "west": False,
        }
