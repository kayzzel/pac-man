from ..Entity import Entity
from ..Pac_man import Pac_man
from ...map.Cell import Cell
from ....utils.enum_utils import Ghost_state, Pacman_state
from ....utils.path_utils import next_direction

from abc import ABC, abstractmethod
from random import choice
from math import modf


class Ghost(Entity, ABC):
    """Base of the four ghosts: state machine, target and movement."""

    def __init__(self, name: str) -> None:
        """
            Description:
        Create a ghost in CHASE, with its target and points at the
        origin, that can still be eaten during a power-up.

            Parameters:
        name -> name of the ghost, used to identify it
        """
        super().__init__(name)
        self.state: Ghost_state = Ghost_state.CHASE
        self.target: tuple[int, int] = (0, 0)
        self.spawn_point: tuple[float, float] = (0, 0)
        self.scatter_point: tuple[float, float] = (0, 0)
        self.real_path_finding = False
        self.eaten_this_power = False

    @abstractmethod
    def define_target(self, entities: dict[str, Entity]) -> int:
        """
            Description:
        Update the target tile of the ghost according to its
        personality (each ghost defines its own). The ghost targets
        its spawn when EATEN, its scatter corner when SCATTER, and
        keeps its current target when FRIGHTENED.

            Parameters:
        entities -> the entities of the game, needs a "pacman" key

            Returns value:
        return 1 when the target was set here, 0 when the subclass
        must compute its own chasing target
        """
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
        """
            Description:
        Eat the ghost: it becomes a pair of eyes, can no longer be
        eaten during this power-up and moves twice as fast until it
        comes back to its spawn.
        """
        if self.state != Ghost_state.EATEN:
            self.state = Ghost_state.EATEN
            self.eaten_this_power = True
            self.speed *= 2

    def __respawned(self) -> None:
        """
            Description:
        Give the ghost its normal speed back, once it comes back to
        its spawn as a pair of eyes.
        """
        self.speed /= 2

    def __choose_state(self, pacman: Pac_man, elapsed_time: int) -> None:
        """
            Description:
        Move the ghost from state to state: a respawned ghost leaves
        EATEN, an energized Pac-Man turns every not yet eaten ghost
        into FRIGHTENED (making it turn back), and otherwise the
        ghost follows the alternating chase/scatter schedule,
        turning back every time its state changes.

            Parameters:
        pacman -> Pac-Man, driving the frightened and eaten states
        elapsed_time -> the current elapsed time of the game, in
                        seconds
        """
        OPPOSITE: dict[str, str] = {
                "N": "S",
                "S": "N",
                "E": "W",
                "W": "E"
        }

        # A ghost can only be eaten once per power-up
        if pacman.is_energized == Pacman_state.NORMAL:
            self.eaten_this_power = False

        if self.state == Ghost_state.EATEN:
            if (self.pos_x, self.pos_y) != self.spawn_point:
                return
            else:
                self.__respawned()

        if (
                pacman.is_energized != Pacman_state.NORMAL and
                not self.eaten_this_power
        ):
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
        """
            Description:
        Give the state the schedule wants at the given time: the
        ghosts alternate between regrouping at their corners and
        chasing Pac-Man, and chase for good after the last window.

            Parameters:
        elapsed_time -> the current elapsed time of the game, in
                        seconds

            Returns value:
        return the scheduled state, SCATTER or CHASE
        """
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
        """
            Description:
        Pick how the ghost chooses its direction: the A* path finding
        when the map allows it, the honest greedy way otherwise.

            Parameters:
        walls -> the walls of the cell the ghost is on
        maze -> the grid of Cells, indexed maze[y][x]
        """
        if self.real_path_finding:
            self.__pacman_real_direction(walls)
        else:
            self.__not_pacman_real_direction(walls, maze)

    def __not_pacman_real_direction(
                self,
                walls: dict[str, bool],
                maze: list[list[Cell]]
            ) -> None:
        """
            Description:
        Choose the direction with the A* path finding, able to follow
        the real rules of Pac-Man: no turning back, and a goal
        reached only on a legal path. Frightened ghosts just wander,
        and an unreachable goal falls back on the greedy way.

            Parameters:
        walls -> the walls of the cell the ghost is on
        maze -> the grid of Cells, indexed maze[y][x]
        """
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
        """
            Description:
        Choose the direction like the honest Pac-Man ghosts: an
        available direction closest to the target, never turning back
        unless it is the only way out. Frightened ghosts pick one at
        random instead.

            Parameters:
        walls -> the walls of the cell the ghost is on
        """
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
        """
            Description:
        Advance the ghost for one tick: update its state, then when it
        is exactly on the center of a cell, recompute its target and
        choose a direction, and finally walk one step.

            Parameters:
        entities -> the entities of the game, needs a "pacman" key
        maze -> the grid of Cells, indexed maze[y][x]
        elapsed_time -> the current elapsed time of the game, in
                        seconds
        """
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
