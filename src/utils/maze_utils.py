from ..Config import Config
from ..game.map.Map import Map
from ..game.map.Cell import Cell
from ..game.entity.collectible.Collectible import Collectible


def find_spawn_position(maze: list[list[int]]) -> tuple[int, int]:
    height = len(maze)
    width = len(maze[0])

    center_y = height // 2
    center_x = width // 2

    max_dist = max(center_x, center_y,
                   width - 1 - center_x, height - 1 - center_y)

    for dist in range(max_dist + 1):
        for dy in range(-dist, dist + 1):
            for dx in range(-dist, dist + 1):
                if abs(dx) + abs(dy) != dist:
                    continue
                x = center_x + dx
                y = center_y + dy
                if 0 <= x < width and 0 <= y < height and maze[y][x] != 15:
                    return (x, y)

    raise ValueError("No walkable spawn position found")


def convert_maze_to_map(maze: list[list[int]], config: Config) -> Map:
    new_map: Map = Map()

    width = len(maze[0])
    height = len(maze)

    spawn_x, spawn_y = find_spawn_position(maze)
    new_map.spawn = (spawn_x, spawn_y)

    def convert_nbr_to_cell(nbr: int) -> dict[str, bool]:
        return {
                "north": bool(nbr & 1),
                "east": bool(nbr & 2),
                "south": bool(nbr & 4),
                "west": bool(nbr & 8),
        }

    def is_corner(x: int, y: int) -> bool:
        return (x == 0 or x == width - 1) and (y == 0 or y == height - 1)

    for y in range(height):
        for x in range(width):
            cell = Cell(x, y)
            cell.walls = convert_nbr_to_cell(maze[y][x])

            if maze[y][x] != 15 and (x, y) != (spawn_x, spawn_y):
                if is_corner(x, y):
                    cell.collectible = Collectible(
                            "super_pacgum",
                            config.point_per_super_pacgum,
                        )
                else:
                    cell.collectible = Collectible(
                            "pacgum",
                            config.point_per_pacgum,
                        )
                new_map.collectible_count += 1

            new_map.cells.append(cell)

    return new_map
