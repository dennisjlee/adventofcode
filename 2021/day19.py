from __future__ import annotations

import itertools
import math
import sys
from functools import reduce
from typing import *


class Point3(NamedTuple):
    x: int
    y: int
    z: int

    def __repr__(self):
        return f'({self.x},{self.y},{self.z})'


class Scanner:
    id: int
    detected: list[Point3]

    def __init__(self, scanner_id: int, detected: list[Point3]):
        self.id = scanner_id
        self.detected = detected


def main():
    scanners: list[Scanner] = []
    with open(sys.argv[1]) as f:
        scanner_blocks = f.read().strip().split('\n\n')
        for block in scanner_blocks:
            block_lines = block.split('\n')
            scanner_id = int(block_lines[0].split()[2])
            points = [
                Point3(*line.strip().split(',')) for line in block_lines[1:]
            ]
            scanners.append(Scanner(scanner_id, points))

    for scanner in scanners:
        print('\n', scanner.id)
        print('\n'.join(str(p) for p in scanner.detected))


if __name__ == '__main__':
    main()
