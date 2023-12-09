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


class Nanobot:
    pos: Point3D
    rad: int
    neighbors: set[Nanobot]

    def __init__(self, pos: Point3D, rad: int):
        self.pos = pos
        self.rad = rad
        self.neighbors = set()

    @staticmethod
    def parse(line: str) -> Nanobot:
        match = NANOBOT_REGEX.match(line)
        return Nanobot(Point3D.parse(match.group(1)), int(match.group(2)))

    def __repr__(self):
        return f'Nanobot(pos={self.pos}, rad={self.rad}, neighbors={[n.pos for n in self.neighbors]})'

    def overlaps(self, other: Nanobot):
        return manhattan_distance(self.pos, other.pos) <= (self.rad + other.rad)


def manhattan_distance(p1: Point3D, p2: Point3D):
    return abs(p1.y - p2.y) + abs(p1.x - p2.x) + abs(p1.z - p2.z)


def main():
    with open(sys.argv[1]) as f:
        nanobots = [Nanobot.parse(line) for line in f.readlines()]

    strongest = max(nanobots, key=lambda n: n.rad)
    print(strongest)
    print(sum(1 for n in nanobots
              if manhattan_distance(n.pos, strongest.pos) <= strongest.rad))

    for i, n1 in enumerate(nanobots):
        for j in range(i + 1, len(nanobots)):
            n2 = nanobots[j]
            if n1.overlaps(n2):
                n1.neighbors.add(n2)
                n2.neighbors.add(n1)

    most_neighboring = sorted(nanobots, key=lambda n: len(n.neighbors), reverse=True)
    for n in most_neighboring:
        print(f'Nanobot({n.pos}, rad={n.rad}, neighbor_count={len(n.neighbors)})')


"""
2d:

M2_0 = 1 = 4*0 + 1 = 4*T_0 + 1
M2_1 = 5 = 1+3+1 = 4*1 + 1 = 4*T_1 + 1
M2_2 = 13 = 1+3+5+3+1 = 4*3 + 1 = 4*T_2 + 1
M2_3 = 25 = 1+3+5+7+5+3+1 = 4*6 + 1 = 4*T_3 + 1
M2_4 = 41 = 1+3+5+7+9+7+5+3+1 = 4*10 + 1
M2_5 = 61 = 1+3+5+7+9+11+9+7+5+3+1 = 4*15 + 1

Triangular number T_n has the formula T_n = n(n+1)/2
So M2_n (squares contained in 2d Manhattan distance of n) has the formula:
  M2_n = 2n^2 + 2n + 1

      x
     xxx      x
    xxxxx    xxx
   xxxxxxx  xxxxx
    xxxxx    xxx
     xxx      x
      x
      
3d:

M3_0 = 1
M3_1 = M2_1 + 2*M2_0 = 5+1+1 = 7
M3_2 = M2_2 + 2*M2_1 + 2*M2_0 = 13 + 10 + 2 = 25
M3_3 = M2_3 + 2*M2_2 + 2*M2_1 + 2*M2_0 = 25 + 26 + 10 + 2 = 63

M3_n = 2*∑(M2_n) - M2_n + 2
     = 2*∑(2n^2 + 2n + 1) - 2n^2 - 2n + 1
     = 4*∑(n^2) + 4*∑(n) + 2n - 2n^2 - 2n + 1
     = 4n(n+1)(2n+1)/6 + 4n(n+1)/2 - 2n^2 + 1
     = 2n(n+1)(2n+1)/3 + 2n^2 + 2n - 2n^2 + 1
     = (2n^2+2n)(2n+1)/3 + 2n + 1
     = (4n^3 + 2n^2 + 4n^2 + 2n)/3 + 2n + 1
     = 4n^3/3 + 2n^2 + 8n/3 + 1
"""

def manhattan_distance_3d_count(dist: int) -> int:
    return 4*(dist**3)/3 + 2*(dist ** 2) + 8*dist/3 + 1


if __name__ == '__main__':
    main()
