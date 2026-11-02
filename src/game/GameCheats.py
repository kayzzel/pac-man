from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Game import Game   # only imported by type checkers, not at runtime


class GameCheats:
    def __init__(self, game: Game) -> None:
        self.__game = game
        self.__is_invincible = False
        self.__is_clipping = False

    @property
    def is_invincible(self) -> bool:
        return self.__is_invincible

    @property
    def is_clipping(self) -> bool:
        return self.__is_clipping

    def add_live(self) -> None:
        self.__game.player.nb_lives += 1

    def remove_live(self) -> None:
        if self.__game.player.nb_lives > 1:
            self.__game.player.nb_lives -= 1

    def add_points(self, points: int) -> None:
        if points < 0:
            return
        self.__game.player.score += points

    def remove_points(self, points: int) -> None:
        if points < 0:
            return

        if self.__game.player.score - points < 0:
            self.__game.player.score = 0
            return

        self.__game.player.score -= points

    def toggle_invincible(self) -> None:
        self.__is_invincible = not self.__is_invincible

    def toggle_clipping(self) -> None:
        self.__is_clipping = not self.__is_clipping
