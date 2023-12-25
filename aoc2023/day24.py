from __future__ import annotations

import sys
from collections import deque
from fractions import Fraction
from typing import NamedTuple, Iterable, Tuple


class Point(NamedTuple):
    x: float
    y: float


class Point3D(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def parse(s: str) -> Point3D:
        xs, ys, zs = s.split(',')
        return Point3D(int(xs.strip()), int(ys.strip()), int(zs.strip()))


class Hailstone(NamedTuple):
    position: Point3D
    velocity: Point3D
    m: Fraction
    b: Fraction

    @staticmethod
    def parse(line: str) -> Hailstone:
        p, v = line.strip().split(' @ ')
        position = Point3D.parse(p)
        velocity = Point3D.parse(v)

        m_numerator = velocity.y
        m_denominator = velocity.x
        b = position.y - Fraction(position.x * m_numerator, m_denominator)
        m = Fraction(m_numerator, m_denominator)
        return Hailstone(position, velocity, m, b)

    def project_for_x(self, x: float) -> tuple[float, float]:
        y = float(self.m * x + self.b)
        t = (y - self.position.y) / self.velocity.y
        return y, t

    def intersection_xy(self, other: Hailstone, min_bounds: Point, max_bounds: Point) -> Point | None:
        """
        y = m1*x + b1
        y = m2*x + b2
        0 = (m1-m2)x + b1 - b2
        x = (b2 - b1) / (m1 - m2)
        """
        if self.m == other.m:
            assert self.b != other.b
            return None
        intersection_x = float((other.b - self.b) / (self.m - other.m))
        intersection_y, t1 = self.project_for_x(intersection_x)
        intersection_y2, t2 = other.project_for_x(intersection_x)
        if min_bounds.x <= intersection_x <= max_bounds.x and \
                min_bounds.y <= intersection_y <= max_bounds.y and \
                t1 >= 0 and t2 >= 0:
            return Point(intersection_x, intersection_y)



def main():
    with open(sys.argv[1]) as f:
        hailstones = [Hailstone.parse(line) for line in f.readlines()]

    bounds_min = Point(200_000_000_000_000, 200_000_000_000_000)
    bounds_max = Point(400_000_000_000_000, 400_000_000_000_000)

#     hailstones = [Hailstone.parse(line) for line in """
#     19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3""".strip().split('\n')]
#
#     bounds_min = Point(7, 7)
#     bounds_max = Point(27, 27)

    length = len(hailstones)
    intersection_count = 0
    for i, h1 in enumerate(hailstones):
        for j in range(i + 1, length):
            h2 = hailstones[j]
            if h1.intersection_xy(h2, bounds_min, bounds_max):
                intersection_count += 1
    print(intersection_count)




if __name__ == '__main__':
    main()
