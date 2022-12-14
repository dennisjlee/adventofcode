#!/usr/bin/env python3

import sys
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def parse_line(line):
    parts = line.strip().split(', ')
    return Point(int(parts[0]), int(parts[1]))


def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def main(filename):
    with open(filename) as f:
        lines = f.readlines()
        points = [parse_line(line) for line in lines]

    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)

    height = max_y - min_y + 1
    width = max_x - min_x + 1

    DISTANCE_THRESHOLD = 10000

    matching_points = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            current = Point(x, y)
            total_distance = sum(manhattan_distance(current, p) for p in points)
            if total_distance < DISTANCE_THRESHOLD:
                matching_points += 1

    print(matching_points)


if __name__ == '__main__':
    main(sys.argv[1])
