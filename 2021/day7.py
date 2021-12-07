import math
import sys
from collections import Counter


def main():
    with open(sys.argv[1]) as f:
        orig_positions = [int(w) for w in f.readline().strip().split(',')]

    position_counts = Counter(orig_positions)
    print(part1(position_counts))
    print(part2(position_counts))


def part1(position_counts: dict[int, int]) -> int:
    unique_positions = position_counts.keys()
    best_cost = math.inf
    for dest in range(min(unique_positions), max(unique_positions) + 1):
        cost = sum(abs(pos - dest) * count for pos, count in position_counts.items())
        if cost < best_cost:
            best_cost = cost

    return best_cost


def part2(position_counts: dict[int, int]) -> int:
    unique_positions = position_counts.keys()
    best_cost = math.inf
    for dest in range(min(unique_positions), max(unique_positions) + 1):
        cost = sum(abs(pos - dest) * (abs(pos - dest) + 1) / 2 * count for pos, count in position_counts.items())
        if cost < best_cost:
            best_cost = cost

    return int(best_cost)


if __name__ == '__main__':
    main()
