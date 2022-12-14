#!/usr/bin/env python3

from collections import namedtuple, Counter
import sys
import re

class Claim(namedtuple('Claim', ['claim_id', 'x', 'y', 'w', 'h'])):
    pass

def main(filename):
    regex = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    points = {}
    untouched_claim_ids = set()
    with open(filename) as f:
        for line in f:
            match = regex.match(line)
            claim = Claim(*map(int, match.groups()))
            untouched_claim_ids.add(claim.claim_id)
            for x in range(claim.x, claim.x + claim.w):
                for y in range(claim.y, claim.y + claim.h):
                    p = (x, y)
                    if p in points:
                        untouched_claim_ids.discard(claim.claim_id)
                        untouched_claim_ids.discard(points[p])
                    else:
                        points[p] = claim.claim_id

    print(untouched_claim_ids)


if __name__ == '__main__':
    main(sys.argv[1])
