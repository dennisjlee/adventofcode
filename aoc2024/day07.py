import math
import sys
from operator import add, mul
from typing import NamedTuple


def concatenate_ints(n1: int, n2: int) -> int:
    digit_count = int(math.log10(n2)) + 1
    return n1 * (10**digit_count) + n2


class Equation(NamedTuple):
    target: int
    operands: list[int]

    @staticmethod
    def parse(line: str):
        target, rest = line.split(": ")
        return Equation(int(target), [int(s) for s in rest.split()])

    def is_possibly_true(self, ops) -> bool:
        curr_results = {self.operands[0]}
        for n in self.operands[1:]:
            next_results = set()
            for r in curr_results:
                for op in ops:
                    r_prime = op(r, n)
                    if r_prime <= self.target:
                        next_results.add(r_prime)
            curr_results = next_results
        return self.target in curr_results


def main():
    with open(sys.argv[1]) as f:
        equations = [Equation.parse(line) for line in f.readlines()]

    ops_part1 = (add, mul)
    ops_part2 = (add, mul, concatenate_ints)
    part1_sum = 0
    part2_sum = 0
    for e in equations:
        if e.is_possibly_true(ops_part1):
            part1_sum += e.target
        elif e.is_possibly_true(ops_part2):
            part2_sum += e.target

    print(part1_sum)
    print(part1_sum + part2_sum)


if __name__ == "__main__":
    main()
