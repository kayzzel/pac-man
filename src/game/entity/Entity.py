from abc import ABC
from math import modf


class Entity(ABC):
    """Base of every moving thing: position, speed and one direction."""

    def __init__(self, name: str) -> None:
        """
            Description:
        Create an entity at the origin, facing north, at the default
        speed of 0.02 cell per tick (a full cell every 50 ticks).

            Parameters:
            name -> name of the entity, used to identify it
        """
        self.name: str = name
        self.pos_x: float = 0.0
        self.pos_y: float = 0.0
        self.speed = 0.02
        self.direction = "N"

    def walk(self) -> None:
        """
            Description:
        Move the entity one step (its speed) in its direction. When the
        step crosses the middle of a cell (the x.5 center), the
        position is snapped exactly on it: every entity therefore
        always lands on the centers, where the turns are decided.
        """
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
