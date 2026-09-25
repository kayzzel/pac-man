from ..Entity import Entity

from abc import ABC, abstractmethod
from random import choice
from math import modf


class Ghost(Entity, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.state = "Normal"
        self.target: tuple[int, int] = (0, 0)
        self.spawn_point: tuple[int, int] = (0, 0)
        self.scater_point: tuple[int, int] = (0, 0)

    @abstractmethod
    def define_target(self, entitys: dict[str, Entity]) -> None:
        ...

    def __chose_direction(self, walls: dict[str, bool]) -> None:

        OPOSITE: dict[str, str] = {
                "N": "S",
                "S": "N",
                "E": "W",
                "W": "E"
        }

        VECTORS: dict[str, tuple[int, int]] = {
                "N": (0,-1),
                "S": (0,1),
                "E": (1,0),
                "W": (-1,0)
        }


        possibles = [key for key, value in walls.items() if not value]

        if len(possibles) == 0:
            raise ValueError("No possible direction for the ghost")

        if len(possibles) == 1:
            self.direction = possibles[0]
            return

        try:
            possibles.remove(OPOSITE[self.direction])
        except:
            pass

        if len(possibles) == 1:
            self.direction = possibles[0]
            return

        if self.state == "frightened":
            self.direction = choice(possibles)
            return

        distances = []
        for possible in possibles:
            new_x, new_y = VECTORS[possible]
            distance = (
                abs(int(self.pos_x) + new_x - self.target[0])
                + abs((self.pos_y) + new_y - self.target[1])
            )
            distances.append((possible, distance))

        self.direction = min(distances, key=(lambda d: d[1]))[0]
    
    def update(
            self,
            entitys: dict[str, Entity],
            walls: dict[str, bool],
            can_change: bool = True,
        ) -> None:

        self.walk()
        
        if (modf(self.pos_x)[0] != 0.5 or modf(self.pos_y)[0] != 0.5):
            return

        if (can_change):
            self.define_target(entitys)

        self.__chose_direction(walls)
