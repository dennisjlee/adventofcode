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


class Sensor:
    location: Point
    nearest_beacon: Point
    beacon_dist: int

    def __init__(self, location: Point, nearest_beacon: Point):
        self.location = location
        self.nearest_beacon = nearest_beacon
        self.beacon_dist = manhattan_distance(location, nearest_beacon)


PARSE_PATTERN = re.compile(r'Sensor at x=(\S*?), y=(\S*?): closest beacon is at x=(\S*?), y=(\S*?)$', re.MULTILINE)


class Interval(NamedTuple):
    start: int
    end: int

    def overlaps(self, other: Interval):
        return self.end >= other.start and self.start <= other.end

    def __or__(self, other: Interval):
        return Interval(min(self.start, other.start), max(self.end, other.end))

    @staticmethod
    def join(intervals: list[Interval], new_interval: Interval):
        results = []
        to_merge = []
        for interval in intervals:
            if not interval.overlaps(new_interval):
                results.append(interval)
            else:
                to_merge.append(interval)

        for other in to_merge:
            new_interval = new_interval | other

        results.append(new_interval)
        return results

    @staticmethod
    def merge(intervals: list[Interval]):
        sorted_intervals = sorted(intervals)
        results = []
        curr = sorted_intervals[0]
        for i in range(1, len(sorted_intervals)):
            other = sorted_intervals[i]
            if curr.overlaps(other):
                curr = curr | other
            else:
                results.append(curr)
                curr = other
        results.append(curr)

        return results


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

    part1(grid, sensors)
    part2(sensors)


def part1(grid: dict[Point, str], sensors: list[Sensor]):
    # target_y = 10
    target_y = 2_000_000

    blocked_positions = set()
    for i, sensor in enumerate(sensors):
        # print(f'sensor {i}: {sensor}; manhattan distance: {sensor.beacon_dist}')
        dist = sensor.beacon_dist
        x, y = sensor.location
        dy = target_y - y
        if abs(dy) <= dist:
            r = range(x + abs(dy) - dist, x + dist - abs(dy) + 1)
            # print(f'sensor {i}, blocked in {r}\n')
            blocked_positions.update(r)

    blocked_positions -= {p.x for p in grid.keys() if p.y == target_y}

    print(len(blocked_positions))


def part2(sensors: list[Sensor]):
    upper_bound = 4_000_000
    for target_y in range(3_000_000, upper_bound + 1):
        blocked_intervals = []
        if target_y % 10_000 == 0:
            print('trying on row', target_y)
        for sensor in sensors:
            dist = sensor.beacon_dist
            x, y = sensor.location
            dy = abs(target_y - y)
            if dy <= dist:
                new_interval = Interval(max(0, x + dy - dist), min(upper_bound, x + dist - dy))
                blocked_intervals.append(new_interval)

        blocked_intervals = Interval.merge(blocked_intervals)
        if len(blocked_intervals) > 1:
            nonblocked_x = blocked_intervals[0].end + 1
            print(blocked_intervals, nonblocked_x, target_y)
            print(nonblocked_x * upper_bound + target_y)
            break


if __name__ == '__main__':
    main()
