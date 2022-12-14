from __future__ import annotations

import math
import time

INPUT = '157901'

MAX_SIZE = math.inf
# MAX_SIZE = 10_000_000
PRINT = False


def main():
    start = time.perf_counter()
    try:
        print(part1(INPUT))
        print(part2(INPUT))
    finally:
        end = time.perf_counter()
        print(f'Elapsed time: {end - start}s')


def part1(target: str):
    state = [3, 7]
    i = 0
    j = 1
    count = int(target)
    while len(state) < count + 10:
        score1 = state[i]
        score2 = state[j]
        next_num = score1 + score2
        if next_num >= 10:
            state.append(1)
        state.append(next_num % 10)
        i = (i + 1 + score1) % len(state)
        j = (j + 1 + score2) % len(state)

    return int(''.join(str(d) for d in state[count:count + 10]))


def part2(target: str):
    state = bytearray([3, 7])
    i = 0
    j = 1
    target_array = bytearray([int(c) for c in target])
    target_len = len(target_array)
    size = len(state)
    while size < MAX_SIZE:
        if PRINT and size % 1_000_000 == 0:
            print(size)
        score1 = state[i]
        score2 = state[j]
        next_num = score1 + score2
        if next_num >= 10:
            size += 2
            state.append(1)
            if state.endswith(target_array):
                break
            state.append(next_num % 10)
            if state.endswith(target_array):
                break
        else:
            size += 1
            state.append(next_num)
            if state.endswith(target_array):
                break

        i = (i + 1 + score1) % size
        j = (j + 1 + score2) % size

    return len(state) - target_len


if __name__ == '__main__':
    main()
