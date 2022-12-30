from __future__ import annotations

import re
import sys
from typing import Optional, NamedTuple, Literal

MOVE_REGEX = re.compile(r'(\d+)([LR]?)')


class Facings:
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

FACING_NAMES = ['right', 'down', 'left', 'up']

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


class Node(NamedTuple):
    value: str
    point: Point
    neighbors: list[Optional[Node]]
    facing_changes: dict[int, int]

    def __repr__(self):
        return f'Node(\'{self.value}\', {self.point})'


def main():
    with open(sys.argv[1]) as f:
        board, path = f.read().split('\n\n')


    moves = []
    for match in MOVE_REGEX.finditer(path):
        magnitude = int(match.group(1))
        moves.append(Move(magnitude, None))
        if match.group(2):
            moves.append(Move(None, match.group(2)))

    part1(board, moves)
    part2(board, moves)


def part1(board: str, moves: list[Move]):
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
            if facing == Facings.RIGHT:
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
            elif facing == Facings.DOWN:
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
            elif facing == Facings.LEFT:
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
            elif facing == Facings.UP:
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


def part2(board: str, moves: list[Move]):
    grid: list[list[Optional[Node]]] = []

    for y, line in enumerate(board.split('\n')):
        row = [Node(c, Point(x, y), neighbors=[None]*4, facing_changes={})
               if c != ' ' else None for x, c in enumerate(line)]
        grid.append(row)

    for y in range(50):
        # square 1
        for x in range(50, 100):
            node = grid[y][x]
            node.neighbors[Facings.RIGHT] = grid[y][x + 1]
            node.neighbors[Facings.DOWN] = grid[y + 1][x]
            if y > 0:
                node.neighbors[Facings.UP] = grid[y - 1][x]
            else:
                # link to left edge of square 6
                node.neighbors[Facings.UP] = grid[100 + x][0]
                node.facing_changes[Facings.UP] = Facings.RIGHT

            if x > 50:
                node.neighbors[Facings.LEFT] = grid[y][x - 1]
            else:
                # link to left edge of square 4
                node.neighbors[Facings.LEFT] = grid[149 - y][0]
                node.facing_changes[Facings.LEFT] = Facings.RIGHT

        # square 2
        for x in range(100, 150):
            node = grid[y][x]
            node.neighbors[Facings.LEFT] = grid[y][x - 1]
            if y > 0:
                node.neighbors[Facings.UP] = grid[y - 1][x]
            else:
                # link to bottom edge of square 6, still facing up
                node.neighbors[Facings.UP] = grid[199][x - 100]

            if y < 49:
                node.neighbors[Facings.DOWN] = grid[y + 1][x]
            else:
                # link to right edge of square 3
                node.neighbors[Facings.DOWN] = grid[x - 50][99]
                node.facing_changes[Facings.DOWN] = Facings.LEFT

            if x < 149:
                node.neighbors[Facings.RIGHT] = grid[y][x + 1]
            else:
                # link to right edge of square 5
                node.neighbors[Facings.RIGHT] = grid[149 - y][99]
                node.facing_changes[Facings.RIGHT] = Facings.LEFT

    for y in range(50, 100):
        # square 3
        for x in range(50, 100):
            node = grid[y][x]
            node.neighbors[Facings.UP] = grid[y - 1][x]
            node.neighbors[Facings.DOWN] = grid[y + 1][x]
            if x > 50:
                node.neighbors[Facings.LEFT] = grid[y][x - 1]
            else:
                # link to top edge of square 4
                node.neighbors[Facings.LEFT] = grid[100][y - 50]
                node.facing_changes[Facings.LEFT] = Facings.DOWN

            if x < 99:
                node.neighbors[Facings.RIGHT] = grid[y][x + 1]
            else:
                # link to bottom edge of square 2
                node.neighbors[Facings.RIGHT] = grid[49][y + 50]
                node.facing_changes[Facings.RIGHT] = Facings.UP

    for y in range(100, 150):
        # square 4
        for x in range(50):
            node = grid[y][x]
            node.neighbors[Facings.RIGHT] = grid[y][x + 1]
            node.neighbors[Facings.DOWN] = grid[y + 1][x]
            if y > 100:
                node.neighbors[Facings.UP] = grid[y - 1][x]
            else:
                # link to left edge of square 3
                node.neighbors[Facings.UP] = grid[x + 50][50]
                node.facing_changes[Facings.UP] = Facings.RIGHT

            if x > 0:
                node.neighbors[Facings.LEFT] = grid[y][x - 1]
            else:
                # link to left edge of square 1
                node.neighbors[Facings.LEFT] = grid[149 - y][50]
                node.facing_changes[Facings.LEFT] = Facings.RIGHT

        # square 5
        for x in range(50, 100):
            node = grid[y][x]
            node.neighbors[Facings.LEFT] = grid[y][x - 1]
            node.neighbors[Facings.UP] = grid[y - 1][x]

            if x < 99:
                node.neighbors[Facings.RIGHT] = grid[y][x + 1]
            else:
                # link to right edge of square 2
                node.neighbors[Facings.RIGHT] = grid[149 - y][149]
                node.facing_changes[Facings.RIGHT] = Facings.LEFT

            if y < 149:
                node.neighbors[Facings.DOWN] = grid[y + 1][x]
            else:
                # link to right edge of square 6
                node.neighbors[Facings.DOWN] = grid[x + 100][49]
                node.facing_changes[Facings.DOWN] = Facings.LEFT

    for y in range(150, 200):
        # square 6
        for x in range(50):
            node = grid[y][x]
            node.neighbors[Facings.UP] = grid[y - 1][x]

            if y < 199:
                node.neighbors[Facings.DOWN] = grid[y + 1][x]
            else:
                # link to top edge of square 2, still facing down
                node.neighbors[Facings.DOWN] = grid[0][x + 100]

            if x > 0:
                node.neighbors[Facings.LEFT] = grid[y][x - 1]
            else:
                # link to top edge of square 1
                node.neighbors[Facings.LEFT] = grid[0][y - 100]
                node.facing_changes[Facings.LEFT] = Facings.DOWN

            if x < 49:
                node.neighbors[Facings.RIGHT] = grid[y][x + 1]
            else:
                # link to bottom edge of square 5
                node.neighbors[Facings.RIGHT] = grid[149][y - 100]
                node.facing_changes[Facings.RIGHT] = Facings.UP

    for row in grid:
        for node in row:
            if node is not None:
                assert all(node.neighbors)

    curr_node = grid[0][50]
    facing = 0

    for move in moves:
        if move.rotation:
            if move.rotation == 'R':
                facing = (facing + 1) % 4
            elif move.rotation == 'L':
                facing = (facing - 1) % 4
        else:
            for _ in range(move.magnitude):
                next_node = curr_node.neighbors[facing]
                if next_node.value == '#':
                    break
                facing = curr_node.facing_changes.get(facing, facing)
                curr_node = next_node

    print(curr_node.point.y + 1, curr_node.point.x + 1, facing)
    print(1000 * (curr_node.point.y + 1) + 4 * (curr_node.point.x + 1) + facing)


if __name__ == '__main__':
    main()
