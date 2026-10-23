from .Map import Map
from .Cell import Cell
from ..entity.collectible.Pacgum import Pacgum
from ..entity.collectible.Super_Pacgum import Super_Pacgum
from ..entity.collectible.Consumable import Consumable
from ...utils.enum_utils import Consumable_type
from ...utils.json_utils import get_json_from_file

from pydantic import (
        BaseModel,
        Field,
        ValidationError,
        field_validator,
        model_validator
    )

import json


class Collectible_info(BaseModel):
    name: str
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    points: int = Field(ge=0)

    @field_validator("name", mode="before")
    @classmethod
    def check_name(cls, value: object) -> str:
        if isinstance(value, Consumable_type):
            return value.value
        if not isinstance(value, str):
            raise ValueError("collectible name must be a string")
        if value in ("pacgum", "super_pacgum"):
            return value
        try:
            Consumable_type(value)
        except ValueError:
            raise ValueError(f"unknown collectible name: {value!r}") from None
        return value


class Cell_info(BaseModel):
    pos_x: int = Field(ge=0)
    pos_y: int = Field(ge=0)
    walls: dict[str, bool]
    special: bool = False
    collectible: Collectible_info | None = None

    @model_validator(mode="after")
    def check(self) -> "Cell_info":
        if set(self.walls.keys()) != {"N", "S", "E", "W"}:
            raise ValueError("walls must have exactly the N, S, E, W keys")

        if (
                self.collectible is not None
                and (self.collectible.x != self.pos_x
                     or self.collectible.y != self.pos_y)
           ):
            raise ValueError(
                    "a collectible must be on its own cell "
                    f"({self.pos_x}, {self.pos_y})"
                )
        return self


class Map_info(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    cells: list[list[Cell_info]]
    real_path_finding: bool = False
    collectible_count: int = Field(ge=0)
    pacman_spawn: tuple[float, float]
    ghosts_spawn: dict[str, tuple[float, float]]
    ghosts_scatter: dict[str, tuple[float, float]]

    @model_validator(mode="after")
    def check(self) -> "Map_info":
        GHOSTS: set[str] = {"BLINKY", "PINKY", "CLYDE", "INKY"}

        if len(self.cells) < 10 or len(self.cells[0]) < 10:
            raise ValueError("a map must be at least 10x10")

        if len(self.cells) > 50 or len(self.cells[0]) > 50:
            raise ValueError("a map must be at most 50x50")

        width: int = len(self.cells[0])
        height: int = len(self.cells)
        for row in self.cells:
            if len(row) != width:
                raise ValueError("the map grid must be rectangular")

        if set(self.ghosts_spawn.keys()) != GHOSTS:
            raise ValueError("ghosts_spawn must have the 4 ghost names")
        if set(self.ghosts_scatter.keys()) != GHOSTS:
            raise ValueError("ghosts_scatter must have the 4 ghost names")

        def inside(pos: tuple[float, float]) -> bool:
            return 0 <= int(pos[0]) < width and 0 <= int(pos[1]) < height

        def walkable(what: str, pos: tuple[float, float]) -> None:
            if not inside(pos):
                raise ValueError(f"{what} {pos} is outside of the map")
            if all(self.cells[int(pos[1])][int(pos[0])].walls.values()):
                raise ValueError(f"{what} {pos} is on a closed cell")

        walkable("pacman_spawn", self.pacman_spawn)
        for name, pos in self.ghosts_spawn.items():
            walkable(f"ghosts_spawn[{name}]", pos)
        for name, pos in self.ghosts_scatter.items():
            if not inside(pos):
                raise ValueError(
                        f"ghosts_scatter[{name}] {pos} is outside of the map"
                    )

        count: int = sum(
                1 for row in self.cells for cell in row if cell.collectible
            )
        if count != self.collectible_count:
            raise ValueError(
                    f"collectible_count is {self.collectible_count} "
                    f"but the map holds {count} collectibles"
                )

        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if (
                        y > 0
                        and cell.walls["N"] != self.cells[y - 1][x].walls["S"]
                   ):
                    raise ValueError(
                            f"north wall of ({x}, {y}) disagrees with the "
                            "south wall of the cell above"
                        )
                if x > 0 and cell.walls["W"] != row[x - 1].walls["E"]:
                    raise ValueError(
                            f"west wall of ({x}, {y}) disagrees with the "
                            "east wall of the cell on its left"
                        )

        return self


def map_to_info(m: Map) -> Map_info:
    cells: list[list[Cell_info]] = []

    for row in m.cells:
        cells_row: list[Cell_info] = []
        for cell in row:
            collectible: Collectible_info | None = None
            if cell.collectible is not None:
                collectible = Collectible_info(
                        name=cell.collectible.name,
                        x=cell.collectible.pos_x,
                        y=cell.collectible.pos_y,
                        points=cell.collectible.points
                    )
            cells_row.append(
                    Cell_info(
                        pos_x=cell.pos_x,
                        pos_y=cell.pos_y,
                        walls=cell.walls,
                        special=cell.special,
                        collectible=collectible
                    )
                )
        cells.append(cells_row)

    return Map_info(
            name=m.name,
            cells=cells,
            real_path_finding=m.real_path_finding,
            collectible_count=m.collectible_count,
            pacman_spawn=m.pacman_spawn,
            ghosts_spawn=m.ghosts_spawn,
            ghosts_scatter=m.ghosts_scatter
        )


def info_to_map(info: Map_info) -> Map:
    m: Map = Map()

    for row in info.cells:
        cells_row: list[Cell] = []
        for cell_info in row:
            cell = Cell(cell_info.pos_x, cell_info.pos_y)
            cell.walls = cell_info.walls
            cell.special = cell_info.special

            col = cell_info.collectible
            if col is not None:
                if col.name == "pacgum":
                    cell.collectible = Pacgum(col.x, col.y, col.points)
                elif col.name == "super_pacgum":
                    cell.collectible = Super_Pacgum(col.x, col.y, col.points)
                else:
                    cell.collectible = Consumable(
                            Consumable_type(col.name),
                            col.x,
                            col.y,
                            col.points
                        )

            cells_row.append(cell)
        m.cells.append(cells_row)

    m.name = info.name
    m.real_path_finding = info.real_path_finding
    m.collectible_count = info.collectible_count
    m.pacman_spawn = info.pacman_spawn
    m.ghosts_spawn = info.ghosts_spawn
    m.ghosts_scatter = info.ghosts_scatter

    return m


def save_map_to_file(m: Map, filename: str) -> None:
    info = map_to_info(m)

    try:
        with open(filename, "w") as f:
            json.dump(info.model_dump(), f, indent=4)
    except OSError as err:
        raise ValueError(
                f"ERROR: couldn't write the map file {filename}: {err}"
            ) from err


def load_map_from_file(filename: str) -> Map:
    data = get_json_from_file(filename)

    try:
        info = Map_info.model_validate(data)
    except ValidationError as err:
        raise ValueError(
                f"ERROR: invalid map file {filename}: {err}"
            ) from err

    return info_to_map(info)
