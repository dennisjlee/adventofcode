from __future__ import annotations
import re
import sys
from typing import NamedTuple, Optional
from copy import deepcopy


class Point3D(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def parse(s: str) -> Point3D:
        xs, ys, zs = s.split(',')
        return Point3D(int(xs), int(ys), int(zs))

    def adjacent_points(self):
        yield Point3D(self.x-1, self.y, self.z)
        yield Point3D(self.x+1, self.y, self.z)
        yield Point3D(self.x, self.y-1, self.z)
        yield Point3D(self.x, self.y+1, self.z)
        yield Point3D(self.x, self.y, self.z-1)
        yield Point3D(self.x, self.y, self.z+1)


def main():
    with open(sys.argv[1]) as f:
        points = set(Point3D.parse(line.strip()) for line in f.readlines())

    # part1
    exposed_sides = 0
    for p in points:
        exposed_sides += sum(1 for neighbor in p.adjacent_points() if neighbor not in points)
    print(exposed_sides)


if __name__ == '__main__':
    main()
