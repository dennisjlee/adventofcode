import re
import sys
from typing import Dict

mask_re = re.compile(r'mask = (\w+)')
mem_re = re.compile(r'mem\[(\d+)\] = (\d+)')


def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f]

    part1(lines)
    part2(lines)


ALL_ONES = (1 << 36) - 1


def part1(lines):
    ones_mask = 0
    zeros_mask = ALL_ONES

    memory: Dict[int] = {}
    for line in lines:
        mask_match = mask_re.match(line)
        if mask_match:
            mask = mask_match.group(1)
            ones_mask = int(mask.replace('X', '0'), 2)
            zeros_mask = int(mask.replace('X', '1'), 2)
        else:
            mem_match = mem_re.match(line)
            if mem_match:
                address = int(mem_match.group(1), 10)
                value = int(mem_match.group(2), 10)
                masked_value = (value | ones_mask) & zeros_mask
                memory[address] = masked_value
            else:
                raise AssertionError('no match found for line ' + line)

    print(sum(memory.values()))


def part2(lines):
    ones_mask = 0
    floating_bits = []
    memory: Dict[int] = {}
    for line in lines:
        mask_match = mask_re.match(line)
        if mask_match:
            mask = mask_match.group(1)
            ones_mask = int(mask.replace('X', '0'), 2)
            floating_bits = [(35 - i) for i, char in enumerate(mask) if char == 'X']
        else:
            mem_match = mem_re.match(line)
            if mem_match:
                address = int(mem_match.group(1), 10)
                value = int(mem_match.group(2), 10)
                initial_masked_address = (address | ones_mask)
                if not floating_bits:
                    memory[initial_masked_address] = value
                else:
                    masked_address = initial_masked_address
                    # model the inclusion of each floating bit with an n-bit number
                    for floating_bits_enabled in range(1 << len(floating_bits)):
                        for i, bit_index in enumerate(floating_bits):
                            enabled = floating_bits_enabled & (1 << i)
                            if enabled:
                                masked_address |= 1 << bit_index
                            else:
                                masked_address &= ALL_ONES ^ (1 << bit_index)
                        memory[masked_address] = value
            else:
                raise AssertionError('no match found for line ' + line)

    print(sum(memory.values()))


def debug(n):
    print(format(n, '036b'))


if __name__ == '__main__':
    main()
