from __future__ import annotations

import math
from copy import deepcopy
from collections import deque, defaultdict
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


def manhattan_distance(p1: Point, p2: Point):
    return abs(p1.y - p2.y) + abs(p1.x - p2.x)


# def estimated_distance(p: Point):
#     z = grid[p.y][p.x]
#     if z == 0:
#         return manhattan_distance(p, start)
#     points_below = locations_by_z[z - 1]
#     best_dist = math.inf
#     best = None
#     for pb in points_below:
#         dist = manhattan_distance(p, pb)
#         if dist < best_dist:
#             best_dist = dist
#             best = pb
#     return best_dist + estimated_distance(best)


def main():
    with open(sys.argv[1]) as f:
        raw_grid = [list(line.strip()) for line in f.readlines()]

    # dijkstra(raw_grid)
    a_star(raw_grid)

def dijkstra(raw_grid):
    height = len(raw_grid)
    width = len(raw_grid[0])
    start: Optional[Point] = None
    end: Optional[Point] = None

    print(f'grid is {height} x {width}')

    grid = [
        [0] * width
        for _ in range(height)
    ]

    visited = set()
    tentative_distance = {}
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
            grid[y][x] = z
            p = Point(x, y)
            tentative_distance[p] = math.inf

    tentative_distance[start] = 0
    heap = [(0, start)]
    steps = 0
    while heap:
        dist, curr = heappop(heap)
        x, y = curr
        z = grid[y][x]
        candidate_points = []

        steps += 1
        if steps % 1000 == 0:
            print(f'step: {steps}, # of states: {len(heap)}, z: {z}, dist: {dist}, visited #: {len(visited)}')

        if curr == end:
            print(dist, f'(steps: {steps})')
            break

        if x > 0:
            candidate_points.append(Point(x - 1, y))

        if x < width - 1:
            candidate_points.append(Point(x + 1, y))

        if y > 0:
            candidate_points.append(Point(x, y - 1))

        if y < height - 1:
            candidate_points.append(Point(x, y + 1))

        visited.add(curr)

        for candidate in candidate_points:
            if candidate not in visited and grid[candidate.y][candidate.x] <= z + 1:
                if dist + 1 < tentative_distance[candidate]:
                    tentative_distance[candidate] = dist + 1
                heappush(heap, (tentative_distance[candidate], candidate))


def a_star(raw_grid):
    height = len(raw_grid)
    width = len(raw_grid[0])
    start: Optional[Point] = None
    end: Optional[Point] = None

    print(f'grid is {height} x {width}')

    grid = [
        [0] * width
        for _ in range(height)
    ]

    locations_by_z = defaultdict(set)
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
            grid[y][x] = z
            locations_by_z[z].add(Point(x, y))

    distance_estimates: dict[Point, int] = {}
    for p in locations_by_z[0]:
        distance_estimates[p] = manhattan_distance(p, start)
    for z in range(1, 26):
        for p1 in locations_by_z[z]:
            candidates = [(manhattan_distance(p1, p2), p2) for p2 in locations_by_z[z-1]]
            dist, p2 = min(candidates)
            distance_estimates[p1] = dist + distance_estimates[p2]

    # for y in range(height):
    #     print([distance_estimates[Point(x, y)] for x in range(width)])


    forward = False
    if forward:
        def forward_heuristic(p: Point, path_len: int):
            z = grid[p.y][p.x]
            return path_len + max(25 - z, manhattan_distance(p, end))

        states = [State(forward_heuristic(start, 0), start, {start})]
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
                print(len(visited) - 1, 'steps:', steps)
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
                    heappush(states, State(forward_heuristic(candidate, len(visited)), candidate, visited | {candidate}))
    else:
        def backward_heuristic(p: Point, path_len: int):
            return path_len + distance_estimates[p]

        states = [State(backward_heuristic(end, 0), end, {end})]
        heapify(states)
        steps = 0
        while states:
            state = heappop(states)
            steps += 1
            x, y = state.current
            z = grid[y][x]
            if steps % 1000 == 0:
                print(
                    f'step: {steps}, # of states: {len(states)}, z: {z}, cost: {state.cost}, path len: {len(state.visited)}')
            visited = state.visited

            if start.x == x and start.y == y:
                print(len(visited) - 1, f'(steps: {steps})')
                break

            candidate_points = []
            if x > 0:
                candidate_points.append(Point(x - 1, y))

            if x < width - 1:
                candidate_points.append(Point(x + 1, y))

            if y > 0:
                candidate_points.append(Point(x, y - 1))

            if y < height - 1:
                candidate_points.append(Point(x, y + 1))

            for candidate in candidate_points:
                if candidate not in visited and grid[candidate.y][candidate.x] >= z - 1:
                    heappush(states, State(backward_heuristic(candidate, len(visited)), candidate, visited | {candidate}))


if __name__ == '__main__':
    main()
