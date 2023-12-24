from __future__ import annotations

import sys
from bisect import insort_left
from collections import defaultdict, deque
from typing import NamedTuple, Literal
import re


class Point(NamedTuple):
    x: int
    y: int


class Node(NamedTuple):
    point: Point
    type: str
    edges_out: list[Edge]


class Edge(NamedTuple):
    dest: Node
    weight: int


DELTAS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]

ALLOWED_TYPES_BY_DELTA = {
    (0, 1): {'.', 'v'},
    (0, -1): {'.', '^'},
    (1, 0): {'.', '>'},
    (-1, 0): {'.', '<'},
}


class Graph(NamedTuple):
    start: Node
    end: Node
    all_nodes: list[Node]

    @staticmethod
    def parse1(grid: list[list[str]]) -> Graph:
        height = len(grid)
        width = len(grid[0])
        start = None
        end = None
        nodes_by_point: dict[Point, Node] = {}
        for y in range(height):
            for x in range(width):
                if grid[y][x] != '#':
                    point = Point(x, y)
                    node = Node(point, grid[y][x], [])
                    nodes_by_point[point] = node
                    if y == 0:
                        start = node
                    elif y == height - 1:
                        end = node
        for p, node in nodes_by_point.items():
            if node.type == '.':
                for dx, dy in DELTAS:
                    np = Point(p.x + dx, p.y + dy)
                    neighbor = nodes_by_point.get(np)
                    if neighbor and neighbor.type in ALLOWED_TYPES_BY_DELTA[(dx, dy)]:
                        node.edges_out.append(Edge(neighbor, 1))
            elif node.type == '>':
                node.edges_out.append(Edge(nodes_by_point[Point(p.x + 1, p.y)], 1))
            elif node.type == '<':
                node.edges_out.append(Edge(nodes_by_point[Point(p.x - 1, p.y)], 1))
            elif node.type == '^':
                node.edges_out.append(Edge(nodes_by_point[Point(p.x, p.y - 1)], 1))
            elif node.type == 'v':
                node.edges_out.append(Edge(nodes_by_point[Point(p.x, p.y + 1)], 1))

        return Graph(start, end, list(nodes_by_point.values()))

    @staticmethod
    def parse2(grid: list[list[str]]) -> Graph:
        height = len(grid)
        width = len(grid[0])
        start = None
        end = None
        nodes_by_point: dict[Point, Node] = {}
        for y in range(height):
            for x in range(width):
                if grid[y][x] != '#':
                    point = Point(x, y)
                    node = Node(point, grid[y][x], [])
                    nodes_by_point[point] = node
                    if y == 0:
                        start = node
                    elif y == height - 1:
                        end = node
        for p, node in nodes_by_point.items():
            for dx, dy in DELTAS:
                np = Point(p.x + dx, p.y + dy)
                neighbor = nodes_by_point.get(np)
                if neighbor:
                    node.edges_out.append(Edge(neighbor, 1))

        queue = deque([start])
        visited = {start.point}
        new_start = None
        new_end = None
        new_nodes_by_point: dict[Point, Node] = {}
        while queue:
            source = queue.popleft()
            new_source = new_nodes_by_point.setdefault(source.point, Node(source.point, source.type, []))
            if new_source.point == start.point:
                new_start = new_source
            elif new_source.point == end.point:
                new_end = new_source
            for neighbor, weight in source.edges_out:
                if neighbor.point in visited:
                    continue
                visited.add(neighbor.point)
                # do a DFS in each direction until we get to a node that has more than one edge out
                curr_weight = weight
                prev = source
                curr = neighbor
                while len(curr.edges_out) == 2:
                    edge = next(edge for edge in curr.edges_out if edge.dest != prev)
                    curr_weight += edge.weight
                    prev = curr
                    curr = edge.dest
                    visited.add(curr.point)
                new_dest = new_nodes_by_point.setdefault(curr.point, Node(curr.point, curr.type, []))
                new_dest.edges_out.append(Edge(new_source, curr_weight))
                new_source.edges_out.append(Edge(new_dest, curr_weight))
                queue.append(curr)

        return Graph(new_start, new_end, list(new_nodes_by_point.values()))


class State(NamedTuple):
    last: Node
    path_length: int
    visited: set[Point]


def longest_path_length(graph: Graph) -> int:
    max_path_length = 0

    queue: deque[State] = deque([State(graph.start, 0, {graph.start.point})])
    while queue:
        state = queue.pop()
        if state.last == graph.end:
            max_path_length = max(max_path_length, state.path_length)
            print('found a path', state.path_length, 'best is', max_path_length)
        else:
            for neighbor, weight in state.last.edges_out:
                if neighbor.point not in state.visited:
                    queue.append(State(neighbor, state.path_length + weight, state.visited | {neighbor.point}))

    return max_path_length


def main():
    with open(sys.argv[1]) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    grid2 = [list(line.strip()) for line in """
    #.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
    """.strip().split('\n')]

    # part1(grid)
    part2(grid)


def part1(grid):
    graph1 = Graph.parse1(grid)
    print(len(graph1.all_nodes))
    print(longest_path_length(graph1))


def part2(grid):
    graph2 = Graph.parse2(grid)
    print(len(graph2.all_nodes))
    print(longest_path_length(graph2))


if __name__ == '__main__':
    main()
