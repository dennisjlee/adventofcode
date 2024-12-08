import itertools
import sys
from collections import defaultdict
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def in_range(self, w: int, h: int):
        return 0 <= self.x < w and 0 <= self.y < h


def antinode_positions1(p1: Point, p2: Point):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return [Point(p2.x + dx, p2.y + dy), Point(p1.x - dx, p1.y - dy)]


def antinode_positions2(p1: Point, p2: Point, w: int, h: int):
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    x, y = p2
    while 0 <= x < w and 0 <= y < h:
        yield Point(x, y)
        x += dx
        y += dy

    x, y = p1
    while 0 <= x < w and 0 <= y < h:
        yield Point(x, y)
        x -= dx
        y -= dy


def main():
    with open(sys.argv[1]) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    w = len(grid[0])
    h = len(grid)

    nodes: dict[str, list[Point]] = defaultdict(list)
    antinodes1: set[Point] = set()

    for y in range(h):
        for x in range(w):
            if (c := grid[y][x]) != '.':
                nodes[c].append(Point(x, y))

    for c, node_points in nodes.items():
        for p1, p2 in itertools.combinations(node_points, 2):
            for potential_antinode in antinode_positions1(p1, p2):
                if potential_antinode.in_range(w, h):
                    antinodes1.add(potential_antinode)

    print(len(antinodes1))

    antinodes2: set[Point] = set()
    for c, node_points in nodes.items():
        for p1, p2 in itertools.combinations(node_points, 2):
            for potential_antinode in antinode_positions2(p1, p2, w, h):
                antinodes2.add(potential_antinode)

    print(len(antinodes2))


if __name__ == '__main__':
    main()
