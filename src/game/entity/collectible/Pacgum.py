from .Collectible import Collectible


class Pacgum(Collectible):
    def __init__(self, x: int, y: int, points: int) -> None:
        super().__init__(x, y, points)
