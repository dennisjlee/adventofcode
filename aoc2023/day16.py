from __future__ import annotations

import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def move(self, vector: tuple[int, int]):
        return Point(self.x + vector[0], self.y + vector[1])


NORTH = (0, -1)
SOUTH = (0, 1)
WEST = (-1, 0)
EAST = (1, 0)

REFLECTIONS = {
    '\\': {
        EAST: SOUTH,
        SOUTH: EAST,
        WEST: NORTH,
        NORTH: WEST
    },
    '/': {
       EAST: NORTH,
       NORTH: EAST,
       WEST: SOUTH,
       SOUTH: WEST
    }
}

SPLITS = {
    '|': {
        EAST: [NORTH, SOUTH],
        SOUTH: [SOUTH],
        WEST: [NORTH, SOUTH],
        NORTH: [NORTH]
    },
    '-': {
        EAST: [EAST],
        NORTH: [EAST, WEST],
        WEST: [WEST],
        SOUTH: [EAST, WEST]
    }
}


class BeamLocation(NamedTuple):
    point: Point
    direction: tuple[int, int]


def main():
    with open(sys.argv[1]) as f:
        grid = [list(s) for s in f.readlines()]

    height = len(grid)
    width = len(grid[0])

    # part 1
    print(count_energized_tiles(BeamLocation(Point(-1, 0), EAST), grid, width, height))

    # part 2
    entry_points = [
        BeamLocation(Point(-1, y), EAST) for y in range(height)
    ] + [
        BeamLocation(Point(width, y), WEST) for y in range(height)
    ] + [
        BeamLocation(Point(x, -1), SOUTH) for x in range(width)
    ] + [
        BeamLocation(Point(x, height), NORTH) for x in range(width)
    ]
    print(max(count_energized_tiles(entry, grid, width, height) for entry in entry_points))


def count_energized_tiles(starting_beam: BeamLocation, grid: list[list[str]], width: int, height: int) -> int:
    queue = [starting_beam]
    visited: set[BeamLocation] = set()
    while queue:
        loc = queue.pop()
        dir = loc.direction
        if loc not in visited:
            visited.add(loc)
            new_point = loc.point.move(dir)
            if 0 <= new_point.x < width and 0 <= new_point.y < height:
                obj = grid[new_point.y][new_point.x]
                if obj == '.':
                    queue.append(BeamLocation(new_point, dir))
                elif obj in REFLECTIONS:
                    new_dir = REFLECTIONS[obj][dir]
                    queue.append(BeamLocation(new_point, new_dir))
                elif obj in SPLITS:
                    new_dirs = SPLITS[obj][dir]
                    queue.extend(BeamLocation(new_point, new_dir) for new_dir in new_dirs)

    return len(set(loc.point for loc in visited if 0 <= loc.point.x < width and 0 <= loc.point.y < height))


if __name__ == '__main__':
    main()
