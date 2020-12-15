from collections import defaultdict
import sys


def main():
    with open(sys.argv[1]) as f:
        starting_numbers = [int(s) for s in f.readline().split(',')]

    v3(starting_numbers, 2020)
    v3(starting_numbers, 30000000)


# note that v1, v2, v3 all do the same things, just at various levels of
# refinement / performance


def v1(starting_numbers, stop_index):
    last_seen_indexes = defaultdict(list)
    numbers = []
    n = -1
    for i in range(stop_index):
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


def v2(starting_numbers, stop_index):
    last_seen_indexes = {}
    n = -1
    for i in range(stop_index):
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


def v3(starting_numbers, stop_index):
    last_seen_indexes = {n: i for i, n in enumerate(starting_numbers[:-1])}
    prev_n = starting_numbers[-1]
    for i in range(len(starting_numbers), stop_index):
        if prev_n in last_seen_indexes:
            n = i - 1 - last_seen_indexes[prev_n]
        else:
            n = 0
        last_seen_indexes[prev_n] = i - 1
        prev_n = n
    print(n)


if __name__ == '__main__':
    main()
