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
                splited_nbr = modf(self.pos_y)
                if (splited_nbr[0] > 0.5 and splited_nbr[0] - self.speed < 0.5):
                    self.pos_y = splited_nbr[1] + 0.5
                else:
                    self.pos_y -= self.speed
            case "S":
                splited_nbr = modf(self.pos_y)
                if (splited_nbr[0] < 0.5 and splited_nbr[0] + self.speed > 0.5):
                    self.pos_y = splited_nbr[1] + 0.5
                else:
                    self.pos_y += self.speed
            case "W":
                splited_nbr = modf(self.pos_x)
                if (splited_nbr[0] > 0.5 and splited_nbr[0] - self.speed < 0.5):
                    self.pos_x = splited_nbr[1] + 0.5
                else:
                    self.pos_x -= self.speed
            case "E":
                splited_nbr = modf(self.pos_x)
                if (splited_nbr[0] < 0.5 and splited_nbr[0] + self.speed > 0.5):
                    self.pos_x = splited_nbr[1] + 0.5
                else:
                    self.pos_x += self.speed
