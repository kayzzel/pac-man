from .Ghost import Ghost
from ..Entity import Entity


class Clyde(Ghost):
    """The orange ghost: chases when far, retreats when close."""

    def __init__(self) -> None:
        """
            Description:
        Create Clyde, the shy ghost of the group.
        """
        super().__init__("clyde")

    def define_target(self, entities: dict[str, Entity]) -> int:
        """
            Description:
        Chase Pac-Man while he is more than 8 tiles away, and head
        back to his scatter corner as soon as he comes closer.

            Parameters:
        entities -> the entities of the game, needs a "pacman" key

            Returns value:
        return 1 when the target was set by the base class, 0 when
        Clyde computed his moody target
        """
        if (super().define_target(entities)):
            return 0

        pacman = entities["pacman"]

        distance = (
            abs(int(self.pos_x) - int(pacman.pos_x))
            + abs(int(self.pos_y) - int(pacman.pos_y))
        )
        if distance > 8:
            if self.target != (int(pacman.pos_x), int(pacman.pos_y)):
                self.target = (int(pacman.pos_x), int(pacman.pos_y))

        else:
            self.target = (
                        int(self.scatter_point[0]),
                        int(self.scatter_point[1])
                   )

        return 0
