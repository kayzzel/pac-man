from enum import Enum


class Game_state(str, Enum):
    NOT_RUNNING = "not_running"
    RUNNING = "running"
    PAUSED = "paused"
    DIED = "died"
    FINISHED_MAP = "finished_map"
    WON = "won"
    LOST = "lost"


class Ghost_state(Enum):
    CHASE = "chase"
    EATEN = "eaten"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"


class Consumable_type(str, Enum):
    CHERRY = "cherry"
    STRAWBERRY = "strawberry"
    ORANGE = "orange"
    APPLE = "apple"
    MELON = "melon"
    GALAXIAN = "galaxian"
    BELL = "bell"
    KEY = "key"
