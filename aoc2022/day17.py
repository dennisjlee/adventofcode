from __future__ import annotations

import sys
from collections import defaultdict
from itertools import cycle
from typing import NamedTuple, Iterable


class Point(NamedTuple):
    x: int
    y: int


class Shape(NamedTuple):
    height: int
    relative_points: frozenset[Point]


HORIZONTAL_LINE = Shape(1, frozenset([
    Point(0, 0),
    Point(1, 0),
    Point(2, 0),
    Point(3, 0),
]))

CROSS = Shape(3, frozenset([
    Point(0, 1),
    Point(1, 0),
    Point(1, 1),
    Point(1, 2),
    Point(2, 1),
]))

RIGHT_ANGLE = Shape(3, frozenset([
    Point(0, 0),
    Point(1, 0),
    Point(2, 0),
    Point(2, 1),
    Point(2, 2),
]))

VERTICAL_LINE = Shape(4, frozenset([
    Point(0, 0),
    Point(0, 1),
    Point(0, 2),
    Point(0, 3),
]))

SQUARE = Shape(2, frozenset([
    Point(0, 0),
    Point(1, 0),
    Point(0, 1),
    Point(1, 1),
]))

SHAPES = [HORIZONTAL_LINE, CROSS, RIGHT_ANGLE, VERTICAL_LINE, SQUARE]


def get_shape_points(lower_left: Point, shape: Shape):
    return [
        Point(lower_left.x + p.x, lower_left.y + p.y)
        for p in shape.relative_points
    ]


def print_grid(occupied_spaces: set[Point]):
    max_y = max(p.y for p in occupied_spaces) if occupied_spaces else 1
    for y in range(max_y, -1, -1):
        row = ''.join('#' if Point(x, y) in occupied_spaces else '.'
                      for x in range(7))
        print(row)
    print('\n')


def main():
    with open(sys.argv[1]) as f:
        jet_pattern = f.read().strip()

    part1(jet_pattern)
    part2(jet_pattern)


def part1(jet_pattern: str):
    occupied_spaces: set[Point] = set()
    jet_iter = cycle([-1 if j == '<' else 1 for j in jet_pattern])

    def all_unoccupied(points: Iterable[Point]) -> bool:
        return all(
            (p not in occupied_spaces and
             0 <= p.x < 7 and
             p.y >= 0)
            for p in points
        )
    verbose = False

    max_y = 0
    for i in range(2022):
        if verbose:
            print_grid(occupied_spaces)
        shape = SHAPES[i % len(SHAPES)]
        x = 2
        y = max_y + 3
        curr_points = get_shape_points(Point(x, y), shape)
        while True:
            dx = next(jet_iter)
            next_points = get_shape_points(Point(x+dx, y), shape)
            if all_unoccupied(next_points):
                curr_points = next_points
                x += dx
            next_points = get_shape_points(Point(x, y - 1), shape)
            if all_unoccupied(next_points):
                curr_points = next_points
                y -= 1
            else:
                occupied_spaces.update(curr_points)
                max_y = max(max_y, y + shape.height)
                break
    print(max_y)
    # print_grid(occupied_spaces)


def shift_points(points: Iterable[Point], *, dx: int = 0, dy: int = 0) -> Iterable[Point]:
    for p in points:
        yield Point(p.x + dx, p.y + dy)


def row_to_str(grid, ys):
    return '\n'.join(
        ''.join('#' if x in grid[y] else '.' for x in range(7))
        for y in ys
    )


class Checkpoint(NamedTuple):
    shape_index: int
    height: int


def part2(jet_pattern: str, verbose=False):
    jet_direction = [-1 if c == '<' else 1 for c in jet_pattern]
    jet_count = len(jet_direction)
    shape_count = len(SHAPES)
    grid: dict[int, set[int]] = defaultdict(set)

    min_y = 0
    max_y = 0

    def unoccupied(p: Point) -> bool:
        return (0 <= p.x < 7 and
                p.y >= min_y and
                not (p.y in grid and
                     p.x in grid[p.y]))

    j = 0
    checkpoints: list[Checkpoint] = []
    key_checkpoints: list[Checkpoint] = []
    for i in range(100_000):
        shape = SHAPES[i % shape_count]
        if verbose and i > 0 and j % jet_count == 0:
            print(f'{i}\t{j}\t{max_y}')
        checkpoints.append(Checkpoint(i, max_y))
        if i > 0 and j % jet_count == 0:
            key_checkpoints.append(Checkpoint(i, max_y))
            if len(key_checkpoints) > 2:
                print(key_checkpoints,
                      [(key_checkpoints[i][0] - key_checkpoints[i-1][0]) for i in range(1, len(key_checkpoints))])

                print(checkpoints[key_checkpoints[1][0] - 5: key_checkpoints[1][0] + 1])
                print(checkpoints[key_checkpoints[2][0] - 5: key_checkpoints[2][0] + 1])
                break
        x = 2
        y = max_y + 3
        curr_points = get_shape_points(Point(x, y), shape)
        stopped = False
        while not stopped:
            dx = jet_direction[j % jet_count]
            j += 1
            next_points = []
            for next_p in shift_points(curr_points, dx=dx):
                if unoccupied(next_p):
                    next_points.append(next_p)
                else:
                    break
            else:
                curr_points = next_points
                x += dx

            next_points = []
            for next_p in shift_points(curr_points, dy=-1):
                if unoccupied(next_p):
                    next_points.append(next_p)
                else:
                    stopped = True
                    for new_p in curr_points:
                        grid[new_p.y].add(new_p.x)
                    max_y = max(max_y, y + shape.height)

                    for affected_y in {new_p.y for new_p in curr_points}:
                        if len(grid[affected_y]) == 7:
                            # we have a fully completed row, move the floor up and delete
                            # data below this
                            for y_to_remove in range(min_y, affected_y):
                                if y_to_remove in grid:
                                    del grid[y_to_remove]
                            min_y = affected_y

                    break
            else:
                curr_points = next_points
                y -= 1

    target = 1_000_000_000_000
    cycle_start_index = key_checkpoints[0].shape_index
    cycle_start_y = key_checkpoints[0].height
    cycle_length = key_checkpoints[1].shape_index - cycle_start_index
    cycle_dy = key_checkpoints[1].height - key_checkpoints[0].height
    effective_index = (target - cycle_start_index) % cycle_length
    num_cycles = (target - cycle_start_index) // cycle_length
    print(num_cycles * cycle_dy +
          (checkpoints[cycle_start_index + effective_index].height - checkpoints[cycle_start_index].height) +
          cycle_start_y)


if __name__ == '__main__':
    main()
