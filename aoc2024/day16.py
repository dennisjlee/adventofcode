from __future__ import annotations

import sys
from collections import defaultdict
from heapq import heappop, heappush
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Vector(NamedTuple):
    dx: int
    dy: int

Grid = list[list[str]]

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


class Node:
    point: Point
    vector: Vector
    edges_out: list[tuple[Node, int]]

    def __init__(self, point: Point, vector: Vector):
        self.point = point
        self.vector = vector
        self.edges_out = []

    def add_edge(self, dest: Node, weight: int):
        self.edges_out.append((dest, weight))

    def __repr__(self):
        return f'Node(point={self.point},vector={self.vector},' + \
            f'edges_out=[{", ".join(o.summarize() for (o, _) in self.edges_out)}])'

    def summarize(self):
        return f'({self.point.x},{self.point.y},{self.vector.dx},{self.vector.dy})'


class Graph:
    maze_nodes: dict[Point, dict[Vector, set[Node]]]
    start: Node
    end: Node

    def __init__(self, maze_nodes: dict[Point, dict[Vector, set[Node]]], start: Node, end: Node):
        self.maze_nodes = maze_nodes
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
