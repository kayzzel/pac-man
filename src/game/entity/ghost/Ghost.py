class Ghost:
    def __init__(self) -> None:
        self.pos_x = 0
        self.pos_y = 0
        self.direction = "N"
        self.state = "Normal"
        self.target: tuple[int, int] = (0, 0)
