from __future__ import annotations

import sys
from typing import NamedTuple


"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

"""


class Point(NamedTuple):
    x: int
    y: int


class PipeSegment(NamedTuple):
    point: Point
    kind: str

    def neighbors(self):
        if self.kind == '|':
            return [
                Point(self.point.x, self.point.y - 1),
                Point(self.point.x, self.point.y + 1),
            ]
        elif self.kind == '-':
            return [
                Point(self.point.x - 1, self.point.y),
                Point(self.point.x + 1, self.point.y),
            ]
        elif self.kind == 'L':
            return [
                Point(self.point.x, self.point.y - 1),
                Point(self.point.x + 1, self.point.y),
            ]
        elif self.kind == 'J':
            return [
                Point(self.point.x, self.point.y - 1),
                Point(self.point.x - 1, self.point.y),
            ]
        elif self.kind == '7':
            return [
                Point(self.point.x, self.point.y + 1),
                Point(self.point.x - 1, self.point.y),
            ]
        elif self.kind == 'F':
            return [
                Point(self.point.x, self.point.y + 1),
                Point(self.point.x + 1, self.point.y),
            ]
        else:
            return []


def main():
    with open(sys.argv[1]) as f:
        grid = [list(line) for line in f.readlines()]

    start = None
    for y, line in enumerate(grid):
        try:
            x = line.index('S')
            start = Point(x, y)
            break
        except ValueError:
            pass

    print(start)
    visited = {start}
    ends: list[PipeSegment] = []
    for candidate in [
        Point(start.x, start.y + 1),
        Point(start.x, start.y - 1),
        Point(start.x + 1, start.y),
        Point(start.x - 1, start.y),
    ]:
        pipe = PipeSegment(candidate, grid[candidate.y][candidate.x])
        neighbors = pipe.neighbors()
        if start in neighbors:
            visited.add(candidate)
            ends.append(pipe)

    while len(ends):
        new_ends = []
        for end in ends:
            for neighbor in end.neighbors():
                if neighbor not in visited:
                    visited.add(neighbor)
                    pipe = PipeSegment(neighbor, grid[neighbor.y][neighbor.x])
                    new_ends.append(pipe)
        ends = new_ends

    # part 1
    print(len(visited) // 2)

    for y in range(len(grid)):
        line = ''.join([
            grid[y][x] if Point(x, y) in visited else '.'
            for x in range(len(grid[0]))
        ])
        print(line)



if __name__ == '__main__':
    main()
