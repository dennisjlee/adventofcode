from __future__ import annotations

import sys
from pathlib import Path
from typing import NamedTuple


class BatteryBank(NamedTuple):
    batteries: list[int]

    @classmethod
    def parse(cls, line: str) -> BatteryBank:
        return BatteryBank([int(c) for c in line.strip()])

    def __str__(self) -> str:
        return ''.join(str(b) for b in self.batteries)

    def max_joltage2(self) -> int:
        i, max_tens = max(enumerate(self.batteries[:-1]), key=lambda x: x[1])
        max_ones = max(self.batteries[i+1:])
        return max_tens * 10 + max_ones

    def max_joltage(self, ndigits: int) -> int:
        total = 0
        start_index = 0
        length = len(self.batteries)
        for n in range(ndigits - 1, -1, -1):
            max_digit, i = max(
                (self.batteries[i], -i)
                for i in range(start_index, length - n)
            )
            start_index = -i + 1
            total = total * 10 + max_digit
        return total

def main():
    with Path(sys.argv[1]).open() as f:
        battery_banks = [BatteryBank.parse(line) for line in f.readlines()]

    print(sum(bb.max_joltage2() for bb in battery_banks))
    print(sum(bb.max_joltage(12) for bb in battery_banks))


if __name__ == "__main__":
    main()