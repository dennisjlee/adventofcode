from __future__ import annotations

import sys
from collections import defaultdict
from fractions import Fraction
from math import lcm
from itertools import combinations
from typing import NamedTuple, Literal

from sympy import divisors


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
    m: Fraction | None
    b: Fraction | None

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

    def position_at_time(self, t: int) -> Point3D:
        x = self.position.x + self.velocity.x * t
        y = self.position.y + self.velocity.y * t
        z = self.position.z + self.velocity.z * t
        return Point3D(x, y, z)

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
        return None

    def intersection_time_single_axis(self, m_other: int, b_other: int, axis: Literal['x', 'y', 'z']) -> float:
        """
        Find the intersection point of two hailstones in the specified axis.
        """
        assert axis in ('x', 'y', 'z')
        m_self = getattr(self.velocity, axis)
        b_self = getattr(self.position, axis)
        return (b_other - b_self) / (m_self - m_other)


def main():
    with open(sys.argv[1]) as f:
        hailstones = [Hailstone.parse(line) for line in f.readlines()]

    bounds_min = Point(200_000_000_000_000, 200_000_000_000_000)
    bounds_max = Point(400_000_000_000_000, 400_000_000_000_000)

    length = len(hailstones)
    intersection_count = 0
    for i, h1 in enumerate(hailstones):
        for j in range(i + 1, length):
            h2 = hailstones[j]
            if h1.intersection_xy(h2, bounds_min, bounds_max):
                intersection_count += 1
    print(intersection_count)

    slopes_x = get_possible_intercept_slopes(hailstones, 'x')
    slopes_y = get_possible_intercept_slopes(hailstones, 'y')
    slopes_z = get_possible_intercept_slopes(hailstones, 'z')

    assert len(slopes_x) == len(slopes_y) == len(slopes_z) == 1
    slope_x = next(iter(slopes_x))
    slope_y = next(iter(slopes_y))
    slope_z = next(iter(slopes_z))
    print(slope_x, slope_y, slope_z)

    # Note: slope_x is negative in both the example and the problem input
    # Find the stones with the closest slopes (on the higher and lower sides) to slope_x.
    _, next_lower_slope_stone = max((h.position.x / 1*(h.velocity.x - slope_x), h) for h in hailstones if h.velocity.x < slope_x)
    _, next_higher_slope_stone = min((h.position.x / 1*(h.velocity.x - slope_x), h) for h in hailstones if h.velocity.x > slope_x)

    b_x = next_lower_slope_stone.position.x - 1
    current_base_x = 1
    intercepted_hailstones = []
    remaining_hailstones = set(hailstones)
    while remaining_hailstones:
        current_intercepts = set()
        for h in remaining_hailstones:
            t = h.intersection_time_single_axis(slope_x, b_x, 'x')
            if t == int(t) and t >= 0:
                current_intercepts.add(h)
        if len(current_intercepts) == 0:
            b_x -= current_base_x
        else:
            print([h.velocity.x for h in current_intercepts])
            current_base_x = lcm(current_base_x, *[h.velocity.x - slope_x for h in current_intercepts])
            print(f"current_b_x={b_x}, current_base={current_base_x}, current_intercepts length={len(current_intercepts)}")
            intercepted_hailstones.extend(current_intercepts)
            remaining_hailstones -= current_intercepts

    first_intersect_time = next_lower_slope_stone.intersection_time_single_axis(slope_x, b_x, 'x')
    assert first_intersect_time == int(first_intersect_time)
    b_y = next_lower_slope_stone.position.y + (next_lower_slope_stone.velocity.y - slope_y) * int(first_intersect_time)
    b_z = next_lower_slope_stone.position.z + (next_lower_slope_stone.velocity.z - slope_z) * int(first_intersect_time)

    for i, h in enumerate(hailstones):
        time_x = h.intersection_time_single_axis(slope_x, b_x, 'x')
        time_y = h.intersection_time_single_axis(slope_y, b_y, 'y')
        time_z = h.intersection_time_single_axis(slope_z, b_z, 'z')
        assert time_x == int(time_x) == time_y == time_z

    print(b_x + b_y + b_z)


# Find hailstones that are moving at the same velocity in X, Y, or Z directions.
# For each pair of hailstones with the same X, Y, or Z velocity, that restricts the possible slopes of the
# intersection line based on these equations (for two hailstones with index i and j and X-velocity of m):
#   x_i = m * t + b_i
#   x_j = m * t + b_j
# To intersect both these lines, consider the difference in x and t.
#   dx = m * dt ± (b_j - b_i)
#   m_intersection = dx/dt = m ± (b_j - b_i) / dt
# To ensure that m_intersection is an integer, we need to ensure that (b_j - b_i) / dt is an integer.
# (b_j - b_i) / dt can have integer values of any divisor of (b_j - b_i).
# Then we can repeat this for all pairs of hailstones with matching velocities to restrict the possible slopes of
# an intercept.
def get_possible_intercept_slopes(hailstones: list[Hailstone], axis: Literal['x', 'y', 'z']) -> set[int]:
    stones_by_slope = defaultdict(list)
    for h in hailstones:
        stones_by_slope[getattr(h.velocity, axis)].append(h)

    all_possible_slopes = None
    for slope, stones in stones_by_slope.items():
        if len(stones) > 1:
            for pair in combinations([getattr(h.position, axis) for h in stones], 2):
                divisor_list = divisors(pair[1] - pair[0])
                possible_slopes = {slope - d for d in divisor_list} | {slope + d for d in divisor_list}
                if all_possible_slopes is None:
                    all_possible_slopes = possible_slopes
                else:
                    all_possible_slopes &= possible_slopes

    return all_possible_slopes



if __name__ == '__main__':
    main()