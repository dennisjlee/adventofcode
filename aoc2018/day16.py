import typing
from collections import namedtuple
import inspect
import re
import sys

SAMPLE_PATTERN = re.compile(r'Before:\s*\[(.+?)]\n(.+?)\nAfter:\s*\[(.+?)]')


class Sample(typing.NamedTuple):
    before: list[int]
    instruction: list[int]
    after: list[int]

    def check(self, operation):
        registers = self.before[:]
        operation(*self.instruction[1:], registers)
        return registers == self.after


class Operations:
    @staticmethod
    def addr(a, b, c, registers):
        registers[c] = registers[a] + registers[b]

    @staticmethod
    def addi(a, b, c, registers):
        registers[c] = registers[a] + b

    @staticmethod
    def mulr(a, b, c, registers):
        registers[c] = registers[a] * registers[b]

    @staticmethod
    def muli(a, b, c, registers):
        registers[c] = registers[a] * b

    @staticmethod
    def banr(a, b, c, registers):
        registers[c] = registers[a] & registers[b]

    @staticmethod
    def bani(a, b, c, registers):
        registers[c] = registers[a] & b

    @staticmethod
    def borr(a, b, c, registers):
        registers[c] = registers[a] | registers[b]

    @staticmethod
    def bori(a, b, c, registers):
        registers[c] = registers[a] | b

    @staticmethod
    def setr(a, b, c, registers):
        registers[c] = registers[a]

    @staticmethod
    def seti(a, b, c, registers):
        registers[c] = a

    @staticmethod
    def gtir(a, b, c, registers):
        registers[c] = int(a > registers[b])

    @staticmethod
    def gtri(a, b, c, registers):
        registers[c] = int(registers[a] > b)

    @staticmethod
    def gtrr(a, b, c, registers):
        registers[c] = int(registers[a] > registers[b])

    @staticmethod
    def eqir(a, b, c, registers):
        registers[c] = int(a == registers[b])

    @staticmethod
    def eqri(a, b, c, registers):
        registers[c] = int(registers[a] == b)

    @staticmethod
    def eqrr(a, b, c, registers):
        registers[c] = int(registers[a] == registers[b])


OperationMethods = dict(inspect.getmembers(Operations, inspect.isfunction))


def main():
    samples: list[Sample] = []
    with open(sys.argv[1]) as f:
        samples_text, test_program_text = f.read().split('\n\n\n')
        for match in SAMPLE_PATTERN.finditer(samples_text):
            before = [int(s) for s in match.group(1).split(', ')]
            instruction = [int(s) for s in match.group(2).split(' ')]
            after = [int(s) for s in match.group(3).split(', ')]
            samples.append(Sample(before, instruction, after))

        test_instructions = [
            [int(n) for n in line.strip().split(' ')]
            for line in test_program_text.strip().split('\n')
        ]

    # part 1
    very_ambiguous_samples = 0
    for sample in samples:
        possible_opcodes = 0
        for name, operation in OperationMethods.items():
            if sample.check(operation):
                possible_opcodes += 1
            if possible_opcodes >= 3:
                very_ambiguous_samples += 1
                break

    print(very_ambiguous_samples)

    # part 2
    opcodes = set(sample.instruction[0] for sample in samples)
    operation_map: dict[int, set[str]] = {opcode: set(OperationMethods.keys()) for opcode in opcodes}
    final_operation_map: dict[int, str] = {}
    for sample in samples:
        opcode = sample.instruction[0]
        possibilities = operation_map[opcode]
        if len(possibilities) == 1:
            continue

        filtered_possibilities = {
            opname for opname in possibilities
            if sample.check(OperationMethods[opname])
        }
        operation_map[opcode] = filtered_possibilities

    while len(operation_map):
        for opcode, possibilities in list(operation_map.items()):
            if len(possibilities) == 1:
                final_operation_map[opcode] = next(iter(possibilities))
                del operation_map[opcode]
                for other_opcode, other_possibilities in operation_map.items():
                    other_possibilities -= possibilities

    registers = [0, 0, 0, 0]
    for instruction in test_instructions:
        operation = OperationMethods[final_operation_map[instruction[0]]]
        operation(*instruction[1:], registers)

    print(registers[0])


if __name__ == '__main__':
    main()
