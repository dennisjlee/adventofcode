from __future__ import annotations

import re
import sys
from typing import NamedTuple, Optional, Literal


class Point3D(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def parse(s: str) -> Point3D:
        xs, ys, zs = s.split(',')
        return Point3D(int(xs), int(ys), int(zs))


# example: 'pos=<-10401751,8998791,-4822601>, r=53367159'
NANOBOT_REGEX = re.compile(r'pos=<(.*?)>, r=(\d+)')

class Nanobot(NamedTuple):
    pos: Point3D
    rad: int

    @staticmethod
    def parse(line: str) -> Nanobot:
        match = NANOBOT_REGEX.match(line)
        return Nanobot(Point3D.parse(match.group(1)), int(match.group(2)))


def manhattan_distance(p1: Point3D, p2: Point3D):
    return abs(p1.y - p2.y) + abs(p1.x - p2.x) + abs(p1.z - p2.z)


def main():
    with open(sys.argv[1]) as f:
        nanobots = [Nanobot.parse(line) for line in f.readlines()]

    strongest = max(nanobots, key=lambda n: n.rad)
    print(strongest)
    print(sum(1 for n in nanobots
              if manhattan_distance(n.pos, strongest.pos) <= strongest.rad))


if __name__ == '__main__':
    main()
