from __future__ import annotations

from functools import cached_property
import heapq
import math
import sys
from collections import Counter, deque
from enum import Enum
from typing import NamedTuple, Optional, Iterable


Grid = tuple[tuple[str]]


class Point(NamedTuple):
    x: int
    y: int


class State(NamedTuple):
    heuristic: int
    step: int
    point: Point


def manhattan_distance(p1: Point, p2: Point):
    return abs(p1.y - p2.y) + abs(p1.x - p2.x)


def heuristic(step: int, point: Point, end: Point):
    return step + manhattan_distance(point, end)


def make_state(curr_point: Point, end_point: Point, step: int) -> State:
    return State(heuristic(step, curr_point, end_point), step, curr_point)


def main():
    with open(sys.argv[1]) as f:
        initial_board: list[list[str]] = [list(line.strip()) for line in f.readlines()]

    grid: Grid = tuple(
        tuple(
            initial_board[y][x] if initial_board[y][x] != '.' else ''
            for x in range(1, len(initial_board[y]) - 1)
        )
        for y in range(1, len(initial_board) - 1)
    )

    height = len(grid)
    width = len(grid[0])

    start_point = Point(0, -1)
    start_adjacent = Point(0, 0)
    end_point = Point(width - 1, height)
    end_adjacent = Point(width - 1, height - 1)

    grid_cache = {0: grid}
    for i in range(1, 601):
        get_grid(grid_cache, i, height, width)

    # part 1
    there_state = a_star(grid, grid_cache, height, width, start_point, end_adjacent)
    there_step = there_state.step + 1
    print(there_step)

    grid2 = get_grid(grid_cache, there_step, height, width)
    and_back_state = a_star(grid2, grid_cache, height, width, end_point, start_adjacent, there_step)
    and_back_step = and_back_state.step + 1

    grid3 = get_grid(grid_cache, and_back_step, height, width)
    and_there_again_state = a_star(grid3, grid_cache, height, width, start_point, end_adjacent, and_back_step)
    and_there_again_step = and_there_again_state.step + 1

    print(there_step, and_back_step, and_there_again_step)


def a_star(grid, grid_cache, height, width, start_point, end_point, start_step=0):
    heap = [make_state(start_point, end_point, start_step)]

    visited = {
        (start_point, grid)
    }

    def push_state(new_step: int, new_grid: Grid, new_point: Point):
        visited_marker = (new_point, new_grid)
        if visited_marker not in visited:
            visited.add(visited_marker)
            heapq.heappush(heap, make_state(new_point, end_point, new_step))

    while heap:
        state = heapq.heappop(heap)
        next_step = state.step + 1
        next_grid = get_grid(grid_cache, next_step, height, width)
        p = state.point
        if p == end_point:
            # destination!
            return state

        if p != start_point:
            # assuming start_point is always at y == -1 or y == height
            if p.x > 0 and p.y >= 0:
                if not next_grid[p.y][p.x - 1]:
                    push_state(next_step, next_grid, Point(p.x - 1, p.y))
            if p.x < width - 1 and p.y >= 0:
                if not next_grid[p.y][p.x + 1]:
                    push_state(next_step, next_grid, Point(p.x + 1, p.y))
        if p.y > 0:
            if not next_grid[p.y - 1][p.x]:
                push_state(next_step, next_grid, Point(p.x, p.y - 1))
        if p.y < height - 1:
            if not next_grid[p.y + 1][p.x]:
                push_state(next_step, next_grid, Point(p.x, p.y + 1))

        if p == start_point or not next_grid[p.y][p.x]:
            push_state(next_step, next_grid, p)


def get_grid(grid_cache: dict[int, Grid], step: int, height: int, width: int) -> Grid:
    step = step % math.lcm(height, width)
    if step not in grid_cache:
        grid = grid_cache[step - 1]
        new_grid = [
            [[] for x in range(width)]
            for y in range(height)
        ]
        for y in range(height):
            for x in range(width):
                blizzards = grid[y][x]
                if '>' in blizzards:
                    new_grid[y][(x + 1) % width].append('>')
                if '<' in blizzards:
                    new_grid[y][(x - 1) % width].append('<')
                if '^' in blizzards:
                    new_grid[(y - 1) % height][x].append('^')
                if 'v' in blizzards:
                    new_grid[(y + 1) % height][x].append('v')

        grid_cache[step] = tuple(
            tuple(''.join(sorted(new_grid[y][x])) for x in range(width))
            for y in range(height)
        )
    return grid_cache[step]


if __name__ == '__main__':
    main()
