import heapq
import math
import sys
import typing


class Point(typing.NamedTuple):
    x: int
    y: int


DIRECTIONS = [Point(0, -1), Point(-1, 0), Point(1, 0), Point(0, 1)]


def main():
    with open(sys.argv[1]) as f:
        grid = [
            [int(c) for c in line.strip()]
            for line in f.readlines()
        ]

    # part 1
    print(dijkstra2(grid))

    # part 2
    width = len(grid[0])
    height = len(grid)
    big_grid = [
        [-1 for x in range(5 * width)]
        for y in range(5 * height)
    ]
    for tile_y in range(5):
        for tile_x in range(5):
            for y in range(height):
                for x in range(width):
                    value = grid[y][x] + tile_y + tile_x
                    big_grid[tile_y * height + y][tile_x * width + x] = (value - 1) % 9 + 1

    print(dijkstra2(big_grid))


def dijkstra(grid):
    width = len(grid[0])
    height = len(grid)

    previous: dict[Point, Point] = {}
    queue = {Point(x, y) for x in range(width) for y in range(height)}
    target = Point(width - 1, height - 1)

    distances = {p: math.inf for p in queue}
    distances[Point(0, 0)] = 0
    while queue:
        curr = min(queue, key=lambda p: distances[p])
        queue.remove(curr)
        if curr == target:
            break

        curr_distance = distances[curr]

        for direction in DIRECTIONS:
            new_pos = Point(curr.x + direction.x, curr.y + direction.y)
            if new_pos in queue:
                alt_distance = curr_distance + grid[new_pos.y][new_pos.x]
                if alt_distance < distances[new_pos]:
                    distances[new_pos] = alt_distance
                    previous[new_pos] = curr

    return distances[target]


def dijkstra2(grid):
    width = len(grid[0])
    height = len(grid)

    previous: dict[Point, Point] = {}
    heap = [(0, Point(0, 0))]
    target = Point(width - 1, height - 1)

    distances = {Point(x, y): math.inf for x in range(width) for y in range(height)}
    distances[Point(0, 0)] = 0
    while heap:
        curr_distance, curr = heapq.heappop(heap)

        if curr == target:
            break

        for direction in DIRECTIONS:
            new_pos = Point(curr.x + direction.x, curr.y + direction.y)
            if 0 <= new_pos.x < width and 0 <= new_pos.y < height:
                alt_distance = curr_distance + grid[new_pos.y][new_pos.x]
                if alt_distance < distances[new_pos]:
                    distances[new_pos] = alt_distance
                    previous[new_pos] = curr
                    heapq.heappush(heap, (alt_distance, new_pos))

    return distances[target]


if __name__ == '__main__':
    main()
