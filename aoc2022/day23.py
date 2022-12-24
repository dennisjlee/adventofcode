from __future__ import annotations

import sys
from collections import Counter, deque
from enum import Enum
from typing import NamedTuple, Optional, Iterable


class Move(NamedTuple):
    dx: int
    dy: int


NORTH = Move(0, -1)
SOUTH = Move(0, 1)
WEST = Move(-1, 0)
EAST = Move(1, 0)


class Point(NamedTuple):
    x: int
    y: int

    def adjacent_points(self, direction: Optional[Move] = None):
        if direction is None:
            yield Point(self.x - 1, self.y - 1)
            yield Point(self.x - 1, self.y)
            yield Point(self.x - 1, self.y + 1)
            yield Point(self.x, self.y - 1)
            yield Point(self.x, self.y + 1)
            yield Point(self.x + 1, self.y - 1)
            yield Point(self.x + 1, self.y)
            yield Point(self.x + 1, self.y + 1)
        elif direction == NORTH:
            yield Point(self.x - 1, self.y - 1)
            yield Point(self.x, self.y - 1)
            yield Point(self.x + 1, self.y - 1)
        elif direction == SOUTH:
            yield Point(self.x - 1, self.y + 1)
            yield Point(self.x, self.y + 1)
            yield Point(self.x + 1, self.y + 1)
        elif direction == WEST:
            yield Point(self.x - 1, self.y - 1)
            yield Point(self.x - 1, self.y)
            yield Point(self.x - 1, self.y + 1)
        elif direction == EAST:
            yield Point(self.x + 1, self.y - 1)
            yield Point(self.x + 1, self.y)
            yield Point(self.x + 1, self.y + 1)

    def walk(self, move: Move):
        return Point(self.x + move.dx, self.y + move.dy)


def main():
    with open(sys.argv[1]) as f:
        board = [list(line.strip()) for line in f.readlines()]

    elf_points = {
        Point(x, y)
        for y in range(len(board))
        for x in range(len(board[y]))
        if board[y][x] == '#'
    }
    directions = deque([NORTH, SOUTH, WEST, EAST])
    for i in range(1_000_000):
        new_elf_points = iterate(elf_points, directions)
        if i % 1000 == 0:
            print(f'executed {i + 1} rounds so far...')
        if elf_points == new_elf_points:
            print(f'done after {i + 1} rounds')
            break
        elf_points = new_elf_points
        directions.rotate(-1)

        if i == 9:
            # part 1
            min_x = min(p.x for p in elf_points)
            max_x = max(p.x for p in elf_points)
            min_y = min(p.y for p in elf_points)
            max_y = max(p.y for p in elf_points)
            print((max_x - min_x + 1) * (max_y - min_y + 1) - len(elf_points))


def iterate(elf_points: set[Point], directions: deque[Move], verbose=False) -> set[Point]:
    if verbose:
        min_x = min(p.x for p in elf_points)
        max_x = max(p.x for p in elf_points)
        min_y = min(p.y for p in elf_points)
        max_y = max(p.y for p in elf_points)
        for y in range(min_y, max_y + 1):
            print(''.join('#' if Point(x, y) in elf_points else '.' for x in range(min_x, max_x + 1)))
        print()

    proposed_moves: dict[Point, Point] = {}
    for p in elf_points:
        if any(np in elf_points for np in p.adjacent_points()):
            for direction in directions:
                if all(np not in elf_points for np in p.adjacent_points(direction)):
                    proposed_moves[p] = p.walk(direction)
                    break
            else:
                proposed_moves[p] = p
        else:
            proposed_moves[p] = p

    counter = Counter(proposed_moves.values())
    new_points = {
        p_next if counter[p_next] == 1 else p_curr
        for p_curr, p_next in proposed_moves.items()
    }
    assert len(new_points) == len(elf_points)
    return new_points


if __name__ == '__main__':
    main()
