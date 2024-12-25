from __future__ import annotations

import sys
from collections import defaultdict, deque
from heapq import heappop, heappush
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    @staticmethod
    def parse(s: str) -> Point:
        x_str, y_str = s.strip().split(",")
        return Point(int(x_str), int(y_str))

    def neighbors(self):
        yield Point(self.x - 1, self.y)
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y - 1)
        yield Point(self.x, self.y + 1)

    def in_range(self, w: int, h: int):
        return 0 <= self.x < w and 0 <= self.y < h


def main():
    with open(sys.argv[1]) as f:
        obstacles = [Point.parse(line) for line in f.readlines()]

    # part1
    obstacle_set = set(obstacles[:1024])
    w = h = 71
    start = Point(0, 0)
    end = Point(70, 70)
    heap = [(0, start)]
    tentative_distance: dict[Point, int] = defaultdict(lambda: sys.maxsize)
    tentative_distance[start] = 0
    while heap:
        item: tuple[int, Point] = heappop(heap)
        cost, curr = item
        if curr == end:
            print(cost)
            break
        for n in curr.neighbors():
            if n.in_range(w, h) and n not in obstacle_set:
                new_cost = cost + 1
                if new_cost < tentative_distance[n]:
                    tentative_distance[n] = new_cost
                    heappush(heap, (new_cost, n))

    for i, obstacle in enumerate(obstacles[1025:]):
        obstacle_set.add(obstacle)
        if not can_reach_end(obstacle_set, start, end, w, h):
            print(1025 + i, f"{obstacle.x},{obstacle.y}")
            break


def can_reach_end(obstacle_set: set[Point], start: Point, end: Point, w: int, h: int):
    visited = {start}
    q: deque[Point] = deque([start])
    while q:
        p = q.popleft()
        if p == end:
            break
        for n in p.neighbors():
            if n.in_range(w, h) and n not in visited and n not in obstacle_set:
                visited.add(n)
                q.append(n)
    return end in visited


if __name__ == "__main__":
    main()
