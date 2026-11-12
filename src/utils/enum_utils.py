from enum import Enum


class Game_state(str, Enum):
    """Every state of a game, shown to the GUI at each pause."""
    NOT_RUNNING = "not_running"
    RUNNING = "running"
    PAUSED = "paused"
    DIED = "died"
    FINISHED_MAP = "finished_map"
    WON = "won"
    LOST = "lost"
    ERROR = "error"


class Pacman_state(Enum):
    """Pac-Man's power-up state, NORMAL means no power-up left."""
    NORMAL = "normal"
    ENERGIZED = "energized"
    ENERGIZED_END = "energized_end"


class Ghost_state(Enum):
    """The states of a ghost, driving its movement and edibility."""
    CHASE = "chase"
    EATEN = "eaten"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"


class Consumable_type(str, Enum):
    """The bonus fruits a Consumable collectible can give."""
    CHERRY = "cherry"
    STRAWBERRY = "strawberry"
    ORANGE = "orange"
    APPLE = "apple"
    MELON = "melon"
    GALAXIAN = "galaxian"
    BELL = "bell"
    KEY = "key"
