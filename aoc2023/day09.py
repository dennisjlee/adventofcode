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

    def extrapolate_next_n(self, n: int):
        assert n >= 1
        if not self.differences:
            return [0] * n
        next_n_differences = self.differences.extrapolate_next_n(n)
        result = []
        for i in range(n - 1):
            if i == 0:
                result.append(self.numbers[-1] + next_n_differences[i])
            else:
                result.append(result[i - 1] + next_n_differences[i])
        return result


def main():
    with open(sys.argv[1]) as f:
        sequences = [Sequence([int(w) for w in line.strip().split()])
                     for line in f.readlines()]

    print(sum(seq.extrapolate_next() for seq in sequences))
    print(sum(seq.extrapolate_prev() for seq in sequences))


if __name__ == '__main__':
    main()
