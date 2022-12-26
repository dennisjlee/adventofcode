from __future__ import annotations

import sys
from math import log, ceil

DIGIT_MAP = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}

REVERSE_DIGIT_MAP = {v: k for k, v in DIGIT_MAP.items()}


class SnafuNumber:
    number: int

    def __init__(self, snafu: str):
        total = 0
        order = 1
        for c in reversed(snafu):
            total += DIGIT_MAP[c] * order
            order *= 5
        self.number = total

    def __repr__(self):
        return f'SnafuNumber({self.number})'

    @staticmethod
    def to_snafu(decimal: int) -> str:
        assert decimal > 0
        position = ceil(log(decimal) / log(5))
        digits = [0] * (position + 1)
        while decimal != 0:
            factor = 5 ** position
            digit = round(decimal / factor)
            digits[position] = digit
            decimal -= digit * factor
            position -= 1

        if digits[-1] == 0:
            del digits[-1]
        return ''.join(REVERSE_DIGIT_MAP[digit] for digit in reversed(digits))


def main():
    with open(sys.argv[1]) as f:
        snafu_numbers = [SnafuNumber(line.strip()) for line in f.readlines()]

    print(snafu_numbers)
    total = sum(n.number for n in snafu_numbers)
    print(total, SnafuNumber.to_snafu(total))


if __name__ == '__main__':
    main()
