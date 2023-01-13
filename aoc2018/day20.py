from __future__ import annotations
import sys
from collections import deque
from typing import NamedTuple, Literal, Iterable, Optional

FORWARD_DIRECTIONS = [
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]


Direction = Literal['N', 'S', 'E', 'W']


class Point(NamedTuple):
    x: int
    y: int

    def translate(self, direction: Direction):
        if direction == 'N':
            return Point(self.x, self.y - 1)
        elif direction == 'S':
            return Point(self.x, self.y + 1)
        elif direction == 'E':
            return Point(self.x + 1, self.y)
        elif direction == 'W':
            return Point(self.x - 1, self.y)


OPPOSITES: dict[Direction, Direction] = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}

DIRECTIONS: set[Direction] = set(OPPOSITES.keys())


class Node:
    point: Point
    neighbors: dict[Direction, Node]
    distance: Optional[int]

    def __init__(self, point: Point, distance=None):
        self.point = point
        self.neighbors = {}
        self.distance = distance

    def __repr__(self):
        return f'Node({self.point}, {"".join(self.neighbors.keys())}, {self.distance})'


Grid = dict[Point, Node]


def main():
    with open(sys.argv[1]) as f:
        regex = f.read().strip()

    solve(regex)


def solve(regex: str):
    grid: Grid = {}
    branch_stack: list[Node] = []
    start = Node(Point(0, 0), 0)
    grid[start.point] = start

    curr = start
    for c in regex:
        if c in DIRECTIONS:
            next_point = curr.point.translate(c)
            next_node = grid.get(next_point) or Node(next_point)
            curr.neighbors[c] = next_node
            next_node.neighbors[OPPOSITES[c]] = curr
            grid[next_point] = next_node
            curr = next_node
        elif c == '(':
            branch_stack.append(curr)
        elif c == ')':
            curr = branch_stack.pop()
        elif c == '|':
            curr = branch_stack[-1]

    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        assert node.point not in visited
        visited.add(node.point)
        for n in node.neighbors.values():
            if n.point not in visited:
                n.distance = node.distance + 1
                queue.append(n)

    # part 1
    print(max(n.distance for n in grid.values()))

    # part 2
    print(sum(1 for n in grid.values() if n.distance >= 1000))


if __name__ == '__main__':
    main()
