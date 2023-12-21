from __future__ import annotations

from collections import deque
import sys
from typing import NamedTuple, Iterable


class Point(NamedTuple):
    x: int
    y: int


def neighbors(point: Point, width: int, height: int) -> Iterable[Point]:
    if point.y > 0:
        yield Point(point.x, point.y - 1)
    if point.y < height - 1:
        yield Point(point.x, point.y + 1)
    if point.x > 0:
        yield Point(point.x - 1, point.y)
    if point.x < width - 1:
        yield Point(point.x + 1, point.y)


def main():
    with open(sys.argv[1]) as f:
        grid = [list(line) for line in f.readlines()]

    start = None
    for y, line in enumerate(grid):
        try:
            x = line.index('S')
            start = Point(x, y)
            break
        except ValueError:
            pass

    # part 1
    points = {start}
    height = len(grid)
    width = len(grid[0])
    for step in range(1, 65):
        new_points: set[Point] = set()
        for point in points:
            for neighbor in neighbors(point, width, height):
                if grid[neighbor.y][neighbor.x] != '#':
                    new_points.add(neighbor)
        points = new_points

    print(len(points))


if __name__ == '__main__':
    main()
