from __future__ import annotations

import sys


def main():
    with open(sys.argv[1]) as f:
        grid = [
            [int(c) for c in line.strip()]
            for line in f.readlines()
        ]

    height = len(grid)
    width = len(grid[0])

    # part 1
    visible = [
        [False] * width
        for __ in range(height)
    ]
    for y in range(height):
        visible[y][0] = True
        visible[y][width - 1] = True

    for x in range(width):
        visible[0][x] = True
        visible[height - 1][x] = True

    for x in range(1, width - 1):
        # from top
        tallest_seen = grid[0][x]
        for y in range(1, height - 1):
            if grid[y][x] > tallest_seen:
                tallest_seen = grid[y][x]
                visible[y][x] = True

        # from bottom
        tallest_seen = grid[height - 1][x]
        for y in range(height - 1, 0, -1):
            if grid[y][x] > tallest_seen:
                tallest_seen = grid[y][x]
                visible[y][x] = True

    for y in range(1, height - 1):
        # from left
        tallest_seen = grid[y][0]
        for x in range(1, width - 1):
            if grid[y][x] > tallest_seen:
                tallest_seen = grid[y][x]
                visible[y][x] = True

        # from bottom
        tallest_seen = grid[y][width - 1]
        for x in range(width - 1, 0, -1):
            if grid[y][x] > tallest_seen:
                tallest_seen = grid[y][x]
                visible[y][x] = True

    print(sum(sum(1 for x in range(width) if visible[y][x])
              for y in range(height)))

    # part 2
    scores = [
        [0] * width
        for __ in range(height)
    ]

    for y in range(height):
        for x in range(width):
            h = grid[y][x]
            left_distance = 0
            for lx in range(x - 1, -1, -1):
                left_distance += 1
                if grid[y][lx] >= h:
                    break

            right_distance = 0
            for rx in range(x + 1, width):
                right_distance += 1
                if grid[y][rx] >= h:
                    break

            up_distance = 0
            for uy in range(y - 1, -1, -1):
                up_distance += 1
                if grid[uy][x] >= h:
                    break

            down_distance = 0
            for dy in range(y + 1, height):
                down_distance += 1
                if grid[dy][x] >= h:
                    break

            scores[y][x] = left_distance * right_distance * up_distance * down_distance

    print(max(max(scores[y][x] for x in range(width))
              for y in range(height)))


if __name__ == '__main__':
    main()
