from __future__ import annotations

from collections import defaultdict
from heapq import heapify, heappop, heappush
from typing import NamedTuple, Optional, Iterable, Callable
import sys


class Point(NamedTuple):
    x: int
    y: int


class State(NamedTuple):
    cost: int
    current: Point
    visited: set[Point]


def manhattan_distance(p1: Point, p2: Point):
    return abs(p1.y - p2.y) + abs(p1.x - p2.x)


def main():
    with open(sys.argv[1]) as f:
        raw_grid = [list(line.strip()) for line in f.readlines()]

    search_dijkstra(raw_grid)


def candidate_points(p: Point, width: int, height: int) -> Iterable[Point]:
    x, y = p
    if x > 0:
        yield Point(x - 1, y)

    if x < width - 1:
        yield Point(x + 1, y)

    if y > 0:
        yield Point(x, y - 1)

    if y < height - 1:
        yield Point(x, y + 1)


def search_dijkstra(raw_grid):
    height = len(raw_grid)
    width = len(raw_grid[0])
    start: Optional[Point] = None
    end: Optional[Point] = None

    print(f'grid is {height} x {width}')

    grid = [
        [0] * width
        for _ in range(height)
    ]

    other_starting_squares = []
    for y in range(height):
        for x in range(width):
            if raw_grid[y][x] == 'S':
                start = Point(x, y)
                z = 0
            elif raw_grid[y][x] == 'E':
                end = Point(x, y)
                z = 25
            else:
                z = ord(raw_grid[y][x]) - ord('a')
                if z == 0:
                    other_starting_squares.append(Point(x, y))
            grid[y][x] = z

    original_dist = dijkstra(grid, start, end, width, height)
    print(original_dist)

    min_distance = dijkstra_backwards(grid, end, width, height)
    print(min_distance)


def dijkstra(grid: list[list[int]], start: Point, end: Point, width: int, height: int):
    visited = set()
    tentative_distance = defaultdict(lambda: sys.maxsize)
    tentative_distance[start] = 0
    heap = [(0, start)]
    steps = 0
    while heap:
        dist, curr = heappop(heap)
        x, y = curr
        z = grid[y][x]

        steps += 1

        if curr == end:
            return dist

        visited.add(curr)

        for candidate in candidate_points(curr, width, height):
            if candidate not in visited and grid[candidate.y][candidate.x] <= z + 1:
                if dist + 1 < tentative_distance[candidate]:
                    tentative_distance[candidate] = dist + 1
                    heappush(heap, (tentative_distance[candidate], candidate))
    return sys.maxsize


def dijkstra_backwards(grid: list[list[int]], end: Point, width: int, height: int):
    visited = set()
    tentative_distance = defaultdict(lambda: sys.maxsize)
    tentative_distance[end] = 0
    heap = [(0, end)]
    steps = 0
    while heap:
        dist, curr = heappop(heap)
        x, y = curr
        z = grid[y][x]

        steps += 1

        if z == 0:
            return dist

        visited.add(curr)

        for candidate in candidate_points(curr, width, height):
            if candidate not in visited and grid[candidate.y][candidate.x] >= z - 1:
                if dist + 1 < tentative_distance[candidate]:
                    tentative_distance[candidate] = dist + 1
                    heappush(heap, (tentative_distance[candidate], candidate))
    return sys.maxsize


if __name__ == '__main__':
    main()
