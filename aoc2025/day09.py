from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    @staticmethod
    def parse(line: str) -> Point:
        xs, ys = line.strip().split(',')
        return Point(int(xs), int(ys))

    def area(self, other: Point) -> int:
        len_x = abs(other.x - self.x) + 1
        len_y = abs(other.y - self.y) + 1
        return len_x * len_y


def main():
    with Path(sys.argv[1]).open() as f:
        points = [Point.parse(line) for line in f.readlines()]

    print(max(p1.area(p2) for p1, p2 in combinations(points, 2)))

if __name__ == "__main__":
    main()