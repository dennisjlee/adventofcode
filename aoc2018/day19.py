from __future__ import annotations

import math
import sys
from typing import NamedTuple, Iterable

from aoc2018.day16 import OperationMethods


class Instruction(NamedTuple):
    name: str
    a: int
    b: int
    c: int


def parse_lines(lines: list[str]) -> tuple[int, list[Instruction]]:
    _, ip_index = lines[0].split()
    ip_index = int(ip_index)

    instructions = []
    for line in lines[1:]:
        name, a, b, c = line.split()
        instructions.append(Instruction(name, int(a), int(b), int(c)))

    return ip_index, instructions


def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    ip_index, instructions = parse_lines(lines)

    registers = [0] * 6

    # slow way
    # execute(instructions, ip_index, registers, verbose=False)
    # print(registers)

    # turns out that this program essentially iterates two nested for loops
    # from 1 to reg4 and adds to reg0 if the two loop variables multiply to reg4.
    # so essentially reg0 will have the result of the sum of all factors of reg4.
    reg4 = 4 * 19 * 11 + (5 * 22 + 12)  # interpreted ops by hand
    print(sum(factors(reg4)))

    # part 2
    reg4 += (27 * 28 + 29) * 30 * 14 * 32  # interpreted ops by hand!
    print(sum(factors(reg4)))


def factors(n: int) -> Iterable[int]:
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            yield i
            yield n // i


def execute(instructions: list[Instruction], ip_index: int, registers: list[int], verbose=False):
    ip = 0
    step = 0
    while 0 <= ip < len(instructions):
        step += 1
        op = instructions[ip]
        registers[ip_index] = ip
        if verbose and step > 100_000:
            print(f'step={step} ip={ip} {registers}')
            break
        OperationMethods[op.name](op.a, op.b, op.c, registers)
        if verbose and step > 100_000:
            print(f'\t{op} {registers}')
            pass
        ip = registers[ip_index] + 1


if __name__ == '__main__':
    main()
