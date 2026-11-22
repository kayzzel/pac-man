from ..Entity import Entity
from .Ghost import Ghost


class Pinky(Ghost):
    """The pink ghost: ambushes 4 tiles ahead of Pac-Man."""

    def __init__(self) -> None:
        """
            Description:
        Create Pinky, the ghost that aims in front of Pac-Man.
        """
        super().__init__("pinky")

    def define_target(self, entities: dict[str, Entity]) -> int:
        """
            Description:
        Aim 4 tiles in front of Pac-Man, in the direction he is going
        to, to cut him off: the faithful ambush of the original
        Pinky (including her famous upward overshoot).

            Parameters:
        entities -> the entities of the game, needs a "pacman" key

            Returns value:
        return 1 when the target was set by the base class, 0 when
        Pinky computed her ambushing target
        """
        if (super().define_target(entities)):
            return 0

        VECTORS: dict[str, tuple[int, int]] = {
                "N": (-4, -4),
                "S": (0, 4),
                "E": (4, 0),
                "W": (-4, 0)
        }

        pacman = entities["pacman"]
        vector = VECTORS[pacman.direction]

        if self.target != (
            int(pacman.pos_x) + vector[0],
            int(pacman.pos_y) + vector[1]
                ):
            self.target = (
                int(pacman.pos_x) + vector[0],
                int(pacman.pos_y) + vector[1]
            )

        return 0
