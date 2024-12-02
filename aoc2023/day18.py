from __future__ import annotations

import re
import sys
from collections import defaultdict, deque
from typing import NamedTuple, Iterable


class Vector(NamedTuple):
    dx: int
    dy: int


class Point(NamedTuple):
    x: int
    y: int


LINE_REGEX = re.compile(r'([A-Z]) (\d+) \(#([0-9a-f]+)\)')


class Instruction(NamedTuple):
    vector: Vector
    magnitude: int

    @staticmethod
    def parse1(line: str) -> Instruction:
        match = LINE_REGEX.match(line)
        vector = VECTOR_LOOKUP[match.group(1)]
        magnitude = int(match.group(2))
        return Instruction(vector, magnitude)

    @staticmethod
    def parse2(line: str) -> Instruction:
        match = LINE_REGEX.match(line)
        color = match.group(3)
        magnitude = int(color[0:-1], 16)
        vector = VECTOR_LOOKUP[color[-1]]
        return Instruction(vector, magnitude)


UP = Vector(0, -1)
DOWN = Vector(0, 1)
LEFT = Vector(-1, 0)
RIGHT = Vector(1, 0)

VECTOR_LOOKUP = {
    'U': UP,
    'D': DOWN,
    'L': LEFT,
    'R': RIGHT,
    '0': RIGHT,
    '1': DOWN,
    '2': LEFT,
    '3': UP,
}


def part1(instructions: list[Instruction], verbose=False):
    curr = Point(0, 0)
    dug_points: set[Point] = {curr}
    for instr in instructions:
        vec = instr.vector
        for step in range(instr.magnitude):
            curr = Point(curr.x + vec.dx, curr.y + vec.dy)
            dug_points.add(curr)

    min_x = min(p.x for p in dug_points) - 1
    min_y = min(p.y for p in dug_points) - 1
    max_x = max(p.x for p in dug_points) + 1
    max_y = max(p.y for p in dug_points) + 1
    total_points = (max_y - min_y + 1) * (max_x - min_x + 1)

    # Do a BFS to find everything reachable from outside the dug points
    outside_points: set[Point] = set()
    stack = [Point(min_x, min_y)]
    while stack:
        search = stack.pop()
        if search not in outside_points:
            outside_points.add(search)
            for y in range(max(search.y - 1, min_y), min(search.y + 2, max_y + 1)):
                for x in range(max(search.x - 1, min_x), min(search.x + 2, max_x + 1)):
                    if x == search.x and y == search.y:
                        continue
                    new_point = Point(x, y)
                    if new_point not in dug_points and new_point not in outside_points:
                        stack.append(Point(x, y))

    print(total_points - len(outside_points))
    if verbose:
        for y in range(min_y, max_y + 1):
            def c(x):
                if x == 0 and y == 0:
                    return '@'
                elif Point(x, y) in dug_points:
                    return '#'
                else:
                    return '.'
            line = ''.join([c(x) for x in range(min_x, max_x + 1)])
            print(line)


class IndexedCorners:
    def __init__(self, corners: list[Point]):
        self.corners = corners

    def remove(self, corner: Point):
        pass
        # self.corners_by_x[corner.x].remove(corner)
        # self.corners_by_x[corner.y].remove(corner)


def part2(instructions: list[Instruction]):
    curr = Point(0, 0)
    corners: list[Point] = [curr]
    for instr in instructions:
        vec = instr.vector
        curr = Point(curr.x + instr.magnitude * vec.dx, curr.y + instr.magnitude * vec.dy)
        corners.append(curr)

    n = len(corners)
    start_index = min(range(n), key=lambda i: corners[i])
    print(corners[start_index], corners[(start_index + 1) % n], corners[(start_index - 1) % n], corners[(start_index - 2) % n])


    # print()
    # print('\n'.join(repr((x, corners)) for x, corners in sorted(corners_by_x.items())))
    # print()
    # print('\n'.join(repr((y, corners)) for y, corners in sorted(corners_by_y.items())))
    # print()
    # print('\n'.join(repr(c) for c in sorted_corners))


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    instructions1 = [Instruction.parse1(line) for line in lines]
    part1(instructions1, True)
    part2(instructions1)
    # print('\n'.join([repr(Instruction.parse2(line)) for line in lines]))
    # part2([Instruction.parse2(line) for line in lines])


if __name__ == '__main__':
    main()
