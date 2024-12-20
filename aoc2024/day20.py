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
    print(len(path), path)

    # TODO: do an O(N^2) loop to see whether point i is <2 manhattan distance from point i+3..end
    # any of those are potential shortcuts, and then we can just subtract the indices to see how much we could save



def get_basic_path(grid: list[list[str]], w: int, h: int, start: Point, end: Point):
    q: deque[tuple[list[Point], set[Point]]] = deque([([start], {start})])
    while q:
        path, visited = q.pop()
        for n in path[-1].neighbors():
            if n == end:
                return path
            if n.in_range(w, h) and grid[n.y][n.x] == "." and n not in path:
                q.append((path + [n], visited | {n}))


if __name__ == "__main__":
    main()
