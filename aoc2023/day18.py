from __future__ import annotations

import sys
from bisect import insort_left
from collections import defaultdict
from typing import NamedTuple
import re


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


def part1(instructions: list[Instruction]):
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


def part2(instructions: list[Instruction]):
    curr = Point(0, 0)
    corners: set[Point] = {curr}
    for instr in instructions:
        vec = instr.vector
        curr = Point(curr.x + instr.magnitude * vec.dx, curr.y + instr.magnitude * vec.dy)
        corners.add(curr)

    corners_by_y: dict[int, list[Point]] = defaultdict(list)
    corners_by_x: dict[int, list[Point]] = defaultdict(list)
    for corner in corners:
        insort_left(corners_by_x[corner.x], corner)
        insort_left(corners_by_y[corner.y], corner)

    print()
    print('\n'.join(repr((x, corners)) for x, corners in sorted(corners_by_x.items())))
    print()
    print('\n'.join(repr((y, corners)) for y, corners in sorted(corners_by_y.items())))


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    instructions1 = [Instruction.parse1(line) for line in lines]
    part1(instructions1)
    part2(instructions1)
    # part2([Instruction.parse2(line) for line in lines])


if __name__ == '__main__':
    main()
