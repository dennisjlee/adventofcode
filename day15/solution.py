from collections import defaultdict
import re
import sys


def main():
    with open(sys.argv[1]) as f:
        starting_numbers = [int(s) for s in f.readline().split(',')]

    part1(starting_numbers)
    part2(starting_numbers)


def part1(starting_numbers):
    last_seen_indexes = defaultdict(list)
    numbers = []
    n = -1
    for i in range(2020):
        if i < len(starting_numbers):
            n = starting_numbers[i]
            numbers.append(n)
            last_seen_indexes[n].append(i)
        else:
            last_seen = last_seen_indexes[n]
            if len(last_seen) < 2:
                n = 0
                numbers.append(n)
                last_seen_indexes[n].append(i)
            else:
                n = last_seen[-1] - last_seen[-2]
                numbers.append(n)
                last_seen_indexes[n].append(i)
    print(n)


def part2(starting_numbers):
    last_seen_indexes = {}
    n = -1
    for i in range(30_000_000):
        if i < len(starting_numbers):
            n = starting_numbers[i]
            last_seen_indexes[n] = (i, None)
        else:
            last_seen, previous_seen = last_seen_indexes[n]
            if previous_seen is None:
                n = 0
            else:
                n = last_seen - previous_seen

            last, prev = last_seen_indexes.get(n, (None, None))
            last_seen_indexes[n] = (i, last)
    print(n)


if __name__ == '__main__':
    main()
