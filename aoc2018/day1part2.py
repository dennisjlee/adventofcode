#!/usr/bin/env python3

import itertools
import sys

def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    numbers = [int(line.strip()) for line in lines]
    print(find_first_repeated_sum(numbers))

def find_first_repeated_sum(numbers):
    current_sum = 0
    seen = {0}
    for num in itertools.cycle(numbers):
        current_sum += num
        if current_sum in seen:
            return current_sum
        else:
            seen.add(current_sum)

if __name__ == '__main__':
    main(sys.argv[1])
