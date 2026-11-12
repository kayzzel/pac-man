from ..Entity import Entity
from .Ghost import Ghost


class Inky(Ghost):
    """The cyan ghost: unpredictable, aims through Blinky."""

    def __init__(self) -> None:
        """
            Description:
        Create Inky, the ghost whose target depends on Blinky.
        """
        super().__init__("inky")

    def define_target(self, entities: dict[str, Entity]) -> int:
        """
            Description:
        Take the tile 2 in front of Pac-Man, and mirror it through
        Blinky: the target is as far beyond Blinky as that tile, which
        makes Inky's approach hard to predict.

            Parameters:
        entities -> the entities of the game, needs a "pacman" and a
                    "blinky" key

            Returns value:
        return 1 when the target was set by the base class, 0 when
        Inky computed his mirrored target
        """
        if super().define_target(entities):
            return 0

        VECTORS: dict[str, tuple[int, int]] = {
                "N": (-2, -2),
                "S": (0, 2),
                "E": (2, 0),
                "W": (-2, 0)
        }

        pacman = entities["pacman"]
        blinky = entities["blinky"]
        vector = VECTORS[pacman.direction]

        central_x = int(pacman.pos_x) + vector[0]
        central_y = int(pacman.pos_y) + vector[1]

        if self.target != (
            2 * central_x - int(blinky.pos_x),
            2 * central_y - int(blinky.pos_y),
                ):
            self.target = (
                2 * central_x - int(blinky.pos_x),
                2 * central_y - int(blinky.pos_y),
            )

        return 0
