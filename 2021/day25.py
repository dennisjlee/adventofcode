import collections
import itertools
import re
import sys
import typing
from copy import deepcopy


class Point(typing.NamedTuple):
    x: int
    y: int

Grid = list[list[str]]


def main():
    with open(sys.argv[1]) as f:
        grid: Grid = [list(line.strip()) for line in f.readlines()]

    height = len(grid)
    width = len(grid[0])
    turn = 0
    for turn in itertools.count(1):
        grid, move_count = iterate(grid, height, width)
        if move_count == 0:
            break
    print(turn)


def iterate(grid: Grid, height: int, width: int) -> tuple[Grid, int]:
    new_grid = deepcopy(grid)
    move_count = 0

    # east
    for m in east_moves(grid, height, width):
        move_count += 1
        new_grid[m.y][m.x] = '.'
        new_grid[m.y][(m.x + 1) % width] = '>'

    # south
    for m in list(south_moves(new_grid, height, width)):
        move_count += 1
        new_grid[m.y][m.x] = '.'
        new_grid[(m.y + 1) % height][m.x] = 'v'

    return new_grid, move_count


def east_moves(grid: Grid, height: int, width: int) -> typing.Iterable[Point]:
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '>' and grid[y][(x + 1) % width] == '.':
                yield Point(x, y)


def south_moves(grid: Grid, height: int, width: int) -> typing.Iterable[Point]:
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'v' and grid[(y + 1) % height][x] == '.':
                yield Point(x, y)


if __name__ == '__main__':
    main()
