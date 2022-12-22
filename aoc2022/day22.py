from __future__ import annotations

import re
import sys
from operator import add, sub, mul, floordiv
from typing import Optional, NamedTuple, Literal

MOVE_REGEX = re.compile(r'(\d+)([LR]?)')

FACINGS = ['r', 'd', 'l', 'u']
FACING_MAP = {f: i for f, i in enumerate(FACINGS)}


Rotation = Literal['L', 'R']


class Point(NamedTuple):
    x: int
    y: int


DELTAS = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]

class Interval(NamedTuple):
    start: int
    end: int


class Move(NamedTuple):
    magnitude: Optional[int]
    rotation: Optional[Rotation]

    def __repr__(self):
        return f'Move({self.rotation or self.magnitude})'


def main():
    with open(sys.argv[1]) as f:
        board, path = f.read().split('\n\n')

    part1(board, path)


def part1(board: str, path: str):
    grid: list[list[Optional[str]]] = []
    x_bounds: list[Interval] = []
    y_bounds: list[Interval] = []

    for y, line in enumerate(board.split('\n')):
        row = [c if c != ' ' else None for c in line]
        grid.append(row)
        populated_x_indices = [x for x, c in enumerate(row) if c is not None]
        x_bounds.append(Interval(min(populated_x_indices), max(populated_x_indices)))

    height = len(grid)
    width = max(len(row) for row in grid)
    for x in range(width):
        populated_y_indices = [y for y in range(height) if len(grid[y]) > x and grid[y][x] is not None]
        y_bounds.append(Interval(min(populated_y_indices), max(populated_y_indices)))

    moves = []
    for match in MOVE_REGEX.finditer(path):
        magnitude = int(match.group(1))
        moves.append(Move(magnitude, None))
        if match.group(2):
            moves.append(Move(None, match.group(2)))

    cy = 0
    cx = x_bounds[0].start
    facing = 0

    for move in moves:
        if move.rotation:
            if move.rotation == 'R':
                facing = (facing + 1) % 4
            elif move.rotation == 'L':
                facing = (facing - 1) % 4
        else:
            if facing == 0:
                bounds = x_bounds[cy]
                for _ in range(move.magnitude):
                    if cx == bounds.end:
                        nx = bounds.start
                    else:
                        nx = cx + 1
                    if grid[cy][nx] == '#':
                        break
                    else:
                        cx = nx
            elif facing == 1:
                bounds = y_bounds[cx]
                for _ in range(move.magnitude):
                    if cy == bounds.end:
                        ny = bounds.start
                    else:
                        ny = cy + 1
                    if grid[ny][cx] == '#':
                        break
                    else:
                        cy = ny
            elif facing == 2:
                bounds = x_bounds[cy]
                for _ in range(move.magnitude):
                    if cx == bounds.start:
                        nx = bounds.end
                    else:
                        nx = cx - 1
                    if grid[cy][nx] == '#':
                        break
                    else:
                        cx = nx
            elif facing == 3:
                bounds = y_bounds[cx]
                for _ in range(move.magnitude):
                    if cy == bounds.start:
                        ny = bounds.end
                    else:
                        ny = cy - 1
                    if grid[ny][cx] == '#':
                        break
                    else:
                        cy = ny

    print(cy + 1, cx + 1, facing)
    print(1000 * (cy + 1) + 4 * (cx + 1) + facing)


if __name__ == '__main__':
    main()
