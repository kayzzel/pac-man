class Collectible:
    def __init__(self, collectible_type: str, points: int) -> None:
        self.collectible_type = collectible_type
        self.points = points

    def collected(self) -> None:
        ...
