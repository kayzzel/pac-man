from ..game.map.Cell import Cell

import heapq


OPPOSITE: dict[str, str] = {"N": "S", "S": "N", "E": "W", "W": "E"}

# direction -> (dx, dy) in (x, y) coordinates
STEPS: dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0)
}


def legal_path(
    start: tuple[int, int],  # (x, y)
    heading: str,
    goal: tuple[int, int],  # (x, y)
    maze: list[list[Cell]]
) -> list[str] | None:
    """
        Description:
    A* over (tile, direction) states to find the shortest path that a ghost
    can really follow:
      - it never turns back (no 180 degrees turn), except in a dead end
        where the only exit is the way it came from
      - the goal must be reached after at least one step, so a ghost that
        is already on its goal leaves and finds the shortest loop that
        brings it back to it

        Parameters:
    start -> the tile of the ghost (x, y)
    heading -> the direction the ghost is currently going to (N, S, E, W)
    goal -> the tile to reach (x, y)
    maze -> the grid of Cells, indexed maze[y][x]

        Returns value:
    return the list of directions to follow, or None if a tile is outside
    of the maze or if the goal cannot be reached
    """

    height: int = len(maze)
    width: int = len(maze[0])

    for x, y in (start, goal):
        if not (0 <= x < width and 0 <= y < height):
            return None

    # A node is (x, y, direction used to enter the tile). The start node has
    # an empty direction so that coming back to it is a different node.
    first: tuple[int, int, str] = (start[0], start[1], "")
    best_cost: dict[tuple[int, int, str], int] = {first: 0}
    came_from: dict[
        tuple[int, int, str],
        tuple[tuple[int, int, str], str]
    ] = {}

    counter: int = 0
    frontier: list[tuple[int, int, int, tuple[int, int, str]]] = [
        (abs(start[0] - goal[0]) + abs(start[1] - goal[1]), 0, counter, first)
    ]

    while frontier:
        _, cost, _, node = heapq.heappop(frontier)
        x, y, entered = node

        if cost > best_cost[node]:
            continue

        # The goal only counts once the ghost has moved at least one tile
        if (x, y) == goal and cost > 0:
            path: list[str] = []
            while node in came_from:
                node, direction = came_from[node]
                path.append(direction)
            path.reverse()
            return path

        current: str = entered if entered else heading

        exits: list[str] = [
            direction
            for direction, wall in maze[y][x].walls.items()
            if not wall
        ]

        # No 180 degrees turn, unless it is the only way out (dead end)
        if len(exits) > 1 and current in OPPOSITE:
            exits = [d for d in exits if d != OPPOSITE[current]]

        for direction in exits:
            new_x: int = x + STEPS[direction][0]
            new_y: int = y + STEPS[direction][1]

            if not (0 <= new_x < width and 0 <= new_y < height):
                continue

            new_node: tuple[int, int, str] = (new_x, new_y, direction)
            new_cost: int = cost + 1

            if new_cost < best_cost.get(new_node, new_cost + 1):
                best_cost[new_node] = new_cost
                came_from[new_node] = (node, direction)
                counter += 1
                heapq.heappush(frontier, (
                    new_cost + abs(new_x - goal[0]) + abs(new_y - goal[1]),
                    new_cost,
                    counter,
                    new_node
                ))

    return None


def next_direction(
    start: tuple[int, int],
    heading: str,
    goal: tuple[int, int],
    maze: list[list[Cell]]
) -> str | None:
    """
        Description:
    Give the direction a ghost must take now to follow legal_path

        Returns value:
    return the next direction (N, S, E, W) or None if there is no path
    """

    path: list[str] | None = legal_path(start, heading, goal, maze)

    if not path:
        return None

    return path[0]
