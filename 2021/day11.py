import sys
from copy import deepcopy
from collections import deque


def main():
    with open(sys.argv[1]) as f:
        grid = [
            [int(c) for c in line.strip()]
            for line in f.readlines()
        ]

    flashes = 0
    for step in range(1000000):
        flashes_in_step = 0
        next_grid = deepcopy(grid)
        height = len(grid)
        width = len(grid[0])

        for y in range(height):
            for x in range(width):
                next_grid[y][x] += 1

        for x, y in find_flash(next_grid, height, width):
            flashes += 1
            flashes_in_step += 1
            next_grid[y][x] = None
            for yy in range(max(0, y - 1), min(y + 2, height)):
                for xx in range(max(0, x - 1), min(x + 2, width)):
                    if next_grid[yy][xx] is not None:
                        next_grid[yy][xx] += 1

        for y in range(height):
            for x in range(width):
                if next_grid[y][x] is None:
                    next_grid[y][x] = 0
        # print('\n'.join(''.join(str(v) for v in row) for row in next_grid), '\n')
        grid = next_grid
        if flashes_in_step == height * width:
            print('All flashed!', step)
            break

    print(flashes)


def find_flash(grid, height, width):
    found_any = True
    while found_any:
        found_any = False
        for y in range(height):
            for x in range(width):
                if grid[y][x] is not None and grid[y][x] > 9:
                    found_any = True
                    yield x, y


if __name__ == '__main__':
    main()
