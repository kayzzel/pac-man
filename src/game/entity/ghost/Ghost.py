from ..Entity import Entity
from ..Pac_man import Pac_man
from ...map.Cell import Cell

from abc import ABC, abstractmethod
from random import choice
from math import modf
from enum import Enum


class Ghost_state(Enum):
    CHASE = "chase"
    EATEN = "eaten"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"


class Ghost(Entity, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.state: Ghost_state = Ghost_state.CHASE
        self.target: tuple[int, int] = (0, 0)
        self.spawn_point: tuple[int, int] = (0, 0)
        self.scatter_point: tuple[int, int] = (0, 0)

    @abstractmethod
    def define_target(self, entitys: dict[str, Entity]) -> int:
        if self.state == Ghost_state.FRIGHTENED:
            return 1

        if self.state == Ghost_state.EATEN:
            self.target = self.spawn_point
            return 1

        if self.state == Ghost_state.SCATTER:
            self.target = self.scatter_point
            return 1

        return 0

    def set_eaten(self) -> None:
        if self.state != Ghost_state.EATEN:
            self.state = Ghost_state.EATEN
            self.speed *= 2

    def __respawned(self) -> None:
        self.speed /=2

    def __chose_state(self, pacman: Pac_man, timer: int) -> None:
        OPOSITE: dict[str, str] = {
                "N": "S",
                "S": "N",
                "E": "W",
                "W": "E"
        }

        if self.state == Ghost_state.EATEN :
            if (int(self.pos_x), int(self.pos_y)) != self.spawn_point:
                return
            else:
                self.__respawned()

        if (
                pacman.last_super_pacgum_time >= 0 and
                timer - pacman.last_super_pacgum_time < 7
                ):
            if self.state != Ghost_state.FRIGHTENED:
                self.direction = OPOSITE[self.direction]
                self.state = Ghost_state.FRIGHTENED
            return

        if timer < 7 and self.state != Ghost_state.SCATTER:     # 7"
            self.state = Ghost_state.SCATTER
            self.direction = OPOSITE[self.direction]
        elif timer < 27 and self.state != Ghost_state.CHASE:  # 20"
            self.state = Ghost_state.CHASE
            self.direction = OPOSITE[self.direction]
        elif timer < 34 and self.state != Ghost_state.SCATTER:  # 7"
            self.state = Ghost_state.SCATTER
            self.direction = OPOSITE[self.direction]
        elif timer < 54 and self.state != Ghost_state.CHASE:  # 20"
            self.state = Ghost_state.CHASE
            self.direction = OPOSITE[self.direction]
        elif timer < 59 and self.state != Ghost_state.SCATTER:  # 5"
            self.state = Ghost_state.SCATTER
            self.direction = OPOSITE[self.direction]
        elif timer < 79 and self.state != Ghost_state.CHASE:  # 20"
            self.state = Ghost_state.CHASE
            self.direction = OPOSITE[self.direction]
        elif timer < 84 and self.state != Ghost_state.SCATTER:  # 5"
            self.state = Ghost_state.SCATTER
            self.direction = OPOSITE[self.direction]
        elif self.state != Ghost_state.CHASE:             # -
            self.state = Ghost_state.CHASE
            self.direction = OPOSITE[self.direction]

    def __chose_direction(self, walls: dict[str, bool]) -> None:

        OPOSITE: dict[str, str] = {
                "N": "S",
                "S": "N",
                "E": "W",
                "W": "E"
        }

        VECTORS: dict[str, tuple[int, int]] = {
                "N": (0, -1),
                "S": (0, 1),
                "E": (1, 0),
                "W": (-1, 0)
        }

        possibles = [key for key, value in walls.items() if not value]

        if len(possibles) == 0:
            raise ValueError("No possible direction for the ghost")

        if len(possibles) == 1:
            self.direction = possibles[0]
            return

        if (OPOSITE[self.direction] in possibles):
            possibles.remove(OPOSITE[self.direction])

        if len(possibles) == 1:
            self.direction = possibles[0]
            return

        if self.state == Ghost_state.FRIGHTENED:
            self.direction = choice(possibles)
            return

        distances = []
        for possible in possibles:
            new_x, new_y = VECTORS[possible]
            distance = (
                abs(int(self.pos_x) + new_x - self.target[0])
                + abs(int(self.pos_y) + new_y - self.target[1])
            )
            distances.append((possible, distance))

        self.direction = min(distances, key=(lambda d: d[1]))[0]

    def update(
                self,
                entitys: dict[str, Entity],
                cell: Cell,
                timer: int
            ) -> None:

        if isinstance(entitys["pacman"], Pac_man):
            self.__chose_state(entitys["pacman"], timer)
        else:
            raise ValueError("There must be a pacman key in the entitys")

        if (modf(self.pos_x)[0] == 0.5 and modf(self.pos_y)[0] == 0.5):

            if (not cell.special):
                self.define_target(entitys)

            self.__chose_direction(cell.walls)

        self.walk()
