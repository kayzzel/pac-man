from .Entity import Entity
from ..map.Cell import Cell
from ...Config import Config
from .collectible.Collectible import Collectible

from math import modf


class Pac_man(Entity):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.score = 0
        self.next_direciton: str = ""
        self.nb_lives = config.lives
        self.collectible: list[None | Collectible] = []
        self.is_powered: bool = False
        self.__last_super_pacgum_time: int = -1

    def __select_next_dir(self, cell: Cell) -> None:
        if not self.next_direciton:
            return

        if self.next_direciton == self.direction:
            return

        if not cell.walls[self.next_direciton]:
            self.direction = self.next_direciton
            self.next_direciton = ""

    def set_powered(self, timer: int):
        self.__last_super_pacgum_time = timer
        self.is_powered = True

    def update(
            self,
            cell: Cell,
            timer: int
        ) -> None:
        if self.is_powered:
            if timer >= self.__last_super_pacgum_time + 7:
                self.is_powered = False

        if (modf(self.pos_x)[0] == 0.5 and modf(self.pos_y)[0] == 0.5):

            self.__select_next_dir(cell)

            if cell.walls[self.direction]:
                return

        self.walk()
