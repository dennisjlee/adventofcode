import re
from collections import Counter
from dataclasses import dataclass

import sys
from functools import reduce
from operator import mul
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Velocity(NamedTuple):
    dx: int
    dy: int


WIDTH = 101
HEIGHT = 103
X_CUTOFF = 50
Y_CUTOFF = 51


ROBOT_REGEX = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')


@dataclass
class Robot:
    point: Point
    velocity: Velocity

    @staticmethod
    def parse(line: str) -> "Robot":
        # p=24,28 v=-92,3
        match = ROBOT_REGEX.match(line.strip())
        return Robot(Point(int(match.group(1)), int(match.group(2))),
                     Velocity(int(match.group(3)), int(match.group(4))))

    def move(self):
        new_point = Point((self.point.x + self.velocity.dx) % WIDTH,
                          (self.point.y + self.velocity.dy) % HEIGHT)
        self.point = new_point

    def quadrant(self):
        upper = self.point.y < Y_CUTOFF
        bottom = self.point.y > Y_CUTOFF
        left = self.point.x < X_CUTOFF
        right = self.point.x > X_CUTOFF
        if left and upper:
            return 0
        elif left and bottom:
            return 2
        elif right and upper:
            return 1
        elif right and bottom:
            return 3
        return None


def main():
    with open(sys.argv[1]) as f:
        robots = [Robot.parse(line) for line in f.readlines()]

    for _ in range(100):
        for r in robots:
            r.move()

    quadrant_counter = Counter()
    for r in robots:
        q = r.quadrant()
        if q is not None:
            quadrant_counter[r.quadrant()] += 1

    print(reduce(mul, quadrant_counter.values(), 1))


if __name__ == "__main__":
    main()
