from __future__ import annotations

from collections import deque, namedtuple, defaultdict
import sys
from datetime import datetime
from typing import NamedTuple, Iterable
from day09 import Sequence


class Point(NamedTuple):
    x: int
    y: int


class RelativePoint(NamedTuple):
    point: Point
    grid_dx: int
    grid_dy: int


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
    t0 = datetime.now()
    count_by_step: list[int] = [1]
    grandparent_visited = set()
    parent_visited = {(start.x, start.y)}
    normalized_new_point_steps: dict[frozenset, list[int]] = defaultdict(list)

    for step in range(1, 1001):
        new_points: set[TPoint] = set()
        for point in parent_visited:
            x, y = point
            for delta in DELTAS:
                nx = x + delta[0]
                ny = y + delta[1]
                if grid[ny % height][nx % width] != '#':
                    p = (nx, ny)
                    if p not in grandparent_visited:
                        new_points.add(p)
        normalized_new_points = frozenset((p[0] % width, p[1] % height) for p in new_points)
        normalized_new_point_steps[normalized_new_points].append(step)

        grandparent_visited = parent_visited
        parent_visited = new_points
        count_by_step.append(len(new_points))
        if step % 131 == 65:
            t = datetime.now()
            print(f'Step {step}, {sum(count_by_step[i] for i in range(step, -1, -2))} total, {len(new_points)} frontier, {(t - t0).total_seconds()}s elapsed'
                  f', {len(grandparent_visited)} grandparents')

    # Got a hint from online that the code from 2023 day 9 could be used to extrapolate the sequence, if we look at the
    # counts every 131 steps starting at 65 (65 steps gets to the edge of the grid, and 131 steps gets across the next
    # grid).
    seq = Sequence([
        sum(count_by_step[i] for i in range(step, -1, -2))
        for step in range(65, 983, 131)
    ])
    print(seq.numbers)
    step_seq = Sequence(list(range(65, 983, 131)))
    extrapolated_step = step_seq.extrapolate_next_n((26501365 - 982) // 131 + 1)
    extrapolated = seq.extrapolate_next_n((26501365 - 982) // 131 + 1)
    print(extrapolated_step[-1])
    print(extrapolated[-1])


if __name__ == '__main__':
    main()
