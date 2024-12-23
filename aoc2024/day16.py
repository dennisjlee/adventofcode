from __future__ import annotations

import sys
from collections import defaultdict, deque
from heapq import heappop, heappush
from typing import NamedTuple, Literal


class Point(NamedTuple):
    x: int
    y: int

    def horizontal_neighbors(self):
        yield Point(self.x - 1, self.y)
        yield Point(self.x + 1, self.y)

    def vertical_neighbors(self):
        yield Point(self.x, self.y - 1)
        yield Point(self.x, self.y + 1)

    def in_range(self, w: int, h: int):
        return 0 <= self.x < w and 0 <= self.y < h


class Vector(NamedTuple):
    dx: int
    dy: int


Grid = list[list[str]]

Direction = Literal["H", "V"]


def rotated(direction: Direction) -> Direction:
    return "V" if direction == "H" else "H"


class Node:
    point: Point
    direction: Direction
    edges_out: list[tuple[Node, int]]

    def __init__(self, point: Point, direction: Direction):
        self.point = point
        self.direction = direction
        self.edges_out = []

    @property
    def key(self):
        return self.point, self.direction

    @property
    def rotated_key(self):
        return self.point, rotated(self.direction)

    def add_edge(self, dest: Node, weight: int):
        self.edges_out.append((dest, weight))
        if (self, weight) not in dest.edges_out:
            dest.edges_out.append((self, weight))

    def __repr__(self):
        return (
            f"Node(point={self.point},direction={self.direction},"
            + f'edges_out=[{", ".join(o.summarize() for (o, _) in self.edges_out)}])'
        )

    def summarize(self):
        return f"({self.point.x},{self.point.y},{self.direction})"

    def __lt__(self, other: Node):
        return self.key < other.key


class Graph:
    start_point: Point
    end_point: Point

    nodes: dict[tuple[Point, Direction], Node]

    def __init__(self, start_point: Point, end_point: Point):
        self.start_point = start_point
        self.end_point = end_point
        self.nodes = {}

    def add_node(self, node: Node):
        self.nodes[node.key] = node

    def get_or_add_node(self, point: Point, direction: Direction):
        key = (point, direction)
        if key not in self.nodes:
            self.nodes[key] = Node(point, direction)
        return self.nodes[key]


def construct_graph(grid: Grid) -> Graph:
    h = len(grid)
    w = len(grid[0])

    start: Point | None = None
    end: Point | None = None
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "S":
                start = Point(x, y)
                grid[y][x] = "."
            elif grid[y][x] == "E":
                end = Point(x, y)
                grid[y][x] = "."
        if start and end:
            break

    graph = Graph(start, end)
    q_points: deque[Point] = deque([start])
    visited: set[Point] = set()
    while q_points:
        p = q_points.popleft()
        visited.add(p)
        node_h: Node | None = None
        node_v: Node | None = None
        h_edges: list[Point] = []
        for n in p.horizontal_neighbors():
            if n.in_range(w, h) and grid[n.y][n.x] == ".":
                h_edges.append(n)
                if n not in visited:
                    q_points.append(n)
        if h_edges:
            node_h = graph.get_or_add_node(p, "H")
            for point_neighbor in h_edges:
                node_neighbor = graph.get_or_add_node(point_neighbor, "H")
                node_h.add_edge(node_neighbor, 1)

        v_edges: list[Point] = []
        for n in p.vertical_neighbors():
            if n.in_range(w, h) and grid[n.y][n.x] == ".":
                v_edges.append(n)
                if n not in visited:
                    q_points.append(n)
        if v_edges:
            node_v = graph.get_or_add_node(p, "V")
            for point_neighbor in v_edges:
                node_neighbor = graph.get_or_add_node(point_neighbor, "V")
                node_v.add_edge(node_neighbor, 1)

        if node_h and node_v:
            node_h.add_edge(node_v, 1000)

    return graph


def dijkstra_graph(graph: Graph):
    start_node = graph.nodes[(graph.start_point, "H")]
    heap = [(0, [start_node])]
    tentative_distance: dict[Node, int] = defaultdict(lambda: sys.maxsize)
    tentative_distance[start_node] = 0

    step = 0
    best_cost = sys.maxsize
    best_paths: list[list[Node]] = []
    while heap:
        item: tuple[int, list[Node]] = heappop(heap)
        cost, path = item
        curr = path[-1]

        step += 1
        if curr.point == graph.end_point:
            if cost > best_cost:
                break
            else:
                print(f"Solved! step: {step}, heap size {len(heap)}")
                best_cost = cost
                best_paths.append(path)

        for neighbor, incremental_cost in curr.edges_out:
            new_cost = cost + incremental_cost
            if new_cost < tentative_distance[neighbor]:
                tentative_distance[neighbor] = new_cost
                heappush(heap, (new_cost, path + [neighbor]))
    return best_cost, best_paths


# def find_best_path_nodes(graph: Graph, optimal_distances: dict[Node, int]) -> set[Node]:
#     start_node = graph.nodes[(graph.start_point, "H")]
#     q: deque[tuple[int, Node, set[Node]]] = deque([(0, start_node, {start_node})])
#     best_path_nodes = set()
#     step = 0
#     while q:
#         step += 1
#         cost, curr, visited = q.popleft()
#         if curr.point == graph.end_point:
#             best_path_nodes |= visited
#             print(f"Found a path! {best_path_nodes=}, {step=}")
#             continue
#         if step % 10_000 == 0:
#             print(f"Step {step}, queue length {len(q)}")
#         for neighbor, incremental_cost in curr.edges_out:
#             if neighbor not in visited:
#                 new_cost = cost + incremental_cost
#                 if new_cost == optimal_distances[neighbor]:
#                     q.append((new_cost, neighbor, visited | {neighbor}))
#     return best_path_nodes


def main():
    with open(sys.argv[1]) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    # part 1
    graph = construct_graph(grid)

    cost, best_paths = dijkstra_graph(graph)
    print(cost)

    # Wrong, too low
    print(len({n.point for path in best_paths for n in path}))


if __name__ == "__main__":
    main()
