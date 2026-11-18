from .Collectible import Collectible


class Pacgum(Collectible):
    def __init__(self, x: int, y: int, points: int = 10) -> None:
        super().__init__("pacgum", x, y, points)
