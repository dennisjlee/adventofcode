from __future__ import annotations

from math import inf
import sys
from typing import NamedTuple, Optional, Literal
import heapq


class Point(NamedTuple):
    x: int
    y: int


ROCKY = 0   # can use climbing gear or torch
WET = 1     # can use climbing gear or nothing
NARROW = 2  # can use torch or nothing

Tool = Literal[0, 1, 2]

# Values of tools chosen so that at a given ROCKY/WET/NARROW risk level,
# the banned tool choice is the one that equals the risk level
NOTHING: Tool = 0
TORCH: Tool = 1
CLIMBING_GEAR: Tool = 2



def manhattan_distance(p1: Point, p2: Point):
    return abs(p1.y - p2.y) + abs(p1.x - p2.x)


class State(NamedTuple):
    heuristic: int
    time_taken: int
    point: Point
    tool: Tool
    visited: set[Point]

    @staticmethod
    def create(time_taken: int, point: Point, tool: Tool, visited: set[Point], target: Point):
        heuristic = time_taken + manhattan_distance(point, target)
        if tool != TORCH:
            # we'll eventually have to change back to the torch at the target
            heuristic += 7
        return State(heuristic, time_taken, point, tool, visited)


def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    depth = int(lines[0].split(': ')[1])
    target_x, target_y = lines[1].split(': ')[1].split(',')
    target = Point(int(target_x), int(target_y))

    # TEST CASE
    depth, target = 510, Point(10, 10)

    width = target.x + 1
    height = target.y + 1

    mod_base = 20183

    width_bound = max(1000, width * 2)
    height_bound = max(1000, height * 2)

    risk_levels = calculate_risk_levels(target, depth, mod_base, height_bound, width_bound)

    # part 1
    print(sum(sum(risk_levels[y][x] for x in range(width))
              for y in range(height)))

    print(part2(target, risk_levels, height_bound, width_bound))


def part2(target, risk_levels, height_bound, width_bound):
    start = Point(0, 0)
    heap = [State.create(0, start, TORCH, set(), target)]
    i = 0
    best_result: dict[tuple[Point, Tool], int] = {}
    while heap:
        state = heapq.heappop(heap)
        if i % 100_000 == 0:
            print(f'step {i}, heap size {len(heap)}')
        i += 1

        result_key = (state.point, state.tool)
        if best_result.get(result_key, inf) > state.time_taken:
            best_result[result_key] = state.time_taken
        else:
            continue

        p = state.point
        if p == target:
            if state.tool == TORCH:
                return state.time_taken
            else:
                heapq.heappush(heap, State.create(
                    state.time_taken + 7, target, TORCH, state.visited, target))
                continue

        def try_neighbor(n: Point):
            if n in state.visited:
                return

            new_risk = risk_levels[n.y][n.x]
            new_tool = state.tool
            new_time = state.time_taken + 1
            if state.tool == new_risk:
                # We can't use the current tool in the new location.
                # Use a trick to compute the tool that can be used in both
                # current risk level and new risk level
                current_risk = risk_levels[p.y][p.x]
                new_tool = (current_risk + current_risk - new_risk) % 3
                new_time += 7

            heapq.heappush(heap, State.create(new_time, n, new_tool, new_visited, target))

        new_visited = state.visited | {p}
        if p.x > 0:
            try_neighbor(Point(p.x - 1, p.y))
        if p.x < width_bound - 1:
            try_neighbor(Point(p.x + 1, p.y))
        if p.y > 0:
            try_neighbor(Point(p.x, p.y - 1))
        if p.y < height_bound - 1:
            try_neighbor(Point(p.x, p.y + 1))


def calculate_risk_levels(target: Point, depth: int, mod_base: int, height_bound: int, width_bound: int):
    geologic_indices: list[list[Optional[int]]] = [
        [None] * width_bound
        for _ in range(height_bound)
    ]
    erosion_levels: list[list[Optional[int]]] = [
        [None] * width_bound
        for _ in range(height_bound)
    ]

    def calc_erosion(ey: int, ex: int):
        erosion_levels[ey][ex] = (geologic_indices[ey][ex] + depth) % mod_base

    geologic_indices[0][0] = 0
    calc_erosion(0, 0)
    geologic_indices[target.y][target.x] = 0
    calc_erosion(target.y, target.x)
    for x in range(1, width_bound):
        geologic_indices[0][x] = x * 16807
        calc_erosion(0, x)
    for y in range(1, height_bound):
        geologic_indices[y][0] = y * 48271
        calc_erosion(y, 0)
    for y in range(1, height_bound):
        for x in range(1, width_bound):
            if y == target.y and x == target.x:
                continue
            geologic_indices[y][x] = erosion_levels[y - 1][x] * erosion_levels[y][x - 1]
            calc_erosion(y, x)
    risk_levels: list[list[int]] = [
        [erosion_levels[y][x] % 3 for x in range(width_bound)]
        for y in range(height_bound)
    ]
    return risk_levels


if __name__ == '__main__':
    main()
