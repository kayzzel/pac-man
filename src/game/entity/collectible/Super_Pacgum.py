
from .Collectible import Collectible
from ...Game import Game


class Super_Pacgum(Collectible):
    def __init__(self, x: int, y: int, points: int) -> None:
        super().__init__(x, y, points)

    def collected(self, game: Game) -> None:
        super().collected(game)

        game.player.set_energized(int(game.game_loop.elapsed_time))
