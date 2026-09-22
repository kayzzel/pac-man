from ..Config import Config
from ..game.map.Map import Map
from ..game.map.Cell import Cell
from ..game.entity.collectible.Collectible import Collectible

def maze_center(height: int, width: int) -> tuple[int, int]:
    return (height // 2, width // 2)

def convert_maze_to_map(maze: list[list[int]], config: Config) -> Map:
    new_map: Map = Map()

    width = len(maze[0])
    height = len(maze)

    center = maze_center(height, width)

    def convert_nbr_to_cell(nbr: int) -> dict[str, bool]:
        return {
                "north": bool(nbr & 1),
                "east": bool(nbr & 2),
                "south": bool(nbr & 4),
                "west": bool(nbr & 8),
        }

    for y in range(height):
        for x in range(width):
            cell = Cell(x, y)
            cell.walls = convert_nbr_to_cell(maze[y][x])

            if ((x == 0 or x == width - 1) and (y == 0 or y == height - 1)):
                cell.collectible = Collectible(
                        "super_pacgum", config.point_per_super_pacgum
                    )
            elif (center[0] == y and center[1] == x):
                cell.collectible = Collectible(
                        "pacgum", config.point_per_pacgum
                    )

            new_map.cells.append(cell)
    new_map.collectible_count = width * height - 1
            
    return new_map


