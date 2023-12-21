from __future__ import annotations

from collections import deque
import sys
from datetime import datetime
from functools import cache
from typing import NamedTuple, Iterable


class Point(NamedTuple):
    x: int
    y: int


def neighbors_bounded(point: Point, width: int, height: int) -> Iterable[Point]:
    if point.y > 0:
        yield Point(point.x, point.y - 1)
    if point.y < height - 1:
        yield Point(point.x, point.y + 1)
    if point.x > 0:
        yield Point(point.x - 1, point.y)
    if point.x < width - 1:
        yield Point(point.x + 1, point.y)


DELTAS = [
    Point(0, 1),
    Point(0, -1),
    Point(1, 0),
    Point(-1, 0)
]


def main():
    with open(sys.argv[1]) as f:
        grid = tuple(tuple(line.strip()) for line in f.readlines())

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
            for neighbor in neighbors_bounded(point, width, height):
                if grid[neighbor.y][neighbor.x] != '#':
                    new_points.add(neighbor)
        points = new_points
    print(len(points))

    # part 2
    height = len(grid)
    width = len(grid[0])
    t0 = datetime.now()
    count_by_step: list[int] = [1]
    grandparent_visited = set()
    parent_visited = {start}
    for step in range(1, 26501366):
        new_points: set[Point] = set()
        for point in parent_visited:
            for delta in DELTAS:
                nx = point.x + delta.x
                ny = point.y + delta.y
                if grid[ny % height][nx % width] != '#':
                    p = Point(nx, ny)
                    if p not in grandparent_visited:
                        new_points.add(p)
        grandparent_visited = parent_visited
        parent_visited = new_points
        count_by_step.append(len(new_points))
        if step in {6, 10, 50, 100, 500, 1000, 5000, 26501355}:
            t = datetime.now()
            print(f'Step {step}, {sum(count_by_step[i] for i in range(step, -1, -2))} total, {(t - t0).total_seconds()}s elapsed')
    print(len(points))


if __name__ == '__main__':
    main()
