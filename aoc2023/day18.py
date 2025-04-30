from __future__ import annotations

import math
from math import sqrt
import re
import sys
from collections import Counter
from typing import NamedTuple, Literal


Rotation = Literal['L', 'R', None]


class Vector(NamedTuple):
    dx: int
    dy: int

    @property
    def magnitude(self) -> float:
        return sqrt(self.dx ** 2 + self.dy ** 2)

    def unit_vector(self) -> Vector:
        mag = self.magnitude
        return Vector(dx=int(self.dx / mag), dy=int(self.dy / mag))

    def rotation_from(self, other: Vector) -> Rotation:
        if self.dx == 0 and other.dx == 0:
            return None
        elif self.dy == 0 and other.dy == 0:
            return None
        elif other.dy < 0:  # other is UP
            return 'R' if self.dx > 0 else 'L'
        elif other.dy > 0:  # other is DOWN
            return 'R' if self.dx < 0 else 'L'
        elif other.dx > 0:  # other is RIGHT
            return 'R' if self.dy > 0 else 'L'
        elif other.dx < 0:  # other is LEFT
            return 'R' if self.dy < 0 else 'L'


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other) -> Point:
        if isinstance(other, Vector):
            return Point(self.x + other.dx, self.y + other.dy)
        raise NotImplementedError

    def __sub__(self, other) -> Point:
        if isinstance(other, Vector):
            return Point(self.x - other.dx, self.y - other.dy)
        raise NotImplementedError


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


def print_dug_points(dug_points: set[Point]):
    min_x = min(p.x for p in dug_points) - 1
    min_y = min(p.y for p in dug_points) - 1
    max_x = max(p.x for p in dug_points) + 1
    max_y = max(p.y for p in dug_points) + 1

    def c(xx, yy):
        if xx == 0 and yy == 0:
            return "@"
        elif Point(xx, yy) in dug_points:
            return "#"
        else:
            return "."

    for y in range(min_y, max_y + 1):
        print("".join([c(x, y) for x in range(min_x, max_x + 1)]))


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
        print_dug_points(dug_points)


def part2(instructions: list[Instruction], verbose=False):
    curr = Point(0, 0)
    corners: list[Point] = [curr]
    rotation_counter: Counter[Rotation] = Counter()
    prev_vec: Vector | None = None
    for instr in instructions:
        vec = instr.vector
        if prev_vec:
            rotation1 = vec.rotation_from(prev_vec)
            rotation_counter[rotation1] += 1
        curr = Point(curr.x + instr.magnitude * vec.dx, curr.y + instr.magnitude * vec.dy)
        corners.append(curr)

        prev_vec = vec
    assert None not in rotation_counter
    if rotation_counter['R'] < rotation_counter['L']:
        # we're going counter-clockwise, reverse things so that we go clockwise
        corners = list(reversed(corners))

    last_corner = corners.pop()  # remove the last corner which is a duplicate
    assert last_corner == corners[0]
    removed_space = 0
    while len(corners) > 4:
        # Walk the edge of the shape clockwise, looking for two right turns in a row. Each time we find that, it's a
        # bump sticking out of the shape. Remove the smallest bump and then keep iterating, keeping track of how much
        # space we removed. Eventually we'll be left with a simple rectangle, and we'll be able to just multiply to get
        # the total area, then add back the space we removed along the way!
        n = len(corners)

        smallest_removal = math.inf
        new_corners: list[Point] = []

        for i0 in range(n):
            i1 = (i0 + 1) % n
            i2 = (i0 + 2) % n
            i3 = (i0 + 3) % n
            corner0 = corners[i0]
            corner1 = corners[i1]
            corner2 = corners[i2]
            corner3 = corners[i3]
            vec1 = Vector(dx=corner1.x - corner0.x, dy=corner1.y - corner0.y)
            vec2 = Vector(dx=corner2.x - corner1.x, dy=corner2.y - corner1.y)
            vec3 = Vector(dx=corner3.x - corner2.x, dy=corner3.y - corner2.y)
            rotation1 = vec2.rotation_from(vec1)
            rotation2 = vec3.rotation_from(vec2)
            if rotation1 == 'R':
                if rotation2 == 'R':
                    # This looks like a bump sticking out of the shape. Note that vec1 can have equal, greater, or lower
                    # magnitude than vec3 (the two horizontal vectors in the three examples below, travelling from top
                    # to bottom).
                    """
                    ....#.....#........#.
                    ..2#3...2#3....2###3.
                    ..#.....#......#.....
                    ..1#0...1###0..1#0...
                    ....#.......#....#...
                    """
                    removal_size = int(min(vec1.magnitude, vec3.magnitude) * (vec2.magnitude + 1))
                    if removal_size < smallest_removal:
                        smallest_removal = removal_size

                        delta = vec3.magnitude - vec1.magnitude
                        if delta == 0:
                            new_corners = [corners[j] for j in range(n) if j not in {i0, i1, i2, i3}]

                        elif delta < 0:
                            new_corner = corner3 - vec2
                            new_corners = [new_corner if j == i3 else corners[j]
                                           for j in range(n) if j not in {i1, i2}]
                        else:
                            new_corner = corner0 + vec2
                            new_corners = [new_corner if j == i0 else corners[j]
                                           for j in range(n) if j not in {i1, i2}]

        if smallest_removal == math.inf:
            # We didn't find two right turns in a row, so flip around and try again
            corners = list(reversed(corners))
        else:
            corners = new_corners
            removed_space += smallest_removal

            if verbose:
                print()
                print_corners(corners)
                print(f"{removed_space=}")

    [corner0, corner1, corner2] = corners[:3]
    vec1 = Vector(dx=corner1.x - corner0.x, dy=corner1.y - corner0.y)
    vec2 = Vector(dx=corner2.x - corner1.x, dy=corner2.y - corner1.y)
    area = int((vec1.magnitude + 1) * (vec2.magnitude + 1)) + removed_space
    print(area)

    if verbose:
        print_corners(corners)


def print_corners(corners: list[Point]):
    dug_points: set[Point] = set()
    n = len(corners)
    for i in range(n):
        corner0 = corners[i]
        corner1 = corners[(i + 1) % n]
        vec = Vector(dx=corner1.x - corner0.x, dy=corner1.y - corner0.y)
        if vec.magnitude == 0:
            print("Warning: duplicate corner", corner0)
            continue
        unit_vec = vec.unit_vector()
        dug_points.add(corner0)
        next_point = corner0
        for j in range(1, int(vec.magnitude)):
            next_point = next_point + unit_vec
            dug_points.add(next_point)

    print_dug_points(dug_points)
    print(corners)


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    instructions1 = [Instruction.parse1(line) for line in lines]
    part1(instructions1, True)
    part2(instructions1, True)
    # print('\n'.join([repr(Instruction.parse2(line)) for line in lines]))
    # part2([Instruction.parse2(line) for line in lines])


if __name__ == '__main__':
    main()
