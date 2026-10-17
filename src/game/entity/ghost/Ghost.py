from ..Entity import Entity
from ..Pac_man import Pac_man
from ...map.Cell import Cell
from ....utils.enum_utils import Ghost_state
from ....utils.path_utils import next_direction
from ....utils.enum_utils import Ghost_state

from abc import ABC, abstractmethod
from random import choice
from math import modf


class Ghost(Entity, ABC):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.state: Ghost_state = Ghost_state.CHASE
        self.target: tuple[int, int] = (0, 0)
        self.spawn_point: tuple[float, float] = (0, 0)
        self.scatter_point: tuple[float, float] = (0, 0)
        self.real_path_finding = False

    @abstractmethod
    def define_target(self, entities: dict[str, Entity]) -> int:
        if self.state == Ghost_state.FRIGHTENED:
            return 1

        if self.state == Ghost_state.EATEN:
            self.target = (int(self.spawn_point[0]), int(self.spawn_point[1]))
            return 1

        if self.state == Ghost_state.SCATTER:
            self.target = (
                        int(self.scatter_point[0]),
                        int(self.scatter_point[1])
                   )
            return 1
        return 0

    def set_eaten(self) -> None:
        if self.state != Ghost_state.EATEN:
            self.state = Ghost_state.EATEN
            self.speed *= 2

    def __respawned(self) -> None:
        self.speed /= 2

    def __choose_state(self, pacman: Pac_man, elapsed_time: int) -> None:
        OPPOSITE: dict[str, str] = {
                "N": "S",
                "S": "N",
                "E": "W",
                "W": "E"
        }

        if self.state == Ghost_state.EATEN:
            if (self.pos_x, self.pos_y) != self.spawn_point:
                return
            else:
                self.__respawned()

        if pacman.is_energized:
            if self.state != Ghost_state.FRIGHTENED:
                self.direction = OPPOSITE[self.direction]
                self.state = Ghost_state.FRIGHTENED
            return

        wanted = self.__scheduled_state(elapsed_time)
        if self.state != wanted:
            self.state = wanted
            self.direction = OPPOSITE[self.direction]

    @staticmethod
    def __scheduled_state(elapsed_time: int) -> Ghost_state:
        schedule = (
            (7, Ghost_state.SCATTER),
            (27, Ghost_state.CHASE),
            (34, Ghost_state.SCATTER),
            (54, Ghost_state.CHASE),
            (59, Ghost_state.SCATTER),
            (79, Ghost_state.CHASE),
            (84, Ghost_state.SCATTER),
        )
        for limit, state in schedule:
            if elapsed_time < limit:
                return state
        return Ghost_state.CHASE

    def __choose_direction(
                self,
                walls: dict[str, bool],
                maze: list[list[Cell]]
            ) -> None:
        if self.real_path_finding:
            self.__pacman_real_direction(walls)
        else:
            self.__not_pacman_real_direction(walls, maze)

    def __not_pacman_real_direction(
                self,
                walls: dict[str, bool],
                maze: list[list[Cell]]
            ) -> None:
        # Frightened ghosts wander randomly, they do not follow a target
        if self.state == Ghost_state.FRIGHTENED:
            self.__pacman_real_direction(walls)
            return

        # Targets (Pinky, Inky...) can be outside of the maze: clamp them
        goal = (
            min(max(int(self.target[0]), 0), len(maze[0]) - 1),
            min(max(int(self.target[1]), 0), len(maze) - 1)
        )

        direction = next_direction(
            (int(self.pos_x), int(self.pos_y)),
            self.direction,
            goal,
            maze
        )

        if direction is None:
            # Goal unreachable (closed tile...): fall back on the greedy way
            self.__pacman_real_direction(walls)
        else:
            self.direction = direction

    def __pacman_real_direction(self, walls: dict[str, bool]) -> None:
        OPPOSITE: dict[str, str] = {
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

        if (OPPOSITE[self.direction] in possibles):
            possibles.remove(OPPOSITE[self.direction])

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
                entities: dict[str, Entity],
                maze: list[list[Cell]],
                elapsed_time: int
            ) -> None:

        cell = maze[int(self.pos_y)][int(self.pos_x)]
        if isinstance(entities["pacman"], Pac_man):
            self.__choose_state(entities["pacman"], elapsed_time)
        else:
            raise ValueError("There must be a pacman key in the entities")

        if (modf(self.pos_x)[0] == 0.5 and modf(self.pos_y)[0] == 0.5):

            if (not cell.special):
                self.define_target(entities)

            self.__choose_direction(cell.walls, maze)

        self.walk()
