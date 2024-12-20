from __future__ import annotations
import sys
from collections import deque, defaultdict, Counter
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

    def manhattan_distance(self, other: Point):
        return abs(other.x - self.x) + abs(other.y - self.y)


class PathPoint(NamedTuple):
    index: int
    point: Point

    def cheat_savings1(self, other: PathPoint) -> int:
        cheat_dist = self.point.manhattan_distance(other.point)
        if cheat_dist <= 2:
            normal_dist = abs(other.index - self.index)
            if cheat_dist < normal_dist:
                return normal_dist - cheat_dist
        return 0

    def cheat_savings2(self, other: PathPoint) -> int:
        cheat_dist = self.point.manhattan_distance(other.point)
        if cheat_dist <= 20:
            normal_dist = abs(other.index - self.index)
            if cheat_dist < normal_dist:
                return normal_dist - cheat_dist
        return 0


def main():
    with open(sys.argv[1]) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    h = len(grid)
    w = len(grid[0])
    start: Point | None = None
    end: Point | None = None
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "S":
                start = Point(x, y)
            elif grid[y][x] == "E":
                end = Point(x, y)
        if start and end:
            break
    assert start and end

    path = get_basic_path(grid, w, h, start, end)
    path_points = [PathPoint(i, point) for i, point in enumerate(path)]

    path_points_by_x: dict[int, list[PathPoint]] = defaultdict(list)
    for pp in path_points:
        path_points_by_x[pp.point.x].append(pp)

    potential_good_cheats = 0
    cheat_counter = Counter()
    for pp in path_points:
        for potential_x in range(pp.point.x - 2, pp.point.x + 3):
            for other in path_points_by_x[potential_x]:
                if other.index > pp.index:
                    savings = pp.cheat_savings1(other)
                    if savings:
                        cheat_counter[savings] += 1
                    if savings >= 100:
                        potential_good_cheats += 1

    print(potential_good_cheats)

    potential_good_cheats = 0
    for pp in path_points:
        for potential_x in range(pp.point.x - 20, pp.point.x + 21):
            for other in path_points_by_x[potential_x]:
                if other.index > pp.index:
                    savings = pp.cheat_savings2(other)
                    if savings >= 100:
                        potential_good_cheats += 1

    print(potential_good_cheats)


def get_basic_path(grid: list[list[str]], w: int, h: int, start: Point, end: Point):
    q: deque[tuple[list[Point], set[Point]]] = deque([([start], {start})])
    while q:
        path, visited = q.pop()
        for n in path[-1].neighbors():
            if n == end:
                return path + [end]
            if n.in_range(w, h) and grid[n.y][n.x] == "." and n not in path:
                q.append((path + [n], visited | {n}))


if __name__ == "__main__":
    main()
