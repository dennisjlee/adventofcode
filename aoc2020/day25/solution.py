import sys
from typing import Tuple


MOD_BASE = 20201227


def main():
    with open(sys.argv[1]) as f:
        keys = [int(line.strip()) for line in f.readlines()]

    part1(7, (keys[0], keys[1]))


def part1(subject_number: int, target_numbers: Tuple[int, int]):
    loop_number = 0
    card_key, door_key = target_numbers
    card_loop_size = door_loop_size = None

    value = 1
    while card_loop_size is None or door_loop_size is None:
        value = (value * subject_number) % MOD_BASE
        loop_number += 1
        if value == card_key:
            card_loop_size = loop_number
        elif value == door_key:
            door_loop_size = loop_number

    print(card_loop_size, door_loop_size)
    value = 1
    for i in range(card_loop_size):
        value = (value * door_key) % MOD_BASE
    print(value)


if __name__ == '__main__':
    main()