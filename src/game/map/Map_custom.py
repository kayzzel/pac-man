from .Map import Map
from .Map_storing import save_map_to_file
from ..entity.collectible.Collectible import Collectible
from ...utils.maze_utils import generate_empty_map, generate_walls
from ...utils.path_utils import next_direction

from pathlib import Path

import json


class Map_custom:
    def __init__(self, map_folder: Path) -> None:
        self.map_folder: Path = map_folder

        self.__rows: int = 15
        self.__cols: int = 15

        self.__map = Map()
        self.__map.cells = generate_empty_map(self.__cols, self.__rows)

        self.name_set: bool = False
        self.walls_set: bool = False
        self.pacman_spawn_set: bool = False
        self.collectibles_set: bool = False
        self.ghost_spawn_set: dict[str, bool] = {
                "BLINKY": False,
                "PINKY": False,
                "CLYDE": False,
                "INKY": False,
        }
        self.ghost_scatter_set: dict[str, bool] = {
                "BLINKY": False,
                "PINKY": False,
                "CLYDE": False,
                "INKY": False,
        }

    @property
    def map(self) -> Map:
        return self.__map

    @property
    def cols(self) -> int:
        return self.__cols

    @property
    def rows(self) -> int:
        return self.__rows

    def __reset(self) -> None:
        self.__map.cells = generate_empty_map(self.__cols, self.__rows)
        self.__map.collectible_count = 0
        self.walls_set = False
        self.pacman_spawn_set = False
        for key in self.ghost_spawn_set.keys():
            self.ghost_spawn_set[key] = False
        for key in self.ghost_scatter_set.keys():
            self.ghost_scatter_set[key] = False

    def set_cols(self, nbr: int) -> bool:
        if not isinstance(nbr, int) or nbr < 10 or nbr > 50:
            return False

        self.__cols = nbr
        self.__reset()
        return True

    def set_rows(self, nbr: int) -> bool:
        if not isinstance(nbr, int) or nbr < 10 or nbr > 50:
            return False

        self.__rows = nbr
        self.__reset()
        return True

    def __reset_collectibles(self) -> None:
        for row in self.__map.cells:
            for cell in row:
                cell.collectible = None
        self.collectibles_set = False
        self.__map.collectible_count = 0

    def set_name(self, name: str) -> bool:
        allowed: set[str] = set(
                "abcdefghijklmnopqrstuvwxyz"
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "0123456789_-"
            )

        if (
                not isinstance(name, str)
                or len(name) < 1
                or len(name) > 20
                or any(char not in allowed for char in name)
           ):
            return False

        if (self.map_folder / name).exists():
            return False

        self.__map.name = name
        self.name_set = True
        return True

    def randomize_wall(self) -> None:
        self.walls_set = False
        self.pacman_spawn_set = False
        for key in self.ghost_spawn_set.keys():
            self.ghost_spawn_set[key] = False
        for key in self.ghost_scatter_set.keys():
            self.ghost_scatter_set[key] = False
        self.__map.cells = generate_walls(self.__cols, self.__rows)

    def get_walls(self, x: int, y: int) -> dict[str, tuple[bool, bool]]:
        if y >= self.__rows or y < 0 or x >= self.__cols or x < 0:
            return {}

        cell = self.__map.cells[y][x]
        return {
                "N": (cell.walls["N"], y == 0),
                "S": (cell.walls["S"], y == self.__rows - 1),
                "E": (cell.walls["E"], x == self.__cols - 1),
                "W": (cell.walls["W"], x == 0),
        }

    def __toggle_opposite(self, x: int, y: int, wall: str) -> None:
        if wall == "N":
            if y != 0:
                cell = self.__map.cells[y - 1][x]
                cell.walls["S"] = not cell.walls["S"]
        elif wall == "S":
            if y != self.__rows - 1:
                cell = self.__map.cells[y + 1][x]
                cell.walls["N"] = not cell.walls["N"]
        elif wall == "E":
            if x != self.__cols - 1:
                cell = self.__map.cells[y][x + 1]
                cell.walls["W"] = not cell.walls["W"]
        elif wall == "W":
            if x != 0:
                cell = self.__map.cells[y][x - 1]
                cell.walls["E"] = not cell.walls["E"]

    def change_wall(self, x: int, y: int, wall: str) -> bool:
        if y >= self.__rows or y < 0 or x >= self.__cols or x < 0:
            return False

        if self.walls_set:
            self.walls_set = False
            self.__reset_collectibles()

        self.pacman_spawn_set = False
        for key in self.ghost_spawn_set.keys():
            self.ghost_spawn_set[key] = False
        for key in self.ghost_scatter_set.keys():
            self.ghost_scatter_set[key] = False

        cell = self.__map.cells[y][x]
        if wall == "N":
            if y != 0:
                cell.walls["N"] = not cell.walls["N"]
                self.__toggle_opposite(x, y, wall)
                return True
        elif wall == "S":
            if y != self.__rows - 1:
                cell.walls["S"] = not cell.walls["S"]
                self.__toggle_opposite(x, y, wall)
                return True
        elif wall == "E":
            if x != self.__cols - 1:
                cell.walls["E"] = not cell.walls["E"]
                self.__toggle_opposite(x, y, wall)
                return True
        elif wall == "W":
            if x != 0:
                cell.walls["W"] = not cell.walls["W"]
                self.__toggle_opposite(x, y, wall)
                return True

        return False

    def set_pacman_spawn(self, x: int, y: int) -> bool:
        if y >= self.__rows or y < 0 or x >= self.__cols or x < 0:
            return False

        if all(self.__map.cells[y][x].walls.values()):
            return False

        self.__reset_collectibles()
        for key in self.ghost_spawn_set.keys():
            self.ghost_spawn_set[key] = False
        for key in self.ghost_scatter_set.keys():
            self.ghost_scatter_set[key] = False

        self.__map.pacman_spawn = (x + 0.5, y + 0.5)

        self.walls_set = True
        self.pacman_spawn_set = True

        return True

    def set_collectible(self, x: int, y: int, item: Collectible) -> bool:
        if not self.walls_set or not self.pacman_spawn_set:
            return False

        if y >= self.__rows or y < 0 or x >= self.__cols or x < 0:
            return False

        if not any(
                    next_direction(
                        (x, y),
                        heading,
                        (
                            int(self.__map.pacman_spawn[0]),
                            int(self.__map.pacman_spawn[1])
                        ),
                        self.__map.cells
                    )
                    for heading in ("N", "S", "E", "W")
                ):
            return False

        if not self.__map.cells[y][x].collectible:
            self.__map.collectible_count += 1

        item.pos_x = x
        item.pos_y = y
        self.__map.cells[y][x].collectible = item

        return True

    def set_ghost_spawn(self, x: int, y: int, name: str) -> bool:
        if (
                not self.walls_set or
                not self.pacman_spawn_set or
                self.__map.collectible_count <= 0
                ):
            return False

        self.collectibles_set = True

        if y >= self.__rows or y < 0 or x >= self.__cols or x < 0:
            return False

        if all(self.__map.cells[y][x].walls.values()):
            return False

        if (x + 0.5, y + 0.5) == self.__map.pacman_spawn:
            return False

        if name not in self.ghost_spawn_set.keys():
            return False

        if not any(
                    next_direction(
                        (x, y),
                        heading,
                        (
                            int(self.__map.pacman_spawn[0]),
                            int(self.__map.pacman_spawn[1])
                        ),
                        self.__map.cells
                    )
                    for heading in ("N", "S", "E", "W")
                ):
            return False

        for key in self.ghost_scatter_set.keys():
            self.ghost_scatter_set[key] = False

        self.__map.ghosts_spawn[name] = (x + 0.5, y + 0.5)
        self.ghost_spawn_set[name] = True

        return True

    def set_ghost_scatter(self, x: int, y: int, name: str) -> bool:
        if (
                not self.walls_set or
                not self.pacman_spawn_set or
                not all(self.ghost_spawn_set.values())
                ):
            return False

        if y >= self.__rows or y < 0 or x >= self.__cols or x < 0:
            return False

        if name not in self.ghost_scatter_set.keys():
            return False

        self.__map.ghosts_scatter[name] = (x + 0.5, y + 0.5)
        self.ghost_scatter_set[name] = True

        return True

    def save_map(self) -> str | None:
        if not self.name_set:
            return "name is not set"
        if not self.walls_set:
            return "walls are not set"
        if not self.pacman_spawn_set:
            return "pacman spawn is not set"
        if not all(self.ghost_spawn_set.values()):
            return "ghost spawn is not set"
        if not all(self.ghost_scatter_set.values()):
            return "ghost scatter point is not set"
        if self.__map.collectible_count == 0:
            return "no collectibles in the map"

        folder: Path = self.map_folder / self.__map.name

        try:
            folder.mkdir(parents=True, exist_ok=True)
            save_map_to_file(self.__map, str(folder / "map.json"))

            score_file: Path = folder / "score.json"
            if not score_file.exists():
                with open(score_file, "w") as f:
                    json.dump([], f)
        except (OSError, ValueError) as err:
            return f"couldn't save the map: {err}"

        return None
