#!/usr/bin/env python3

from collections import namedtuple, Counter
import sys
import re

class Claim(namedtuple('Claim', ['claim_id', 'x', 'y', 'w', 'h'])):
    pass

def main(filename):
    regex = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    points = Counter()
    with open(filename) as f:
        for line in f:
            match = regex.match(line)
            claim = Claim(*map(int, match.groups()))
            for x in range(claim.x, claim.x + claim.w):
                for y in range(claim.y, claim.y + claim.h):
                    points[(x,y)] += 1

    duplicated_points = 0
    for point, count in points.most_common():
        if count <= 1:
            break
        duplicated_points += 1

    print(duplicated_points)


if __name__ == '__main__':
    main(sys.argv[1])
