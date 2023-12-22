from __future__ import annotations

import sys
from collections import deque
from typing import NamedTuple


class Point3D(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def parse(s: str) -> Point3D:
        xs, ys, zs = s.split(',')
        return Point3D(int(xs), int(ys), int(zs))


class Range(NamedTuple):
    """Inclusive"""
    start: int
    end: int

    @staticmethod
    def create(start: int, end: int):
        return Range(start, end) if start < end else Range(end, start)

    def overlaps(self, other: Range) -> bool:
        return self.start <= other.end and self.end >= other.start


class Brick:
    index: int

    """Inclusive"""
    start: Point3D
    end: Point3D

    x_range: Range
    y_range: Range
    edges_up: set[Brick]
    edges_down: set[Brick]
    would_fall: set[Brick] | None

    def __init__(self, index: int, start: Point3D, end: Point3D):
        self.index = index
        self.start = start
        self.end = end

        self.x_range = Range.create(self.min_x, self.max_x)
        self.y_range = Range.create(self.min_y, self.max_y)

        self.edges_up = set()
        self.edges_down = set()
        self.would_fall = None

    @staticmethod
    def parse(index: int, s: str) -> Brick:
        s1, s2 = s.split('~')
        return Brick(index, Point3D.parse(s1), Point3D.parse(s2))

    def overlaps_xy(self, other: Brick) -> bool:
        return self.x_range.overlaps(other.x_range) and self.y_range.overlaps(other.y_range)

    @property
    def min_x(self) -> int:
        return min(self.start.x, self.end.x)

    @property
    def max_x(self) -> int:
        return max(self.start.x, self.end.x)

    @property
    def min_y(self) -> int:
        return min(self.start.y, self.end.y)

    @property
    def max_y(self) -> int:
        return max(self.start.y, self.end.y)

    @property
    def min_z(self) -> int:
        return min(self.start.z, self.end.z)

    @property
    def max_z(self) -> int:
        return max(self.start.z, self.end.z)

    def __repr__(self):
        s, e = self.start, self.end
        return f'Brick({self.index}, {s.x},{s.y},{s.z}~{e.x},{e.y},{e.z})'

    def drop_to(self, new_bottom_z: int) -> Brick:
        start, end = self.start, self.end
        if start.z < end.z:
            return Brick(self.index, start._replace(z=new_bottom_z), end._replace(z=new_bottom_z + end.z - start.z))
        else:
            return Brick(self.index, start._replace(z=new_bottom_z + start.z - end.z), end._replace(z=new_bottom_z))


def main():
    with open(sys.argv[1]) as f:
        bricks = [Brick.parse(i, line.strip()) for i, line in enumerate(f.readlines())]

    z_sorted_bricks = deque(sorted(bricks, key=lambda br: br.min_z))
    landed_bricks: list[Brick] = []

    while z_sorted_bricks:
        b = z_sorted_bricks.popleft()
        overlaps = [other for other in landed_bricks if b.overlaps_xy(other)]
        if not overlaps:
            landed_bricks.append(b.drop_to(1))
        else:
            max_z = max(other.max_z for other in overlaps)
            dropped = b.drop_to(max_z + 1)
            for other in overlaps:
                if other.max_z == max_z:
                    other.edges_up.add(dropped)
                    dropped.edges_down.add(other)
            landed_bricks.append(dropped)

    # part 1
    safe_disintegration_count = 0
    for b in landed_bricks:
        if not b.edges_up:
            safe_disintegration_count += 1
        elif all(len(other.edges_down) > 1 for other in b.edges_up):
            safe_disintegration_count += 1
    print(safe_disintegration_count)

    # part 2
    fall_count = 0
    for b in landed_bricks:
        if b.edges_up:
            fallen_bricks = set()
            find_fallen_bricks(b, fallen_bricks)
            fall_count += len(fallen_bricks) - 1 # don't count itself
    print(fall_count)


def find_fallen_bricks(brick: Brick, fallen_bricks: set[Brick]):
    fallen_bricks.add(brick)
    new_falls = []
    for brick_above in brick.edges_up:
        if len(brick_above.edges_down - fallen_bricks) == 0:
            fallen_bricks.add(brick_above)
            new_falls.append(brick_above)
    for brick_above in new_falls:
        find_fallen_bricks(brick_above, fallen_bricks)


if __name__ == '__main__':
    main()
