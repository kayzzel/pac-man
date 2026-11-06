from .Entity import Entity
from .collectible.Collectible import Collectible
from ..map.Cell import Cell
from ...Config import Config
from ...utils.enum_utils import Pacman_state

from math import modf


class Pac_man(Entity):
    def __init__(self, config: Config) -> None:
        super().__init__("pacman")
        self.score = 0
        self.__next_direction: str = ""
        self.nb_lives = config.lives
        self.collectible: list[None | Collectible] = []
        self.is_energized: Pacman_state = Pacman_state.NORMAL
        self.__last_super_pacgum_time: int = -1

    def set_next_direction(self, direction: str) -> None:
        if direction not in ["N", "S", "W", "E"]:
            return

        self.__next_direction = direction

    def __select_next_dir(
            self,
            cell: Cell,
            is_clipping: bool,
            map_size: tuple[int, int]
    ) -> None:
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

    def test_update(self, cell: Cell) -> None:

        self.__select_next_dir(cell)
        for _ in range(50):
            self.walk()

    def set_energized(self, elapsed_time: int) -> None:
        self.__last_super_pacgum_time = elapsed_time
        self.is_energized = Pacman_state.ENERGIZED

    def update(
                self,
                cell: Cell,
                elapsed_time: int,
                is_clipping: bool,
                map_size: tuple[int, int]
            ) -> None:
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
