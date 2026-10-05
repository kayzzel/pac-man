from abc import ABC
from math import modf


class Entity(ABC):
    def __init__(self) -> None:
        self.pos_x: float = 0.0
        self.pos_y: float = 0.0
        self.speed = 0.02
        self.direction = "N"

    def walk(self) -> None:
        match self.direction:
            case "N":
                split_nbr = modf(self.pos_y)
                if (split_nbr[0] > 0.5 and split_nbr[0] - self.speed < 0.5):
                    self.pos_y = split_nbr[1] + 0.5
                else:
                    self.pos_y -= self.speed
            case "S":
                split_nbr = modf(self.pos_y)
                if (split_nbr[0] < 0.5 and split_nbr[0] + self.speed > 0.5):
                    self.pos_y = split_nbr[1] + 0.5
                else:
                    self.pos_y += self.speed
            case "W":
                split_nbr = modf(self.pos_x)
                if (split_nbr[0] > 0.5 and split_nbr[0] - self.speed < 0.5):
                    self.pos_x = split_nbr[1] + 0.5
                else:
                    self.pos_x -= self.speed
            case "E":
                split_nbr = modf(self.pos_x)
                if (split_nbr[0] < 0.5 and split_nbr[0] + self.speed > 0.5):
                    self.pos_x = split_nbr[1] + 0.5
                else:
                    self.pos_x += self.speed
