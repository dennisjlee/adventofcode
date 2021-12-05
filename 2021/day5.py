from collections import namedtuple, defaultdict
import re
import sys


Point = namedtuple('Point', ['x', 'y'])


class Segment:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    @property
    def horizontal(self):
        return self.start.y == self.end.y

    @property
    def vertical(self):
        return self.start.x == self.end.x

    def points(self):
        if self.horizontal:
            for x in range(min(self.start.x, self.end.x), max(self.start.x, self.end.x) + 1):
                yield Point(x, self.start.y)
        elif self.vertical:
            for y in range(min(self.start.y, self.end.y), max(self.start.y, self.end.y) + 1):
                yield Point(self.start.x, y)
        else:
            dx = 1 if self.end.x > self.start.x else -1
            dy = 1 if self.end.y > self.start.y else -1
            # Assume 45 degrees
            for i in range(abs(self.end.x - self.start.x) + 1):
                yield Point(self.start.x + (i * dx), self.start.y + (i * dy))


def main():
    segments = []
    parser = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')

    with open(sys.argv[1]) as f:
        for line in f.readlines():
            match = parser.match(line.strip())
            segments.append(Segment(
                Point(int(match.group(1)), int(match.group(2))),
                Point(int(match.group(3)), int(match.group(4)))
            ))

    # part 1
    field = defaultdict(int)
    for segment in segments:
        if segment.horizontal or segment.vertical:
            for point in segment.points():
                field[point] += 1

    print(sum(1 for count in field.values() if count > 1))

    # part 2
    for segment in segments:
        if not (segment.horizontal or segment.vertical):
            for point in segment.points():
                field[point] += 1

    print(sum(1 for count in field.values() if count > 1))


if __name__ == '__main__':
    main()
