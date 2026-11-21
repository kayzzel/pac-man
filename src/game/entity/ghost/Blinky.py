from ..Entity import Entity
from .Ghost import Ghost


class Blinky(Ghost):
    """The red ghost: chases Pac-Man where he stands."""

    def __init__(self) -> None:
        """
            Description:
        Create Blinky, the ghost that never stops chasing.
        """
        super().__init__("blinky")

    def define_target(self, entities: dict[str, Entity]) -> int:
        """
            Description:
        Chase Pac-Man directly: the target is simply the tile he is on.

            Parameters:
        entities -> the entities of the game, needs a "pacman" key

            Returns value:
        return 1 when the target was set by the base class, 0 when
        Blinky computed his chasing target
        """
        if (super().define_target(entities)):
            return 0

        pacman = entities["pacman"]

        if self.target != (int(pacman.pos_x), int(pacman.pos_y)):
            self.target = (int(pacman.pos_x), int(pacman.pos_y))

        return 0
