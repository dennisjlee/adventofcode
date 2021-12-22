from __future__ import annotations

import collections
import itertools
import re
import sys
import typing


class Interval(typing.NamedTuple):
    start: int
    end: int

    def overlaps(self, other: Interval):
        return self.end >= other.start and self.start <= other.end

    def contains(self, other: Interval):
        return self.start <= other.start and self.end >= other.end

    def __len__(self):
        return self.end - self.start + 1

    def __sub__(self, other: Interval) -> typing.Iterable[Interval]:
        if self.start < other.start:
            yield Interval(self.start, other.start - 1)
        if self.end > other.end:
            yield Interval(other.end + 1, self.end)

    @staticmethod
    def create(start_str: str, end_str: str):
        return Interval(int(start_str), int(end_str))


class Cuboid(typing.NamedTuple):
    x: Interval
    y: Interval
    z: Interval

    def overlaps(self, other: Cuboid):
        return self.x.overlaps(other.x) and self.y.overlaps(other.y) and self.z.overlaps(other.z)

    def contains(self, other: Cuboid):
        return self.x.contains(other.x) and self.y.contains(other.y) and self.z.contains(other.z)

    def volume(self):
        return len(self.x) * len(self.y) * len(self.z)

    def __sub__(self, other: Cuboid) -> typing.Iterable[Cuboid]:
        if other.contains(self):
            return

        cuboids = []
        if not other.z.contains(self.z):
            for z_interval in self.z - other.z:
                cuboids.append(Cuboid(self.x, self.y, z_interval))

        if not other.y.contains(self.y):
            for y_interval in self.y - other.y:
                new_cuboid = Cuboid(self.x, y_interval, self.z)
                queue = [new_cuboid]
                while queue:
                    curr = queue.pop()
                    for c in cuboids:
                        if curr.overlaps(c):
                            for diff in curr - c:
                                queue.append(diff)
                            break
                    else:
                        # no overlaps
                        cuboids.append(curr)

        if not other.x.contains(self.x):
            for x_interval in self.x - other.x:
                new_cuboid = Cuboid(x_interval, self.y, self.z)
                queue = [new_cuboid]
                while queue:
                    curr = queue.pop()
                    for c in cuboids:
                        if curr.overlaps(c):
                            for diff in curr - c:
                                queue.append(diff)
                            break
                    else:
                        # no overlaps
                        cuboids.append(curr)

        for c in cuboids:
            yield c


class CuboidSet:
    # Invariant: this set of cuboids should never overlap each other
    cuboids: set[Cuboid]

    def __init__(self):
        self.cuboids = set()

    def add(self, other: Cuboid):
        queue = [other]
        while queue:
            other = queue.pop()
            for c in self.cuboids:
                if c.contains(other):
                    break
                if c.overlaps(other):
                    for diff in other - c:
                        queue.append(diff)
                    break
            else:
                # no overlaps
                self.cuboids.add(other)

    def remove(self, other: Cuboid):
        new_cuboids = set()
        for c in self.cuboids:
            if c.overlaps(other):
                for diff in c - other:
                    new_cuboids.add(diff)
            else:
                new_cuboids.add(c)
        self.cuboids = new_cuboids

    def volume(self):
        return sum(c.volume() for c in self.cuboids)


class Instruction(typing.NamedTuple):
    enabled: int
    cuboid: Cuboid


PARSER = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')


def main():
    instructions = []
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            match = PARSER.match(line)
            enabled = int(match.group(1) == 'on')
            instructions.append(Instruction(enabled, Cuboid(
                Interval.create(match.group(2), match.group(3)),
                Interval.create(match.group(4), match.group(5)),
                Interval.create(match.group(6), match.group(7))
            )))

    part1(instructions)
    part2(instructions)


def part1(instructions: list[Instruction]):
    grid = [
        [
            [0] * 101
            for y in range(101)
        ]
        for z in range(101)
    ]
    for inst in instructions:
        for z in range(max(-50, inst.cuboid.z.start), min(50, inst.cuboid.z.end) + 1):
            for y in range(max(-50, inst.cuboid.y.start), min(50, inst.cuboid.y.end) + 1):
                for x in range(max(-50, inst.cuboid.x.start), min(50, inst.cuboid.x.end) + 1):
                    grid[z + 50][y + 50][x + 50] = inst.enabled

    print(sum(sum(sum(row) for row in plane) for plane in grid))


def part2(instructions: list[Instruction]):
    cuboid_set = CuboidSet()
    for inst in instructions:
        if inst.enabled:
            cuboid_set.add(inst.cuboid)
        else:
            cuboid_set.remove(inst.cuboid)

    print(cuboid_set.volume())


if __name__ == '__main__':
    main()
