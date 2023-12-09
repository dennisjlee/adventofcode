from __future__ import annotations

import math
import re
from itertools import cycle
import sys


class Sequence:
    numbers: list[int]
    differences: Sequence | None

    def __init__(self, numbers: list[int]):
        self.numbers = numbers
        if any(n != 0 for n in self.numbers):
            self.differences = Sequence([numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)])
        else:
            self.differences = None

    def extrapolate_next(self):
        if not self.differences:
            return 0
        return self.numbers[-1] + self.differences.extrapolate_next()

    def extrapolate_prev(self):
        if not self.differences:
            return 0
        return self.numbers[0] - self.differences.extrapolate_prev()


def main():
    with open(sys.argv[1]) as f:
        sequences = [Sequence([int(w) for w in line.strip().split()])
                     for line in f.readlines()]

    print(sum(seq.extrapolate_next() for seq in sequences))
    print(sum(seq.extrapolate_prev() for seq in sequences))


if __name__ == '__main__':
    main()
