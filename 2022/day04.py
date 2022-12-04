import sys
from collections import namedtuple


class Assignment(namedtuple('Assignment', ['start', 'end'])):
    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other):
        return self.start <= other.end and self.end >= other.start

def parse_assignment(s: str):
    start, end = s.split('-')
    return Assignment(int(start), int(end))

def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    assignments = []
    for line in lines:
        first, second = line.split(',')
        assignments.append((parse_assignment(first), parse_assignment(second)))

    print(len([1 for left, right in assignments if left.contains(right) or right.contains(left)]))

    print(len([1 for left, right in assignments if left.overlaps(right)]))


if __name__ == '__main__':
    main()
