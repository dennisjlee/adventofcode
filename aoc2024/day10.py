import sys
from collections import deque
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def neighbors(self):
        yield Point(self.x - 1, self.y)
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y - 1)
        yield Point(self.x, self.y + 1)

    def in_range(self, w: int, h: int):
        return 0 <= self.x < w and 0 <= self.y < h


class BFSState(NamedTuple):
    point: Point
    value: int
    path: list[Point]


def main():
    with open(sys.argv[1]) as f:
        grid = [[int(c) for c in l.strip()] for l in f.readlines()]

    w = len(grid[0])
    h = len(grid)

    trailheads: list[Point] = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 0:
                trailheads.append(Point(x, y))

    print(sum(trailhead_score(grid, w, h, t) for t in trailheads))
    print(sum(trailhead_rating(grid, w, h, t) for t in trailheads))


def trailhead_score(grid: list[list[int]], w: int, h: int, t: Point) -> int:
    curr_points: set[Point] = {t}
    for target in range(1, 10):
        next_points: set[Point] = set()
        for p in curr_points:
            for n in p.neighbors():
                if n.in_range(w, h) and grid[n.y][n.x] == target:
                    next_points.add(n)
        curr_points = next_points

    return len(curr_points)


def trailhead_rating(grid: list[list[int]], w: int, h: int, t: Point) -> int:
    rating = 0
    q = deque([BFSState(t, 0, [])])
    while q:
        state = q.popleft()
        if state.value == 9:
            rating += 1
        else:
            for n in state.point.neighbors():
                if n.in_range(w, h) and grid[n.y][n.x] == state.value + 1:
                    q.append(BFSState(n, state.value + 1, state.path + [n]))

    return rating


if __name__ == "__main__":
    main()
