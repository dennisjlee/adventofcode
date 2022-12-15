from __future__ import annotations
import re
import sys
from typing import NamedTuple, Optional, Iterable
from copy import deepcopy


class Point(NamedTuple):
    x: int
    y: int


def manhattan_distance(p1: Point, p2: Point):
    return abs(p1.y - p2.y) + abs(p1.x - p2.x)


class Sensor(NamedTuple):
    location: Point
    nearest_beacon: Point

    @property
    def beacon_dist(self):
        return manhattan_distance(self.location, self.nearest_beacon)

    def eliminated_points(self) -> Iterable[Point]:
        dist = manhattan_distance(self.location, self.nearest_beacon)
        x, y = self.location
        for dy in range(-dist, dist + 1):
            for dx in range(abs(dy) - dist, dist - abs(dy) + 1):
                yield Point(x + dx, y + dy)


PARSE_PATTERN = re.compile(r'Sensor at x=(\w*?), y=(\w*?): closest beacon is at x=(\w*?), y=(\w*?)$', re.MULTILINE)


def main():
    grid: dict[Point, str] = {}
    sensors = []

    with open(sys.argv[1]) as f:
        contents = f.read()
        for match in PARSE_PATTERN.finditer(contents):
            sensor_loc = Point(int(match.group(1)), int(match.group(2)))
            beacon_loc = Point(int(match.group(3)), int(match.group(4)))
            sensor = Sensor(sensor_loc, beacon_loc)
            sensors.append(sensor)
            grid[sensor_loc] = 'S'
            grid[beacon_loc] = 'B'


    min_y = min(p.y for p in grid.keys())
    max_y = max(p.y for p in grid.keys())
    min_x = min(p.x for p in grid.keys())
    max_x = max(p.x for p in grid.keys())

    # target_y = 10
    target_y = 2_000_000

    blocked_positions = set()
    for i, sensor in enumerate(sensors):
        print(f'sensor {i}: {sensor}; manhattan distance: {sensor.beacon_dist}')
        dist = sensor.beacon_dist
        x, y = sensor.location
        dy = abs(y - target_y)
        if dy <= dist:
            r = range(x + dy - dist, x + dist - dy + 1)
            print(f'sensor {i}, blocked in {r}\n')
            blocked_positions.update(r)

    blocked_positions -= {p.x for p in grid.keys() if p.y == target_y}

    print(len(blocked_positions))
    # print(sorted(blocked_positions))


if __name__ == '__main__':
    main()
