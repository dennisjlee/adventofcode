import math
import operator
import sys
from collections import Counter, defaultdict
from functools import reduce


def main():
    with open(sys.argv[1]) as f:
        grid = [
            [int(c) for c in line.strip()]
            for line in f.readlines()
        ]

    low_points = part1(grid)
    print(sum(1 + height for x, y, height in low_points))

    part2(grid, low_points)


def part1(grid: list[list[int]]) -> list[tuple[int,int,int]]:
    low_points = []

    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            val = grid[y][x]
            if y > 0 and val >= grid[y-1][x]:
                continue
            if y < height - 1 and val >= grid[y+1][x]:
                continue
            if x > 0 and val >= grid[y][x-1]:
                continue
            if x < width - 1 and val >= grid[y][x+1]:
                continue
            low_points.append((x, y, val))

    return low_points


def part2(grid: list[list[int]], low_points: list[tuple[int, int, int]]):
    basin_sizes = [explore_basin(grid, x, y, set()) for x, y, val in low_points]
    top_three = sorted(basin_sizes)[-3:]
    print(reduce(operator.mul, top_three, 1))


def explore_basin(grid: list[list[int]], x: int, y: int, visited: set[tuple[int, int]]) -> int:
    height = len(grid)
    width = len(grid[0])
    if (x, y) in visited or x < 0 or x >= width or y < 0 or y >= height or grid[y][x] >= 9:
        return 0

    visited.add((x, y))
    return (1 +
            explore_basin(grid, x - 1, y, visited) +
            explore_basin(grid, x + 1, y, visited) +
            explore_basin(grid, x, y - 1, visited) +
            explore_basin(grid, x, y + 1, visited))


if __name__ == '__main__':
    main()
