from __future__ import annotations

import math
from copy import deepcopy
from collections import deque
from heapq import heapify, heappop, heappush
from typing import NamedTuple, Optional
import re
import sys


class Point(NamedTuple):
    x: int
    y: int


class State(NamedTuple):
    cost: int
    current: Point
    visited: set[Point]

# def search(grid: list[list[int]], path: list[Point], end: Point, visited: list[list[bool]], width: int, height: int):
#     x, y = path[-1]
#     z = grid[y][x]
#
#     if end.x == x and end.y == y:
#         return path
#
#     candidate_points = []
#     if x > 0 and grid[y][x-1] <= z + 1 and not visited[y][x-1]:
#         candidate_points.append(Point(x-1, y))
#
#     if x < width - 1 and grid[y][x+1] <= z + 1 and not visited[y][x+1]:
#         candidate_points.append(Point(x+1, y))
#
#     if y > 0 and grid[y-1][x] <= z + 1 and not visited[y-1][x]:
#         candidate_points.append(Point(x, y-1))
#
#     if y < height - 1 and grid[y+1][x] <= z + 1 and not visited[y+1][x]:
#         candidate_points.append(Point(x, y+1))
#
#     visited[y][x] = True
#     for candidate in sorted(candidate_points, key=lambda p: grid[p.y][p.x], reverse=True):
#         candidate_path = search(grid, [*path, candidate], end, visited, width, height)
#         if candidate_path:
#             return candidate_path
#     visited[y][x] = False


def main():
    with open(sys.argv[1]) as f:
        raw_grid = [list(line.strip()) for line in f.readlines()]

    height = len(raw_grid)
    width = len(raw_grid[0])
    start: Optional[Point] = None
    end: Optional[Point] = None

    print(f'grid is {height} x {width}')

    grid = [
        [0] * width
        for _ in range(height)
    ]
    visited = [
        [False] * width
        for _ in range(height)
    ]

    for y in range(height):
        for x in range(width):
            if raw_grid[y][x] == 'S':
                start = Point(x, y)
                grid[y][x] = 0
            elif raw_grid[y][x] == 'E':
                end = Point(x, y)
                grid[y][x] = 25
            else:
                grid[y][x] = ord(raw_grid[y][x]) - ord('a')
    #
    # path = search(grid, [start], end, visited, width, height)
    # print(len(path), path)

    def heuristic(p: Point, path_len: int):
        z = grid[p.y][p.x]
        manhattan_distance = abs(end.y - p.y) + abs(end.x - p.x)
        return path_len + max(25 - z, manhattan_distance)

    states = [State(heuristic(start, 0), start, {start})]
    heapify(states)
    steps = 0
    while states:
        state = heappop(states)
        steps += 1
        if steps % 1000 == 0:
            print(f'step: {steps}, # of states: {len(states)}, current cost: {state.cost}, path len: {len(state.visited)}')
        x, y = state.current
        z = grid[y][x]
        visited = state.visited

        if end.x == x and end.y == y:
            print(len(visited) - 1)
            break

        candidate_points = []
        if x > 0 and grid[y][x - 1] <= z + 1:
            candidate_points.append(Point(x - 1, y))

        if x < width - 1 and grid[y][x + 1] <= z + 1:
            candidate_points.append(Point(x + 1, y))

        if y > 0 and grid[y - 1][x] <= z + 1:
            candidate_points.append(Point(x, y - 1))

        if y < height - 1 and grid[y + 1][x] <= z + 1:
            candidate_points.append(Point(x, y + 1))

        for candidate in candidate_points:
            if candidate not in visited:
                heappush(states, State(heuristic(candidate, len(visited)), candidate, visited | {candidate}))


if __name__ == '__main__':
    main()
