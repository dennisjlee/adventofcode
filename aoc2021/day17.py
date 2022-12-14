from __future__ import annotations

import itertools
import math
import re
import typing


class Point(typing.NamedTuple):
    x: int
    y: int


class Velocity(typing.NamedTuple):
    dx: int
    dy: int

    def __repr__(self):
        return f'Velocity(dx={self.dx},dy={self.dy})'


class Target(typing.NamedTuple):
    top_left: Point
    bottom_right: Point

    def point_inside(self, point):
        return self.top_left.x <= point.x <= self.bottom_right.x and \
               self.bottom_right.y <= point.y <= self.top_left.y

    def point_overshot(self, point):
        return point.x > self.bottom_right.x or point.y < self.bottom_right.y


PARSER = re.compile(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')


def main():
    solve('target area: x=20..30, y=-10..-5')
    solve('target area: x=70..96, y=-179..-124')


def solve(input: str):
    match = PARSER.match(input)
    x_start = int(match.group(1))
    x_end = int(match.group(2))
    y_start = int(match.group(3))
    y_end = int(match.group(4))
    top_left = Point(x_start, y_end)
    bottom_right = Point(x_end, y_start)
    target = Target(top_left, bottom_right)

    # min x velocity such that dx*(dx+1) >= 2*x_start
    min_dx = min(dx for dx in range(x_start) if triangular(dx) >= x_start)
    max_dx = x_end
    min_dy = y_start
    highest_y = 0
    best_velocity = None
    possible_trajectories = 0
    for dx in range(min_dx - 1, max_dx + 1):
        for dy in range(y_start, 800):  # how can I set a better max here??
            initial_velocity = Velocity(dx, dy)
            best_y = step_until_done(initial_velocity, Point(0, 0), target)
            if best_y is not None:
                possible_trajectories += 1
                if best_y > highest_y:
                    highest_y = best_y
                    best_velocity = initial_velocity

    # step_until_done(best_velocity, Point(0, 0), target, True)
    print(highest_y, best_velocity)
    print(possible_trajectories)


def step_until_done(v: Velocity, p: Point, t: Target, debug=False) -> typing.Optional[int]:
    highest_y = p.y
    if debug:
        print(f'Velocity: {v}, Point: {p}')
    while not (t.point_inside(p) or t.point_overshot(p)):
        v, p = step(v, p)
        if debug:
            print(f'Velocity: {v}, Point: {p}')
        if p.y > highest_y:
            highest_y = p.y
    if t.point_inside(p):
        return highest_y


def step(v: Velocity, p: Point) -> tuple[Velocity, Point]:
    new_point = Point(p.x + v.dx, p.y + v.dy)
    new_dx = 0 if v.dx == 0 else int(v.dx - math.copysign(1, v.dx))
    new_dy = v.dy - 1
    return Velocity(new_dx, new_dy), new_point


def triangular(n: int):
    return n * (n + 1) / 2


if __name__ == '__main__':
    main()
