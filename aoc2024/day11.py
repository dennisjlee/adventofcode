import math
import sys
from collections import Counter


def count_digits(n: int):
    return int(math.log10(n)) + 1


def main():
    with open(sys.argv[1]) as f:
        stones = [int(w) for w in f.read().strip().split()]

    original_stones = stones
    for i in range(25):
        stones = update_stones(stones)
    print(len(stones))

    stone_counter = Counter(original_stones)
    for i in range(75):
        stone_counter = update_stone_counter(stone_counter)
    print(stone_counter.total())


def update_stones(stones: list[int]):
    new_stones: list[int] = []
    for s in stones:
        if s == 0:
            new_stones.append(1)
        elif (digits := count_digits(s)) % 2 == 0:
            cutoff = 10 ** (digits // 2)
            new_stones.append(s // cutoff)
            new_stones.append(s % cutoff)
        else:
            new_stones.append(s * 2024)
    return new_stones


def update_stone_counter(stone_counter: Counter[int]):
    new_stones: Counter[int] = Counter()
    for s, count in stone_counter.items():
        if s == 0:
            new_stones[1] += count
        elif (digits := count_digits(s)) % 2 == 0:
            cutoff = 10 ** (digits // 2)
            new_stones[(s // cutoff)] += count
            new_stones[(s % cutoff)] += count
        else:
            new_stones[s * 2024] += count
    return new_stones


if __name__ == '__main__':
    main()
