from __future__ import annotations

import math
from typing import NamedTuple, Optional
import re
import sys


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    additions = [0] * 500
    next_cycle = 0
    for line in lines:
        if line == 'noop':
            next_cycle += 1
        else:
            _, v = line.split()
            next_cycle += 1
            additions[next_cycle] = int(v)
            next_cycle += 1

    x = 1
    signal_strengths = []
    for cycle in range(220):
        if (cycle % 40) == 19:
            signal_strengths.append((cycle + 1) * x)
        x += additions[cycle]

    print(sum(signal_strengths))

    crt = [
        ['.'] * 40
        for _ in range(6)
    ]
    reg_x = 1
    for cycle in range(240):
        crt_x = cycle % 40
        crt_y = cycle // 40

        if reg_x - 1 <= crt_x <= reg_x + 1:
            crt[crt_y][crt_x] = '#'

        # end cycle
        reg_x += additions[cycle]

    print('\n'.join(''.join(row) for row in crt))


if __name__ == '__main__':
    main()
