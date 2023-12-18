from __future__ import annotations

import sys
from collections import defaultdict
from heapq import heappop, heappush
from typing import NamedTuple, Iterable


class Point(NamedTuple):
    x: int
    y: int

class Vector(NamedTuple):
    x: int
    y: int


Grid = list[list[int]]


Loc = tuple[Point, Vector, int]


class State(NamedTuple):
    loss: int
    point: Point
    vector: Vector
    straight_moves_left: int

    def successor_states(self, grid: Grid, width: int, height: int) -> Iterable[State]:
        new_x = self.point.x + self.vector.x
        new_y = self.point.y + self.vector.y
        if 0 <= new_x < width and 0 <= new_y < height:
            new_loss = self.loss + grid[new_y][new_x]
            if self.straight_moves_left > 1:
                if 0 <= new_x + self.vector.x < width and 0 <= new_y + self.vector.y < height:
                    yield State(new_loss, Point(new_x, new_y), self.vector, self.straight_moves_left - 1)

            for new_vec in ROTATIONS[self.vector]:
                if 0 <= new_x + new_vec.x < width and 0 <= new_y + new_vec.y < height:
                    yield State(new_loss, Point(new_x, new_y), new_vec, 3)

    @property
    def loc(self) -> Loc:
        return self.point, self.vector, self.straight_moves_left


NORTH = Vector(0, -1)
SOUTH = Vector(0, 1)
WEST = Vector(-1, 0)
EAST = Vector(1, 0)


ROTATIONS = {
    NORTH: [EAST, WEST],
    SOUTH: [EAST, WEST],
    WEST: [NORTH, SOUTH],
    EAST: [NORTH, SOUTH],
}


def dijkstra(grid: Grid, start: Point, end: Point, width: int, height: int):
    heap = [State(0, start, EAST, 3), State(0, start, SOUTH, 3)]
    visited: set[Loc] = set()
    tentative_distance: dict[Loc, int] = defaultdict(lambda: sys.maxsize)
    for state in heap:
        loc = state.loc
        visited.add(loc)
        tentative_distance[loc] = 0

    step = 0
    while heap:
        curr: State = heappop(heap)
        x, y = curr.point
        loss = grid[y][x]

        step += 1
        if step % 1000 == 0:
            print(f'step: {step}, heap size {len(heap)}')

        if curr.point == end:
            print(f'Solved! step: {step}, heap size {len(heap)}')
            return curr.loss

        visited.add(curr.loc)

        for candidate in curr.successor_states(grid, width, height):
            if candidate.loc not in visited:
                if candidate.loss < tentative_distance[candidate.loc]:
                    tentative_distance[candidate.loc] = candidate.loss
                    heappush(heap, candidate)
    return sys.maxsize


def main():
    with open(sys.argv[1]) as f:
        grid = [
            [int(c) for c in s.strip()]
            for s in f.readlines()
        ]

    # part 1
    height = len(grid)
    width = len(grid[0])

    print(dijkstra(grid, Point(0, 0), Point(width - 1, height - 1), width, height))

    # part 2


if __name__ == '__main__':
    main()
