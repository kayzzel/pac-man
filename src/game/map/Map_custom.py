from .Map import Map
from .Map_storing import save_map_to_file
from ..entity.collectible.Collectible import Collectible
from ...utils.maze_utils import generate_empty_map, generate_walls
from ...utils.path_utils import next_direction

from sys import stderr
from pathlib import Path

import json


class Map_custom:
    """The map creator: builds, edits and saves one custom map."""

    def __init__(self, map_folder: Path) -> None:
        """
            Description:
        Create an empty editor on a blank empty map of the default
        size, with every step of the creation still to be done.

            Parameters:
        map_folder -> the folder where every custom map is saved
        """
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
        """
            Description:
        Give the map being edited, for the editor to render it.

            Returns value:
        return the map under construction
        """
        return self.__map

    @property
    def cols(self) -> int:
        """
            Description:
        Give the current width of the map being edited.

            Returns value:
        return the number of columns
        """
        return self.__cols

    @property
    def rows(self) -> int:
        """
            Description:
        Give the current height of the map being edited.

            Returns value:
        return the number of rows
        """
        return self.__rows

    def __reset(self) -> None:
        """
            Description:
        Start over on a blank empty map of the current size: called
        when the size changes, since every wall, spawn and ghost
            placement was made for the old size.
        """
        self.__map.cells = generate_empty_map(self.__cols, self.__rows)
        self.__map.collectible_count = 0
        self.walls_set = False
        self.pacman_spawn_set = False
        for key in self.ghost_spawn_set.keys():
            self.ghost_spawn_set[key] = False
        for key in self.ghost_scatter_set.keys():
            self.ghost_scatter_set[key] = False

    def set_cols(self, nbr: int) -> bool:
        """
            Description:
        Set the width of the map, between 10 and 50, and restart on
        a blank map of the new size.

            Parameters:
        nbr -> the wanted number of columns

            Returns value:
        return True when the width was accepted
        """
        if not isinstance(nbr, int) or nbr < 10 or nbr > 50:
            return False

        self.__cols = nbr
        self.__reset()
        return True

    def set_rows(self, nbr: int) -> bool:
        """
            Description:
        Set the height of the map, between 10 and 50, and restart
        on a blank map of the new size.

            Parameters:
        nbr -> the wanted number of rows

            Returns value:
        return True when the height was accepted
        """
        if not isinstance(nbr, int) or nbr < 10 or nbr > 50:
            return False

        self.__rows = nbr
        self.__reset()
        return True

    def __reset_collectibles(self) -> None:
        """
            Description:
        Remove every collectible from the map: their reachability
        from Pac-Man only holds while the spawns and the walls
        stand, so they are placed again after any such change.
        """
        for row in self.__map.cells:
            for cell in row:
                cell.collectible = None
        self.collectibles_set = False
        self.__map.collectible_count = 0

    def set_name(self, name: str) -> bool:
        """
            Description:
        Name the map: 1 to 20 characters among letters, digits, _
        and -, a name that no existing map folder already uses, so
        every map keeps its own folder and its own scores.

            Parameters:
        name -> the wanted name of the map

            Returns value:
        return True when the name was accepted
        """
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
        """
            Description:
        Fill the map with a random maze: the spawns and the collectibles
        made for the old walls are reset, and a failure of the
        generator keeps the current walls untouched.
        """
        try:
            cells = generate_walls(self.__cols, self.__rows)
        except ValueError as err:
            print(err, file=stderr)
            return

        self.walls_set = False
        self.pacman_spawn_set = False
        for key in self.ghost_spawn_set.keys():
            self.ghost_spawn_set[key] = False
        for key in self.ghost_scatter_set.keys():
            self.ghost_scatter_set[key] = False
        self.__map.cells = cells

    def get_walls(self, x: int, y: int) -> dict[str, tuple[bool, bool]]:
        """
            Description:
        Give the four walls of one cell for the editor: each wall as
        a pair (present, on the border of the map), so the editor can
        refuse to remove the border.

            Parameters:
        x -> column of the cell
        y -> row of the cell

            Returns value:
        return the N, S, E, W walls of the cell, or an empty dict
        when the coordinates are outside of the map
        """
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
        """
            Description:
        Toggle the same wall on the other side: a wall always belongs
        to both of the cells it separates, so the saved map stays
        coherent and the ghosts never face a one-way wall.

            Parameters:
        x -> column of the cell
        y -> row of the cell
        wall -> the wall just toggled (N, S, E or W)
        """
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
        """
            Description:
        Toggle one wall of one cell, with the wall of the neighbour
        on the other side: the border of the map cannot be pierced,
        and once the walls were locked in, changing one resets the
        collectibles and the spawns placed for the old walls.

            Parameters:
        x -> column of the cell
        y -> row of the cell
        wall -> the wall to toggle (N, S, E or W)

            Returns value:
        return True when the wall was toggled, False on a border
            wall or invalid coordinates
        """
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
        """
            Description:
        Place the spawn of Pac-Man on a walkable cell: since the
        reachability of everything else is measured from it, the
        collectibles and the ghost placements are reset.

            Parameters:
        x -> column of the spawn
        y -> row of the spawn

            Returns value:
        return True when the spawn was placed, False on a closed
        cell or invalid coordinates
        """
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
        """
            Description:
        Place a collectible on a cell that Pac-Man can really reach
        from his spawn, with one of the four starting directions: a
        collectible out of reach would make the level impossible to
        clear. The item is placed exactly on the given cell.

            Parameters:
        x -> column of the cell
        y -> row of the cell
        item -> the collectible to place

            Returns value:
        return True when the collectible was placed, False before
        the spawns are locked in, outside of the map, or on an
        unreachable cell
        """
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
        """
            Description:
        Place the spawn of one ghost on a walkable cell, different
        from Pac-Man's spawn, that can really reach Pac-Man with one
        of the four starting directions: a sealed ghost would trap it
        for ever.

            Parameters:
        x -> column of the spawn
        y -> row of the spawn
        name -> the ghost this spawn belongs to

            Returns value:
        return True when the spawn was placed, False before the
        collectibles exist, on a closed cell, on Pac-Man's spawn,
        for an unknown ghost, or on an unreachable cell
        """
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
        """
            Description:
        Place the scatter corner of one ghost, once the four spawns
        are placed: a corner stays inside the map, reachable or not,
        like the generated maps that use the corners.

            Parameters:
        x -> column of the corner
        y -> row of the corner
        name -> the ghost this corner belongs to

            Returns value:
        return True when the corner was placed, False before the
        spawns are placed, outside of the map, or for an unknown
        ghost
        """
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
        """
            Description:
        Save the finished map in its own folder, as a map.json file
        validated by Map_info, with an empty score.json next to it
        unless the map already has scores to keep.

            Returns value:
        return None on success, or the reason why the map cannot be
        saved (a missing step, an unwritable folder)
        """
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
