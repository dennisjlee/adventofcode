from __future__ import annotations
import re
import sys
from typing import NamedTuple, Optional
from copy import deepcopy


class Point(NamedTuple):
    x: int
    y: int


HORIZONTAL_LINE = frozenset([
    Point(0, 0),
    Point(1, 0),
    Point(2, 0),
    Point(3, 0),
])

CROSS = frozenset([
    Point(0, 1),
    Point(1, 0),
    Point(1, 1),
    Point(1, 2),
    Point(2, 1),
])

RIGHT_ANGLE = frozenset([
    Point(0, 0),
    Point(1, 0),
    Point(2, 0),
    Point(2, 1),
    Point(2, 2),
])

VERTICAL_LINE = frozenset([
    Point(0, 0),
    Point(0, 1),
    Point(0, 2),
    Point(0, 3),
])

SQUARE = [
    Point(0, 0),
    Point(1, 0),
    Point(0, 1),
    Point(1, 1),
]


class Shape:
    relative_points: list[Point]
    bottom_left: Point

    def __init__(self, relative_points: list[Point], bottom_left: Point):
        self.relative_points = relative_points
        self.bottom_left = bottom_left



def main():
    with open(sys.argv[1]) as f:
        jet_pattern = f.read().strip()

    print(len(jet_pattern))

def iterate(state: State, source: Point, verbose=True, include_floor=False):
    step = 0
    sand_landed = True

    def value(pt: Point) -> str:
        if include_floor and pt.y == state.max_y + 2:
            return '#'
        return state.grid.get(pt)

    limit_y = state.max_y + (2 if include_floor else 0)

    while sand_landed:
        step += 1
        # if step % 1000 == 0:
        #     print('step', step, '# of flow points', len(current_flow_points))
        #     if verbose:
        #         print(state, '\n', current, '\n\n')
        #         zzz = 1
        sand_landed = False
        x = source.x
        y = source.y
        while y <= limit_y:
            if value(down := Point(x, y + 1)) is None:
                x, y = down
            elif value(downleft := Point(x - 1, y + 1)) is None:
                x, y = downleft
            elif value(downright := Point(x + 1, y + 1)) is None:
                x, y = downright
            else:
                # fully blocked!
                p = Point(x, y)
                if p != source:
                    sand_landed = True
                state.grid[p] = 'o'
                break

    if verbose:
        print(state)


if __name__ == '__main__':
    main()
