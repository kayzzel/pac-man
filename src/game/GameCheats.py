from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Game import Game   # only imported by type checkers, not at runtime


class GameCheats:
    """The cheat panel: toggles and adjustments, clamped to sane bounds."""

    def __init__(self, game: Game) -> None:
        """
            Description:
        Create the cheat panel of a game, every cheat turned off.

            Parameters:
        game -> the game the cheats act on
        """
        self.__game = game
        self.__is_invincible = False
        self.__is_clipping = False

    @property
    def is_invincible(self) -> bool:
        """
            Description:
        Tell whether the invincible cheat is currently enabled, in
        which case touching a ghost eats it instead of costing a life.

            Returns value:
        return True when the cheat is enabled
        """
        return self.__is_invincible

    @property
    def is_clipping(self) -> bool:
        """
            Description:
        Tell whether the clipping cheat is currently enabled, in which
        case Pac-Man passes and turns through the walls, without
        ever leaving the map.

            Returns value:
        return True when the cheat is enabled
        """
        return self.__is_clipping

    def change_lives(self, lives: int) -> None:
        """
            Description:
        Add (or remove, with a negative value) lives to the player,
        never going below 1 life.

            Parameters:
        lives -> the number of lives to add, negative to remove
        """
        if self.__game.player.nb_lives + lives < 1:
            self.__game.player.nb_lives = 1
            return
        self.__game.player.nb_lives += lives

    def change_points(self, points: int) -> None:
        """
            Description:
        Add (or remove, with a negative value) points to the score,
        never going below 0 point.

            Parameters:
        points -> the number of points to add, negative to remove
        """
        if self.__game.player.score + points < 0:
            self.__game.player.score = 0
            return
        self.__game.player.score += points

    def toggle_invincible(self) -> None:
        """
            Description:
        Turn the invincible cheat on if it is off, and off if it is on.
        """
        self.__is_invincible = not self.__is_invincible

    def toggle_clipping(self) -> None:
        """
            Description:
        Turn the clipping cheat on if it is off, and off if it is on.
        """
        self.__is_clipping = not self.__is_clipping
