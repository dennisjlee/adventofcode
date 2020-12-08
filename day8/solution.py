from collections import namedtuple 
import re
import sys

instruction_regex = re.compile(r'([a-z]{3}) ([+-]\d+)')

def main():
    instructions = []
    with open(sys.argv[1]) as f:
        for line in f:
            match = instruction_regex.match(line.strip())
            operation, argstr = match.groups()
            argument = int(argstr)
            instructions.append((operation, argument))

    # part 1
    acc, _ = simulate(instructions)
    print(acc)

    # part 2
    for i in reversed(range(len(instructions))):
        operation, argument = instructions[i]
        if operation == 'acc':
            continue
        new_operation = 'jmp' if operation == 'nop' else 'nop'
        debugged_instructions = (
            instructions[:i] +
            [(new_operation, argument)] + 
            instructions[i+1:])

        acc, position = simulate(debugged_instructions)
        if position == len(instructions):
            print(acc)
            return



def simulate(instructions):
    position = 0
    seen_indexes = set()
    accumulator = 0
    while position not in seen_indexes and position < len(instructions):
        seen_indexes.add(position)
        operation, argument = instructions[position]
        if operation == 'nop':
            position += 1
        elif operation == 'acc':
            accumulator += argument
            position += 1
        elif operation == 'jmp':
            position += argument

    return accumulator, position




if __name__ == '__main__':
    main()
