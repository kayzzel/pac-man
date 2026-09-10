class Ghost:
    def __init__(self) -> None:
        self.pos_x: float = 0.0
        self.pos_y: float = 0.0
        self.direction = "N"
        self.state = "Normal"
        self.target: tuple[int, int] = (0, 0)
