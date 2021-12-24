from __future__ import annotations
from collections import deque
import itertools
import sys
from typing import Optional, Iterable, Union, NamedTuple

from copy import copy


class Instruction(NamedTuple):
    instr: str
    reg1: int
    reg2: Optional[int]
    literal: Optional[int]


class CacheKey(NamedTuple):
    digit: int
    registers: tuple


class ALU:
    def __init__(self, instruction_set: list[Instruction]):
        self.registers = [0, 0, 0, 0]
        self.instruction_set = instruction_set
        self.input = None
        self.cache: dict[CacheKey, tuple] = {}

    def reset_registers(self):
        self.set_registers((0, 0, 0, 0))

    def set_registers(self, values):
        r = self.registers
        r[0] = values[0]
        r[1] = values[1]
        r[2] = values[2]
        r[3] = values[3]

    def copy_registers(self, prev_alu: ALU):
        self.set_registers(prev_alu.registers)

    def execute_all(self, digit: int):
        self.input = digit
        cache_key = CacheKey(digit, tuple(self.registers))
        if cache_key in self.cache:
            self.set_registers(self.cache[cache_key])
        else:
            for instruction in self.instruction_set:
                self.execute(instruction)
            self.cache[cache_key] = tuple(self.registers)

    def execute(self, instruction: Instruction):
        r = self.registers
        instr = instruction.instr
        reg = instruction.reg1

        if instr == 'inp':
            r[reg] = self.input
            return

        if instruction.reg2 is not None:
            reg2 = instruction.reg2
            if instr == 'add':
                r[reg] += r[reg2]
            elif instr == 'mul':
                r[reg] *= r[reg2]
            elif instr == 'div':
                r[reg] = int(r[reg] / r[reg2])
            elif instr == 'mod':
                r[reg] = r[reg] % r[reg2]
            elif instr == 'eql':
                r[reg] = int(r[reg] == r[reg2])
        else:
            val = instruction.literal
            if instr == 'add':
                r[reg] += val
            elif instr == 'mul':
                r[reg] *= val
            elif instr == 'div':
                r[reg] = int(r[reg] / val)
            elif instr == 'mod':
                r[reg] = r[reg] % val
            elif instr == 'eql':
                r[reg] = int(r[reg] == val)

    @property
    def is_valid(self):
        return self.registers[-1] == 0


def register_name_to_index(char: str):
    return ord(char) - ord('w')


def main():
    instruction_sets = []
    with open(sys.argv[1]) as f:
        instructions = None
        for i, line in enumerate(f.readlines()):
            args = line.strip().split()
            if len(args) == 2:
                instructions = [Instruction(args[0], register_name_to_index(args[1]), None, None)]
                instruction_sets.append(instructions)
            else:
                try:
                    number = int(args[2])
                    instructions.append(Instruction(args[0], register_name_to_index(args[1]), None, number))
                except ValueError:
                    instructions.append(
                        Instruction(args[0], register_name_to_index(args[1]), register_name_to_index(args[2]), None))

    digits = [9] * 14
    alus = []
    assert len(instruction_sets) == 14
    for i in range(14):
        alu = ALU(instruction_sets[i])
        if i > 0:
            alu.copy_registers(alus[i - 1])
        alu.execute_all(digits[i])
        alus.append(alu)

    counter = 0
    while any(d > 1 for d in digits):
        counter += 1
        if counter % 100000 == 0:
            print('currently trying number', ''.join(str(d) for d in digits))

        # if counter % 5_000_000 == 0:
        #     return

        for j in range(13, -1, -1):
            digits[j] = (digits[j] - 2) % 9 + 1
            if digits[j] < 9:
                for i in range(j, 14):
                    if i > 0:
                        alus[i].copy_registers(alus[i - 1])
                    else:
                        alus[i].reset_registers()
                    alus[i].execute_all(digits[i])
                break
        if alus[-1].is_valid:
            print(''.join(str(d) for d in digits))
            break


if __name__ == '__main__':
    main()

