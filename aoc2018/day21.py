from __future__ import annotations

import math
import sys
from typing import NamedTuple, Iterable

from aoc2018.day16 import OperationMethods
from aoc2018.day19 import Instruction, execute, parse_lines


def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    ip_index, instructions = parse_lines(lines)
    registers = [0] * 6

    # slow way
    execute(instructions, ip_index, registers, verbose=False)
    # print(registers)




if __name__ == '__main__':
    main()
