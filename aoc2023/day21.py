from __future__ import annotations

from collections import deque, namedtuple, defaultdict
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


TPoint = tuple[int, int]


DELTAS: list[TPoint] = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]


def main():
    with open(sys.argv[1]) as f:
        grid = list(list(line.strip()) for line in f.readlines())

    start = None
    for y, line in enumerate(grid):
        try:
            x = line.index('S')
            start = Point(x, y)
            break
        except ValueError:
            pass

    # part 1
    # points = {start}
    # height = len(grid)
    # width = len(grid[0])
    # for step in range(1, 65):
    #     new_points: set[Point] = set()
    #     for point in points:
    #         for neighbor in neighbors_bounded(point, width, height):
    #             if grid[neighbor.y][neighbor.x] != '#':
    #                 new_points.add(neighbor)
    #     points = new_points
    # print(len(points))

    # part 2
    height = len(grid)
    width = len(grid[0])
    t0 = datetime.now()
    count_by_step: list[int] = [1]
    grandparent_visited = set()
    parent_visited = {(start.x, start.y)}
    normalized_parents = {(start.x, start.y)}
    normalized_new_point_steps: dict[frozenset, list[int]] = defaultdict(list)

    for step in range(1, 1001):
        new_points: set[TPoint] = set()
        normalized = {(x % width, y % height) for x, y in parent_visited}
        print(len(parent_visited), len(normalized))
        for point in parent_visited:
            matching_deltas = []
            x, y = point
            for delta in DELTAS:
                nx = x + delta[0]
                ny = y + delta[1]
                if grid[ny % height][nx % width] != '#':
                    p = (nx, ny)
                    if p not in grandparent_visited:
                        matching_deltas.append(delta)
                        new_points.add(p)
        normalized_new_points = frozenset((p[0] % width, p[1] % height) for p in new_points)
        normalized_new_point_steps[normalized_new_points].append(step)

        if 38 <= step <= 49:
            print(f'Step {step}, {len(new_points)} new points')

        grandparent_visited = parent_visited
        parent_visited = new_points
        count_by_step.append(len(new_points))
        if step in {6, 10, 50, 100, 500, 1000, 2000, 3000, 4000, 5000, 26501355}:
            t = datetime.now()
            # print(f'Step {step}, {sum(count_by_step[i] for i in range(step, -1, -2))} total, {len(new_points)} frontier, {(t - t0).total_seconds()}s elapsed')
    # print('\n'.join(f'{repr(sorted(k))}: {v[0]}' for k, v in normalized_new_point_steps.items() if len(v) > 1))


if __name__ == '__main__':
    main()
