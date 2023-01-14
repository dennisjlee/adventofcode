from __future__ import annotations

import math
import sys
from typing import NamedTuple, Iterable, Optional

from aoc2018.day16 import OperationMethods
from aoc2018.day19 import Instruction, execute, parse_lines


class Point(NamedTuple):
    x: int
    y: int


def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    depth = int(lines[0].split(': ')[1])
    target_x, target_y = lines[1].split(': ')[1].split(',')
    target = Point(int(target_x), int(target_y))
    width = target.x + 1
    height = target.y + 1

    mod_base = 20183

    geologic_indices: list[list[Optional[int]]] = [
        [None] * width
        for _ in range(height)
    ]

    erosion_levels: list[list[Optional[int]]] = [
        [None] * width
        for _ in range(height)
    ]

    def calc_erosion(ey: int, ex: int):
        erosion_levels[ey][ex] = (geologic_indices[ey][ex] + depth) % mod_base

    geologic_indices[0][0] = 0
    calc_erosion(0, 0)
    geologic_indices[target.y][target.x] = 0
    calc_erosion(target.y, target.x)
    for x in range(1, width):
        geologic_indices[0][x] = x * 16807
        calc_erosion(0, x)
    for y in range(1, height):
        geologic_indices[y][0] = y * 48271
        calc_erosion(y, 0)

    for y in range(1, height):
        for x in range(1, width):
            if y == target.y and x == target.x:
                continue
            geologic_indices[y][x] = erosion_levels[y-1][x] * erosion_levels[y][x-1]
            calc_erosion(y, x)

    risk_levels: list[list[int]] = [
        [erosion_levels[y][x] % 3 for x in range(width)]
        for y in range(height)
    ]
    print(sum(sum(risk_levels[y][x] for x in range(width))
              for y in range(height)))


if __name__ == '__main__':
    main()
