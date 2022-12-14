from __future__ import annotations
import sys
from collections import namedtuple


class InclusiveRange(namedtuple('InclusiveRange', ['start', 'end'])):
    def contains(self, other: InclusiveRange):
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other: InclusiveRange):
        return self.start <= other.end and self.end >= other.start


def parse_inclusive_range(s: str) -> InclusiveRange:
    start, end = s.split('-')
    return InclusiveRange(int(start), int(end))


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    assignments = []
    for line in lines:
        first, second = line.split(',')
        assignments.append((parse_inclusive_range(first), parse_inclusive_range(second)))

    print(len([1 for left, right in assignments if left.contains(right) or right.contains(left)]))

    print(len([1 for left, right in assignments if left.overlaps(right)]))


if __name__ == '__main__':
    main()
