from __future__ import annotations
import re
import sys
from typing import NamedTuple, Optional
from copy import deepcopy


class Point(NamedTuple):
    x: int
    y: int

    @staticmethod
    def parse(s: str) -> Point:
        xs, ys = s.split(',')
        return Point(int(xs), int(ys))


class State(NamedTuple):
    grid: dict[Point, str]
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def __repr__(self):
        min_x = min(p.x for p in self.grid.keys())
        max_x = max(p.x for p in self.grid.keys())
        max_y = max(p.y for p in self.grid.keys())
        return '\n'.join(
            ''.join(self.grid.get(Point(x, y), '.') for x in range(min_x, max_x + 1))
            for y in range(max_y + 1)
        )



FIXED_TILES = {'#', 'o'}

"""
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def main():
    grid: dict[Point, str] = {}
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            points = [Point.parse(s) for s in line.strip().split(' -> ')]
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i+1]
                if p1.x == p2.x:
                    for y in range(min(p1.y, p2.y), max(p1.y, p2.y) + 1):
                        grid[Point(p1.x, y)] = '#'
                else:
                    for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
                        grid[Point(x, p1.y)] = '#'

    min_y = min(p.y for p in grid.keys())
    max_y = max(p.y for p in grid.keys())
    min_x = min(p.x for p in grid.keys())
    max_x = max(p.x for p in grid.keys())

    starting_point = Point(x=500, y=0)
    grid[starting_point] = '+'
    grid2 = deepcopy(grid)
    state = State(grid, min_x, max_x, min_y, max_y)
    print(state, '\n\n')
    iterate(state, starting_point, verbose=True)

    print(sum(1 for v in state.grid.values() if v == 'o'))

    state2 = State(grid2, min_x, max_x, min_y, max_y)
    iterate(state2, starting_point, verbose=True, include_floor=True)
    print(sum(1 for v in state2.grid.values() if v == 'o'))


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
