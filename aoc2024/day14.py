import re
from collections import Counter
from dataclasses import dataclass, field

import sys
from functools import reduce
from operator import mul
from typing import NamedTuple, Iterable

from blessed import Terminal


class Point(NamedTuple):
    x: int
    y: int


class Velocity(NamedTuple):
    dx: int
    dy: int


WIDTH = 101
HEIGHT = 103
X_CUTOFF = WIDTH // 2
Y_CUTOFF = HEIGHT // 2


ROBOT_REGEX = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')


@dataclass
class Robot:
    point: Point
    velocity: Velocity

    initial_point: Point = field(init=False)
    period: int | None = field(init=False, default=None)

    def __post_init__(self):
        self.initial_point = self.point

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

    def move_back(self):
        new_point = Point((self.point.x - self.velocity.dx) % WIDTH,
                          (self.point.y - self.velocity.dy) % HEIGHT)
        self.point = new_point

    def set_turn(self, turn: int):
        new_point = Point((self.initial_point.x + turn * self.velocity.dx) % WIDTH,
                          (self.initial_point.y + turn * self.velocity.dy) % HEIGHT)
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


def print_grid(robots: Iterable[Robot], row_limit: int):
    points = {r.point for r in robots}
    for y in range(min(HEIGHT, row_limit)):
        print(''.join('#' if Point(x, y) in points else ' ' for x in range(WIDTH)))


def main():
    with open(sys.argv[1]) as f:
        robots = [Robot.parse(line) for line in f.readlines()]

    for r in robots:
        r.set_turn(100)

    quadrant_counter = Counter()
    for r in robots:
        q = r.quadrant()
        if q is not None:
            quadrant_counter[r.quadrant()] += 1

    print(reduce(mul, quadrant_counter.values(), 1))

    term = Terminal()
    default_timeout = 1/60
    timeout = default_timeout
    for r in robots:
        r.set_turn(0)
    with (term.cbreak()):
        i = 0
        while i < WIDTH * HEIGHT:
            keystroke = term.inkey(timeout=timeout)
            if keystroke:
                if keystroke == ' ':
                    timeout = default_timeout if timeout is None else None
                    continue
                elif keystroke.name == "KEY_LEFT":
                    i -= 1
                    for r in robots:
                        r.move_back()
                elif keystroke.name == "KEY_RIGHT":
                    i += 1
                    for r in robots:
                        r.move()
                elif keystroke.name == "KEY_UP":
                    i -= WIDTH
                    for r in robots:
                        r.set_turn(i)
                elif keystroke.name == "KEY_DOWN":
                    i += WIDTH
                    for r in robots:
                        r.set_turn(i)
                print(term.home + term.clear, end='')
                print(term.bright_green(f'{i=}'))
                print_grid(robots, row_limit=HEIGHT)
            else:
                for r in robots:
                    r.move()
                print(term.home + term.clear, end='')
                print(term.bright_green(f'{i=}'))
                print_grid(robots, row_limit=HEIGHT)
                i += 1

    # the answer is 6532!


if __name__ == "__main__":
    main()
