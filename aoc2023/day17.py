from __future__ import annotations

import sys
from collections import defaultdict
from heapq import heappop, heappush
from typing import NamedTuple, Iterable


class Point(NamedTuple):
    x: int
    y: int


class Vector(NamedTuple):
    x: int
    y: int


Grid = list[list[int]]

Loc = tuple[Point, Vector, int]


class State(NamedTuple):
    loss: int
    point: Point
    vector: Vector
    straight_moves_left: int

    def successor_states(self, grid: Grid, width: int, height: int) -> Iterable[State]:
        new_x = self.point.x + self.vector.x
        new_y = self.point.y + self.vector.y
        if 0 <= new_x < width and 0 <= new_y < height:
            new_loss = self.loss + grid[new_y][new_x]
            if self.straight_moves_left > 1:
                if 0 <= new_x + self.vector.x < width and 0 <= new_y + self.vector.y < height:
                    yield State(new_loss, Point(new_x, new_y), self.vector, self.straight_moves_left - 1)

            for new_vec in ROTATIONS[self.vector]:
                if 0 <= new_x + new_vec.x < width and 0 <= new_y + new_vec.y < height:
                    yield State(new_loss, Point(new_x, new_y), new_vec, 3)

    @property
    def loc(self) -> Loc:
        return self.point, self.vector, self.straight_moves_left


NORTH = Vector(0, -1)
SOUTH = Vector(0, 1)
WEST = Vector(-1, 0)
EAST = Vector(1, 0)

ROTATIONS = {
    NORTH: [EAST, WEST],
    SOUTH: [EAST, WEST],
    WEST: [NORTH, SOUTH],
    EAST: [NORTH, SOUTH],
}


def dijkstra_grid(grid: Grid, start: Point, end: Point, width: int, height: int):
    heap = [State(0, start, EAST, 3), State(0, start, SOUTH, 3)]
    visited: set[Loc] = set()
    tentative_distance: dict[Loc, int] = defaultdict(lambda: sys.maxsize)
    for state in heap:
        loc = state.loc
        visited.add(loc)
        tentative_distance[loc] = 0

    step = 0
    while heap:
        curr: State = heappop(heap)

        step += 1
        if curr.point == end:
            print(f'Solved! step: {step}, heap size {len(heap)}')
            return curr.loss

        visited.add(curr.loc)

        for candidate in curr.successor_states(grid, width, height):
            if candidate.loc not in visited:
                if candidate.loss < tentative_distance[candidate.loc]:
                    tentative_distance[candidate.loc] = candidate.loss
                    heappush(heap, candidate)
    return sys.maxsize


class Node:
    x: int
    y: int
    raw_loss: int
    dir: str
    edges_out: list[tuple[Node, int]]

    def __init__(self, x: int, y: int, raw_loss: int, dir: str):
        self.x = x
        self.y = y
        self.raw_loss = raw_loss
        self.dir = dir
        self.edges_out = []

    def add_edge(self, dest: Node, weight: int):
        self.edges_out.append((dest, weight))

    def __repr__(self):
        return f'Node(x={self.x},y={self.y},raw_loss={self.raw_loss},dir={self.dir},' + \
            f'edges_out=[{", ".join(o.summarize() for (o, _) in self.edges_out)}])'

    def summarize(self):
        return f'({self.x},{self.y},{self.dir})'

    def __lt__(self, other: Node):
        return (self.x, self.y, self.raw_loss, id(self)) < (other.x, other.y, other.raw_loss, id(other))


class Graph:
    horizontal_nodes: list[list[Node]]
    vertical_nodes: list[list[Node]]
    start: Node
    end: Node

    def __init__(self, horizontal_nodes: list[list[Node]], vertical_nodes: list[list[Node]], start: Node, end: Node):
        self.horizontal_nodes = horizontal_nodes
        self.vertical_nodes = vertical_nodes
        self.start = start
        self.end = end


def construct_unconnected_graph(grid: Grid) -> Graph:
    height = len(grid)
    width = len(grid[0])
    horizontal = [
        [Node(x, y, grid[y][x], 'H') for x in range(width)]
        for y in range(height)
    ]
    vertical = [
        [Node(x, y, grid[y][x], 'V') for x in range(width)]
        for y in range(height)
    ]
    start = Node(-1, -1, 0, '')
    end = Node(width, height, 0, '')

    start.add_edge(horizontal[0][0], 0)
    start.add_edge(vertical[0][0], 0)
    horizontal[height - 1][width - 1].add_edge(end, 0)
    vertical[height - 1][width - 1].add_edge(end, 0)

    return Graph(horizontal, vertical, start, end)


def construct_graph_part1(grid: Grid) -> Graph:
    graph = construct_unconnected_graph(grid)
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        for x in range(width):
            curr = graph.horizontal_nodes[y][x]
            cumulative_loss = 0
            for new_x in range(x + 1, min(x + 4, width)):
                dest = graph.vertical_nodes[y][new_x]
                cumulative_loss += dest.raw_loss
                curr.add_edge(dest, cumulative_loss)
            cumulative_loss = 0
            for new_x in range(x - 1, max(x - 4, -1), -1):
                dest = graph.vertical_nodes[y][new_x]
                cumulative_loss += dest.raw_loss
                curr.add_edge(dest, cumulative_loss)

            curr = graph.vertical_nodes[y][x]
            cumulative_loss = 0
            for new_y in range(y + 1, min(y + 4, height)):
                dest = graph.horizontal_nodes[new_y][x]
                cumulative_loss += dest.raw_loss
                curr.add_edge(dest, cumulative_loss)
            cumulative_loss = 0
            for new_y in range(y - 1, max(y - 4, -1), -1):
                dest = graph.horizontal_nodes[new_y][x]
                cumulative_loss += dest.raw_loss
                curr.add_edge(dest, cumulative_loss)

    return graph


def construct_graph_part2(grid: Grid) -> Graph:
    graph = construct_unconnected_graph(grid)
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        for x in range(width):
            curr = graph.horizontal_nodes[y][x]
            cumulative_loss = 0
            for new_x in range(x + 1, min(x + 11, width)):
                dest = graph.vertical_nodes[y][new_x]
                cumulative_loss += dest.raw_loss
                if new_x >= x + 4:
                    curr.add_edge(dest, cumulative_loss)
            cumulative_loss = 0
            for new_x in range(x - 1, max(x - 11, -1), -1):
                dest = graph.vertical_nodes[y][new_x]
                cumulative_loss += dest.raw_loss
                if new_x <= x - 4:
                    curr.add_edge(dest, cumulative_loss)

            curr = graph.vertical_nodes[y][x]
            cumulative_loss = 0
            for new_y in range(y + 1, min(y + 11, height)):
                dest = graph.horizontal_nodes[new_y][x]
                cumulative_loss += dest.raw_loss
                if new_y >= y + 4:
                    curr.add_edge(dest, cumulative_loss)
            cumulative_loss = 0
            for new_y in range(y - 1, max(y - 11, -1), -1):
                dest = graph.horizontal_nodes[new_y][x]
                cumulative_loss += dest.raw_loss
                if new_y <= y - 4:
                    curr.add_edge(dest, cumulative_loss)

    return graph


def dijkstra_graph(graph: Graph):
    heap = [(0, graph.start, [(0, graph.start)])]
    visited: set[Node] = {graph.start}
    tentative_distance: dict[Node, int] = defaultdict(lambda: sys.maxsize)

    step = 0
    while heap:
        item: tuple[int, Node, tuple[int, list[Node]]] = heappop(heap)
        cost, curr, path = item

        step += 1
        if curr == graph.end:
            print(f'Solved! step: {step}, heap size {len(heap)}')
            return cost

        visited.add(curr)

        for neighbor, incremental_cost in curr.edges_out:
            if neighbor not in visited:
                new_cost = cost + incremental_cost
                if new_cost < tentative_distance[neighbor]:
                    tentative_distance[neighbor] = new_cost
                    heappush(heap, (new_cost, neighbor, path + [(new_cost, neighbor)]))
    return sys.maxsize


def main():
    with open(sys.argv[1]) as f:
        grid = [
            [int(c) for c in s.strip()]
            for s in f.readlines()
        ]

    # part 1
    height = len(grid)
    width = len(grid[0])

    print(dijkstra_grid(grid, Point(0, 0), Point(width - 1, height - 1), width, height))

    graph1 = construct_graph_part1(grid)
    print(dijkstra_graph(graph1))

    # part 2
    graph2 = construct_graph_part2(grid)
    print(dijkstra_graph(graph2))


if __name__ == '__main__':
    main()
