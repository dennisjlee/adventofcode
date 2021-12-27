import collections
import itertools
import re
import sys
from typing import NamedTuple, Optional


class Instruction(NamedTuple):
    op: str
    reg1: str
    arg: Optional[str]


def register_name_to_index(char: str):
    return ord(char) - ord('w')


def main():
    instruction_sets = []
    with open(sys.argv[1]) as f:
        instructions = None
        for i, line in enumerate(f.readlines()):
            args = line.strip().split()
            if len(args) == 2:
                instructions = [Instruction(args[0], args[1], None)]
                instruction_sets.append(instructions)
            else:
                instructions.append(Instruction(args[0], args[1], args[2]))

    for i, instruction_set in enumerate(instruction_sets):
        print(f'@functools.cache')
        print(f'def alu{i}(d, z):')
        print('    x = y = 0')
        for instruction in instruction_set:
            op = instruction.op
            reg = instruction.reg1

            if op == 'inp':
                print(f'    {reg} = d')
            else:
                arg = instruction.arg
                if op == 'add':
                    print(f'    {reg} += {arg}')
                elif op == 'mul':
                    print(f'    {reg} *= {arg}')
                elif op == 'div':
                    print(f'    {reg} = int({reg} / {arg})')
                elif op == 'mod':
                    print(f'    {reg} = {reg} % {arg}')
                elif op == 'eql':
                    print(f'    {reg} = int({reg} == {arg})')
        print('    return z')
        print('\n')


if __name__ == '__main__':
    main()
