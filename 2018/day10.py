from __future__ import annotations
from collections import defaultdict, namedtuple
import re
import sys

"""
position=< 54359,  43457> velocity=<-5, -4>
position=<-21470, -10698> velocity=< 2,  1>
position=<-43100, -21528> velocity=< 4,  2>
"""

Point = namedtuple('Point', ['x', 'y'])


class Light:
    def __init__(self, x, y, dx, dy):
        self.point = Point(x, y)
        self.velocity = Point(dx, dy)

    def step(self):
        self.point = Point(self.point.x + self.velocity.x, self.point.y + self.velocity.y)


def main():
    pattern = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')
    lights = []
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            match = pattern.match(line.strip())
            lights.append(Light(int(match.group(1)),
                                int(match.group(2)),
                                int(match.group(3)),
                                int(match.group(4))))

    for i in range(100000):
        min_corner, max_corner = bounding_box(lights)
        if max_corner.x - min_corner.x < 100 and max_corner.y - min_corner.y < 100:
            print('step', i, 'field is...', min_corner, max_corner)
            visualize_lights(lights)
            print('\n\n\n')

        for light in lights:
            light.step()


def bounding_box(lights: list[Light]) -> tuple[Point, Point]:
    min_x = min(l.point.x for l in lights)
    max_x = max(l.point.x for l in lights)
    min_y = min(l.point.y for l in lights)
    max_y = max(l.point.y for l in lights)

    return Point(min_x, min_y), Point(max_x, max_y)


def visualize_lights(lights: list[Light]):
    min_corner, max_corner = bounding_box(lights)

    grid = [
        ['.'] * (max_corner.x - min_corner.x + 1)
        for _ in range(min_corner.y, max_corner.y + 1)
    ]
    for light in lights:
        x, y = light.point
        grid[y - min_corner.y][x - min_corner.x] = '#'

    print('\n'.join(''.join(row) for row in grid))


if __name__ == '__main__':
    main()
