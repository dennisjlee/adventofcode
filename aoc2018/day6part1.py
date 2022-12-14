#!/usr/bin/env python3

import sys
from collections import namedtuple
from string import ascii_letters

Point = namedtuple('Point', ['x', 'y', 'label'])

class Region:
    size = 0
    infinite = False

def parse_line(line, label):
    parts = line.strip().split(', ')
    return Point(int(parts[0]), int(parts[1]), label)


def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def main(filename):
    with open(filename) as f:
        lines = f.readlines()
        assert len(lines) <= len(ascii_letters)
        points = [parse_line(line, label)
                  for line, label in zip(lines, ascii_letters)]

    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)

    height = max_y - min_y + 1
    width = max_x - min_x + 1
    # NOTE: indexed as grid[y][x]
    grid = [(['.'] * width) for y in range(height)]

    regions = {p: Region() for p in points}

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            tied = False
            nearest_point = None
            min_distance = height + width + 1
            current = Point(x, y, 'temp')
            for p in points:
                distance = manhattan_distance(current, p)
                if distance < min_distance:
                    nearest_point = p
                    tied = False
                    min_distance = distance
                elif distance == min_distance:
                    tied = True
            if not tied:
                grid[y - min_y][x - min_x] = nearest_point.label
                region = regions[nearest_point]
                region.size += 1
                if y == min_y or y == max_y or x == min_x or x == max_x:
                    region.infinite = True

    # print(points)
    # print('\n'.join(''.join(col for col in row) for row in grid))
    biggest_finite_region = max((r for r in regions.values() if not r.infinite), key=lambda r: r.size)
    print(biggest_finite_region.size)


if __name__ == '__main__':
    main(sys.argv[1])
