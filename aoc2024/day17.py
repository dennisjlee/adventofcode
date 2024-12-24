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

    registers = [
        int(register_line.split()[-1])
        for register_line in registers_str.strip().split("\n")
    ]

    program = [int(s) for s in program_str.split()[-1].split(",")]

    state = ProgramState(registers)
    instructions = [
        Instruction.parse(program[i], program[i + 1]) for i in range(0, len(program), 2)
    ]
    while 0 <= state.instr < len(program):
        if state.instr % 2 == 1:
            raise ValueError(f"Unexpected odd value of instr pointer: {state.instr}")
        instruction = instructions[state.instr // 2]
        instruction.execute(state)

    print(",".join(str(o) for o in state.output))


if __name__ == "__main__":
    main()
