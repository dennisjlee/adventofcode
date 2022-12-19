from __future__ import annotations
import re
import sys
from itertools import cycle
from typing import NamedTuple, Optional, Iterable
from copy import deepcopy


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


if __name__ == '__main__':
    main()
