from __future__ import annotations

import sys
import copy
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def manhattan_distance(p1: Point, p2: Point):
    return abs(p1.y - p2.y) + abs(p1.x - p2.x)


def modified_manhattan_distance(p1: Point, p2: Point, empty_xs: list[int], empty_ys: list[int]):
    distance = manhattan_distance(p1, p2)
    min_y = min(p1.y, p2.y)
    max_y = max(p1.y, p2.y)
    min_x = min(p1.x, p2.x)
    max_x = max(p1.x, p2.x)

    for y in empty_ys:
        if min_y < y < max_y:
            distance += 999_999

    for x in empty_xs:
        if min_x < x < max_x:
            distance += 999_999

    return distance


def empty_row_indices(grid: list[list[str]]):
    for y, row in enumerate(grid):
        if all(cell == '.' for cell in row):
            yield y


def empty_col_indices(grid: list[list[str]]):
    for x in range(len(grid[0])):
        if all(grid[y][x] == '.' for y in range(len(grid))):
            yield x


def main():
    with open(sys.argv[1]) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    empty_ys = list(empty_row_indices(grid))
    empty_xs = list(empty_col_indices(grid))

    part1(grid, empty_xs, empty_ys)
    part2(grid, empty_xs, empty_ys)


def part1(grid: list[list[str]], empty_xs: list[int], empty_ys: list[int]):
    part1_grid = copy.deepcopy(grid)

    for y in reversed(empty_ys):
        part1_grid.insert(y, ['.'] * len(part1_grid[0]))

    for x in reversed(empty_xs):
        for row in part1_grid:
            row.insert(x, '.')

    galaxies: list[Point] = []
    for y, row in enumerate(part1_grid):
        for x, char in enumerate(row):
            if char == '#':
                galaxies.append(Point(x, y))

    shortest_path_sum = 0
    for i, p1 in enumerate(galaxies):
        for j in range(i + 1, len(galaxies)):
            p2 = galaxies[j]
            shortest_path_sum += manhattan_distance(p1, p2)

    print(shortest_path_sum)


def part2(grid: list[list[str]], empty_xs: list[int], empty_ys: list[int]):
    galaxies: list[Point] = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == '#':
                galaxies.append(Point(x, y))

    shortest_path_sum = 0
    for i, p1 in enumerate(galaxies):
        for j in range(i + 1, len(galaxies)):
            p2 = galaxies[j]
            shortest_path_sum += modified_manhattan_distance(p1, p2, empty_xs, empty_ys)

    print(shortest_path_sum)


if __name__ == '__main__':
    main()
