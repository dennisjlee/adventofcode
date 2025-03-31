from __future__ import annotations

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

    def translate_by(self, vector: Vector) -> Point:
        return Point(self.x + vector.dx, self.y + vector.dy)


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
        # we're going counter-clockwise, reverse things so we go clockwise
        corners = list(reversed(corners))

    corners.pop()  # remove the last corner which is a duplicate
    negative_space = 0
    while len(corners) > 4:
        # Walk the edge of the shape clockwise, looking for left turns. When we find one, cut out
        # that corner and keep track of how much space we added. Eventually we'll be left with a
        # simple rectangle and we'll be able to just multiply to get the total area, and subtract
        # the space we added along the way!
        n = len(corners)
        for i in range(n):
            i1 = (i + 1) % n
            i2 = (i + 2) % n
            i3 = (i + 3) % n
            corner0 = corners[i]
            corner1 = corners[i1]
            corner2 = corners[i2]
            corner3 = corners[i3]
            vec1 = Vector(dx=corner1.x - corner0.x, dy=corner1.y - corner0.y)
            vec2 = Vector(dx=corner2.x - corner1.x, dy=corner2.y - corner1.y)
            vec3 = Vector(dx=corner3.x - corner2.x, dy=corner3.y - corner2.y)
            rotation1 = vec2.rotation_from(vec1)
            rotation2 = vec3.rotation_from(vec2)
            if rotation1 == 'L':
                if rotation2 == 'L':
                    # this looks like a pocket taken out of the shape
                    """
                    ....#.
                    ..###.
                    ..#...
                    ..###.
                    ....#.
                    """
                    negative_space += int(vec1.magnitude * (vec2.magnitude - 1))
                else:
                    # this looks like a corner taken out of the shape
                    """
                    ....#.
                    ..###.
                    ..#...
                    ###...
                    """
                    negative_space += int(vec1.magnitude * vec2.magnitude)

                new_corner = corner0.translate_by(vec2)
                if new_corner == corner3:
                    corners = [corners[j] for j in range(n) if j not in {i, i1, i2, i3}]
                else:
                    corners = [new_corner if j == i else corners[j]
                               for j in range(n) if j not in {i1, i2}]

                break
        else:
            print("No left rotations found!", corners)
            break

    corner0 = corners[0]
    corner1 = corners[1]
    corner2 = corners[2]
    vec1 = Vector(dx=corner1.x - corner0.x, dy=corner1.y - corner0.y)
    vec2 = Vector(dx=corner2.x - corner1.x, dy=corner2.y - corner1.y)
    area = int((vec1.magnitude + 1) * (vec2.magnitude + 1)) - negative_space
    print(area)

    if verbose:
        dug_points: set[Point] = set()
        n = len(corners)
        for i in range(n):
            corner0 = corners[i]
            corner1 = corners[(i + 1) % n]
            vec = Vector(dx=corner1.x - corner0.x, dy=corner1.y - corner0.y)
            unit_vec = vec.unit_vector()
            dug_points.add(corner0)
            next_point = corner0
            for j in range(1, int(vec.magnitude)):
                next_point = next_point.translate_by(unit_vec)
                dug_points.add(next_point)

        print_dug_points(dug_points)


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
