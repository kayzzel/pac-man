from .Entity import Entity
from .collectible.Collectible import Collectible
from ..map.Cell import Cell
from ...Config import Config
from ...utils.enum_utils import Pacman_state

from math import modf


class Pac_man(Entity):
    """The player: score, lives, the queued turn and the power-up."""

    def __init__(self, config: Config) -> None:
        """
            Description:
        Create Pac-Man with the lives of the config, no score, no
        queued turn and no power-up.

            Parameters:
        config -> the loaded config of the game
        """
        super().__init__("pacman")
        self.score = 0
        self.__next_direction: str = ""
        self.nb_lives = config.lives
        self.collectible: list[None | Collectible] = []
        self.is_energized: Pacman_state = Pacman_state.NORMAL
        self.__last_super_pacgum_time: int = -1

    def set_next_direction(self, direction: str) -> None:
        """
            Description:
        Queue the next turn of Pac-Man. It is applied when he comes to
        the center of a cell where this direction is not blocked. Any
        other value than N, S, W or E is ignored.

            Parameters:
        direction -> the wanted next direction (N, S, W or E)
        """
        if direction not in ["N", "S", "W", "E"]:
            return

        self.__next_direction = direction

    def __select_next_dir(
            self,
            cell: Cell,
            is_clipping: bool,
            map_size: tuple[int, int]
    ) -> None:
        """
            Description:
        Apply the queued turn if the new direction is open, or if the
        clipping cheat allows going through it. While clipping, a
        turn towards the border of the map is refused, so Pac-Man
        can never turn his way outside of the grid.

            Parameters:
        cell -> the cell Pac-Man is on
        is_clipping -> True when the clipping cheat is enabled
        map_size -> (width, height) of the grid, in cells
        """
        if not self.__next_direction:
            return

        if self.__next_direction == self.direction:
            return

        x = int(self.pos_x)
        y = int(self.pos_y)

        can_clip = is_clipping and (
            (self.__next_direction == "N" and y != 0) or
            (self.__next_direction == "S" and y != map_size[1] - 1) or
            (self.__next_direction == "W" and x != 0) or
            (self.__next_direction == "E" and x != map_size[0] - 1)
        )

        if not cell.walls[self.__next_direction] or can_clip:
            self.direction = self.__next_direction
            self.__next_direction = ""

    def set_energized(self, elapsed_time: int) -> None:
        """
            Description:
        Start the power-up: the ghosts become edible, blink during
        the last seconds (ENERGIZED_END) and stop being edible 7
        seconds after this call.

            Parameters:
        elapsed_time -> the current elapsed time of the game, in
                       seconds
        """
        self.__last_super_pacgum_time = elapsed_time
        self.is_energized = Pacman_state.ENERGIZED

    def update(
                self,
                cell: Cell,
                elapsed_time: int,
                is_clipping: bool,
                map_size: tuple[int, int]
            ) -> None:
        """
            Description:
        Advance Pac-Man for one tick: expire the power-up when its
        time is up, then, when he is exactly on the center of a cell,
        apply the queued turn if possible, refuse to move into a wall
        (unless the clipping cheat lets him pass), and finally walk
        one step.

            Parameters:
        cell -> the cell Pac-Man is currently on
        elapsed_time -> the current elapsed time of the game, in
                        seconds
        is_clipping -> True when the clipping cheat is enabled
        map_size -> (width, height) of the grid, in cells
        """
        if self.is_energized != Pacman_state.NORMAL:
            if (
                    self.is_energized != Pacman_state.ENERGIZED_END and
                    elapsed_time >= self.__last_super_pacgum_time + 4
            ):
                self.is_energized = Pacman_state.ENERGIZED_END
            if elapsed_time >= self.__last_super_pacgum_time + 7:
                self.is_energized = Pacman_state.NORMAL

        if (modf(self.pos_x)[0] == 0.5 and modf(self.pos_y)[0] == 0.5):

            self.__select_next_dir(cell, is_clipping, map_size)

            x = int(self.pos_x)
            y = int(self.pos_y)

            can_clip = is_clipping and (
                (self.direction == "N" and y != 0) or
                (self.direction == "S" and y != map_size[1] - 1) or
                (self.direction == "W" and x != 0) or
                (self.direction == "E" and x != map_size[0] - 1)
            )

            if (not can_clip and cell.walls[self.direction]):
                return

        self.walk()
