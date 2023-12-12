from __future__ import annotations

from collections import deque
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
    visited_points = {start}
    pipes_by_point: dict[Point, PipeSegment] = {}
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
            visited_points.add(candidate)
            ends.append(pipe)
            pipes_by_point[candidate] = pipe

    start_pipe = compute_start_pipe(start, ends)
    pipes_by_point[start] = start_pipe

    while ends:
        new_ends = []
        for end in ends:
            for neighbor in end.neighbors():
                if neighbor not in visited_points:
                    visited_points.add(neighbor)
                    pipe = PipeSegment(neighbor, grid[neighbor.y][neighbor.x])
                    new_ends.append(pipe)
                    pipes_by_point[neighbor] = pipe
        ends = new_ends

    # part 1
    print(len(visited_points) // 2)

    expanded_pipes: set[Point] = set()
    for point, pipe in pipes_by_point.items():
        mapped_point = Point(point.x * 2, point.y * 2)
        expanded_pipes.add(mapped_point)
        mapped_pipe = PipeSegment(mapped_point, pipe.kind)
        for neighbor in mapped_pipe.neighbors():
            expanded_pipes.add(neighbor)

    visited_points: set[Point] = set()
    double_height = len(grid) * 2
    double_width = len(grid[0]) * 2
    edges = [Point(x, 0) for x in range(double_width)] + \
            [Point(x, double_height - 1) for x in range(double_width)] + \
            [Point(0, y) for y in range(double_height)] + \
            [Point(double_width - 1, y) for y in range(double_height)]
    queue = deque([edge for edge in edges if edge not in expanded_pipes])
    while queue:
        p = queue.popleft()
        if p in visited_points:
            continue
        visited_points.add(p)
        for p_next in [Point(p.x - 1, p.y), Point(p.x + 1, p.y), Point(p.x, p.y - 1), Point(p.x, p.y + 1)]:
            if 0 <= p_next.x < double_width and 0 <= p_next.y < double_height \
                    and p_next not in expanded_pipes and p_next not in visited_points:
                queue.append(p_next)

    inside: set[Point] = set()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            candidate = Point(x * 2, y * 2)
            if candidate not in expanded_pipes and candidate not in visited_points:
                inside.add(Point(x, y))
    print(len(inside))

    # visualize the grid
    for y in range(len(grid)):
        def get_chars():
            for x in range(len(grid[0])):
                candidate = Point(x, y)
                if candidate in pipes_by_point:
                    yield pipes_by_point[candidate].kind
                elif Point(2*candidate.x, 2*candidate.y) in visited_points:
                    yield 'O'
                else:
                    yield 'I'
        print(''.join(get_chars()))


def compute_start_pipe(start: Point, neighbors: list[PipeSegment]) -> PipeSegment:
    [p1, p2] = sorted(neighbors, key=lambda p: p.point)
    if p1.point.x == start.x and p2.point.x == start.x:
        start_type = '|'
    elif p1.point.y == start.y and p2.point.y == start.y:
        start_type = '-'
    elif p1.point.x == start.x and p1.point.y == start.y - 1 \
            and p2.point.x == start.x + 1 and p2.point.y == start.y:
        start_type = 'L'
    elif p1.point.x == start.x - 1 and p1.point.y == start.y \
            and p2.point.x == start.x and p2.point.y == start.y - 1:
        start_type = 'J'
    elif p1.point.x == start.x - 1 and p1.point.y == start.y \
            and p2.point.x == start.x and p2.point.y == start.y + 1:
        start_type = '7'
    elif p1.point.x == start.x and p1.point.y == start.y + 1 \
            and p2.point.x == start.x + 1 and p2.point.y == start.y:
        start_type = 'F'
    else:
        raise Exception('Could not determine start type')

    return PipeSegment(start, start_type)


if __name__ == '__main__':
    main()
