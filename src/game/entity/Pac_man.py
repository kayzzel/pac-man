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

    def __select_next_dir(self, cell: Cell) -> None:
        if not self.__next_direction:
            return

        if self.__next_direction == self.direction:
            return

        if not cell.walls[self.__next_direction]:
            self.direction = self.__next_direction
            self.__next_direction = ""

    def set_energized(self, elapsed_time: int) -> None:
        self.__last_super_pacgum_time = elapsed_time
        self.is_energized = Pacman_state.ENERGIZED

    def update(
                self,
                cell: Cell,
                elapsed_time: int
            ) -> None:
        if self.is_energized != Pacman_state.NORMAL:
            if (
                    elapsed_time >= self.__last_super_pacgum_time + 4 and
                    self.is_energized != Pacman_state.ENERGIZED_END
            ):
                self.is_energized = Pacman_state.ENERGIZED_END
            elif elapsed_time >= self.__last_super_pacgum_time + 7:
                self.is_energized = Pacman_state.NORMAL

        if (modf(self.pos_x)[0] == 0.5 and modf(self.pos_y)[0] == 0.5):

            self.__select_next_dir(cell)

            if cell.walls[self.direction]:
                return

        self.walk()
