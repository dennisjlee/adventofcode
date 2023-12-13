from __future__ import annotations

import sys


def find_vertical_reflection(grid: list[list[str]], error_goal=0) -> int | None:
    height = len(grid)
    width = len(grid[0])
    for x in range(width - 1):
        errors = 0
        for dx in range(min(x + 1, width - x - 1)):
            errors += sum(1 for y in range(height) if grid[y][x - dx] != grid[y][x + dx + 1])
            if errors > error_goal:
                break

        if errors == error_goal:
            return x

    return None


def find_horizontal_reflection(grid: list[list[str]], error_goal=0) -> int | None:
    height = len(grid)
    width = len(grid[0])

    for y in range(height - 1):
        errors = 0
        for dy in range(min(y + 1, height - y - 1)):
            errors += sum(1 for x in range(width) if grid[y - dy][x] != grid[y + dy + 1][x])
            if errors > error_goal:
                break

        if errors == error_goal:
            return y

    return None


def parse_grid(grid_string: str) -> list[list[str]]:
    return [list(line) for line in grid_string.strip().split('\n')]


def summarize_grids(grids: list[list[list[str]]], error_goal: int) -> int:
    total = 0
    for i, grid in enumerate(grids):
        vertical_reflection_index = find_vertical_reflection(grid, error_goal)
        if vertical_reflection_index is not None:
            total += vertical_reflection_index + 1
        else:
            horizontal_reflection_index = find_horizontal_reflection(grid, error_goal)
            if horizontal_reflection_index is not None:
                total += 100 * (horizontal_reflection_index + 1)
            else:
                raise Exception(f'could not find a reflection for grid {i}!')
    return total


def main():
    with open(sys.argv[1]) as f:
        grid_strings = f.read().split('\n\n')

    grids = [parse_grid(grid_string) for grid_string in grid_strings]

    print(summarize_grids(grids, 0))
    print(summarize_grids(grids, 1))


if __name__ == '__main__':
    main()
