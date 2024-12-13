import sys
from collections import deque
from dataclasses import dataclass
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


@dataclass
class Plot:
    plant: str
    points: set[Point]
    area: int
    perimeter: int
    edges: int


def main():
    with open(sys.argv[1]) as f:
        grid = [list(l.strip()) for l in f.readlines()]

    w = len(grid[0])
    h = len(grid)

    plots: list[Plot] = []
    visited: set[Point] = set()
    for y in range(h):
        for x in range(w):
            p = Point(x, y)
            if p not in visited:
                plot = bfs(grid, w, h, visited, p)
                plots.append(plot)
    print(sum(plot.area * plot.perimeter for plot in plots))
    print(sum(plot.area * plot.edges for plot in plots))


def bfs(grid: list[list[str]], w: int, h: int, visited: set[Point], p: Point) -> Plot:
    plot = Plot(plant=grid[p.y][p.x], points={p}, area=1, perimeter=0, edges=0)
    visited.add(p)
    q = deque([p])

    edge_points_by_dir: list[set[Point]] = [set(), set(), set(), set()]

    while q:
        p_next = q.popleft()
        for n_index, n in enumerate(p_next.neighbors()):
            if not n.in_range(w, h) or grid[n.y][n.x] != plot.plant:
                plot.perimeter += 1
                edge_points_by_dir[n_index].add(p_next)
            elif grid[n.y][n.x] == plot.plant and n not in visited:
                plot.points.add(n)
                plot.area += 1
                visited.add(n)
                q.append(n)

    for n_index, edge_points in enumerate(edge_points_by_dir):
        visited = set()
        if n_index < 2:  # left or right edge
            for e in sorted(edge_points, key=lambda ep: ep.y):
                if e in visited:
                    continue
                visited.add(e)
                for y in range(e.y + 1, h):
                    next_e = Point(e.x, y)
                    if next_e in edge_points:
                        visited.add(next_e)
                    else:
                        break
                plot.edges += 1
        else:  # top or bottom edge
            for e in sorted(edge_points, key=lambda ep: ep.x):
                if e in visited:
                    continue
                visited.add(e)
                for x in range(e.x + 1, w):
                    next_e = Point(x, e.y)
                    if next_e in edge_points:
                        visited.add(next_e)
                    else:
                        break
                plot.edges += 1

    return plot


if __name__ == "__main__":
    main()
