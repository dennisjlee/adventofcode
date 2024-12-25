from __future__ import annotations

import sys
from dataclasses import dataclass, field


@dataclass
class ProgramState:
    registers: list[int]
    instr: int = 0
    output: list[int] = field(init=False, default_factory=list)


@dataclass
class Instruction:
    operand: int

    @staticmethod
    def parse(opcode: int, operand: int):
        if opcode == 1:
            return BxlInstruction(operand)
        elif opcode == 2:
            return BstInstruction(operand)
        elif opcode == 3:
            return JnzInstruction(operand)
        elif opcode == 4:
            return BxcInstruction(operand)
        elif opcode == 5:
            return OutInstruction(operand)
        else:
            # adv, bdv or cdv
            div_reg_index = [0, 6, 7].index(opcode)
            return DivInstruction(operand, div_reg_index)

    def execute(self, state: ProgramState):
        state.instr += 2

    def combo(self, registers: list[int]) -> int:
        if self.operand <= 3:
            return self.operand
        elif self.operand >= 7:
            raise ValueError("Invalid combo operand")
        else:
            return registers[self.operand - 4]


@dataclass
class DivInstruction(Instruction):
    register_index: int

    def execute(self, state: ProgramState):
        state.registers[self.register_index] = self.div(state.registers)

        super().execute(state)

    def div(self, registers: list[int]):
        numerator = registers[0]
        denominator = 2 ** self.combo(registers)
        return numerator // denominator


@dataclass
class BxlInstruction(Instruction):
    def execute(self, state: ProgramState):
        state.registers[1] ^= self.operand
        super().execute(state)


@dataclass
class BstInstruction(Instruction):
    def execute(self, state: ProgramState):
        state.registers[1] = self.combo(state.registers) % 8
        super().execute(state)


@dataclass
class JnzInstruction(Instruction):
    def execute(self, state: ProgramState):
        if state.registers[0] != 0:
            state.instr = self.operand
        else:
            super().execute(state)


@dataclass
class BxcInstruction(Instruction):
    def execute(self, state: ProgramState):
        state.registers[1] ^= state.registers[2]
        super().execute(state)


@dataclass
class OutInstruction(Instruction):
    def execute(self, state: ProgramState):
        state.output.append(self.combo(state.registers) % 8)
        super().execute(state)


def main():
    with open(sys.argv[1]) as f:
        registers_str, program_str = f.read().split("\n\n")

    original_registers = [
        int(register_line.split()[-1])
        for register_line in registers_str.strip().split("\n")
    ]

    program = [int(s) for s in program_str.split()[-1].split(",")]

    instructions = [
        Instruction.parse(program[i], program[i + 1]) for i in range(0, len(program), 2)
    ]
    output = execute_program(original_registers, instructions)
    print(",".join(str(o) for o in output))

    part2(program)


def execute_program(registers: list[int], instructions: list[Instruction]):
    state = ProgramState(registers)
    while 0 <= state.instr < 2 * len(instructions):
        if state.instr % 2 == 1:
            raise ValueError(f"Unexpected odd value of instr pointer: {state.instr}")
        instruction = instructions[state.instr // 2]
        instruction.execute(state)
    return state.output


# see day17_annotated.txt
# to get 16 output digits, we need 8**15 <= a < 8**16
def compute(a: int):
    output: list[int] = []
    while a:
        b = (a % 8) ^ 1
        c = a // (2**b)
        a //= 8
        b = b ^ 4 ^ c
        output.append(b % 8)
    return output


def part2(program: list[int]):
    # Treat the input `a` as a 16-digit number in octal.
    # The most significant input digit will affect the last digit of program output, and
    # the next most significant input digit will affect the second last digit of output,
    # etc.
    a = 0
    for place in range(15, -1, -1):
        for digit in range(8):
            test_a = a | (digit << (place * 3))
            output = compute(test_a)
            if output[place:] == program[place:]:
                a = test_a
                break
        else:
            # In some situations, the contents of one digit are not enough to get the
            # output digit we want, and we have to start manipulating the previous digit
            # too
            for digits in range(9, 63):
                test_a = a | (digits << (place * 3))
                output = compute(test_a)
                if output[place:] == program[place:]:
                    a = test_a
                    break
    print(a)


if __name__ == "__main__":
    main()
