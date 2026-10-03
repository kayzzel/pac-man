from ...Game import Game

from abc import ABC, abstractmethod


class Collectible(ABC):
    def __init__(self, x: int, y: int, points: int) -> None:
        self.pos_x: int = x
        self.pos_y: int = y
        self.points = points

    def collected(self, game: Game) -> None:
        game.player.score += self.points

        current_map = game.map[game.map_index]
        current_map.collectible_count -= 1
        current_map.cells[self.pos_y][self.pos_x].collectible = None
