#!/usr/bin/env python3

import sys
from collections import Counter

def main(filename):
    two_count = 0
    three_count = 0
    with open(filename) as f:
        for line in f:
            seen_two = False
            seen_three = False
            char_counter = Counter(line.strip())
            for c, count in char_counter.items():
                if count == 2 and not seen_two:
                    two_count += 1
                    seen_two = True
                elif count == 3 and not seen_three:
                    three_count += 1
                    seen_three = True
                if seen_two and seen_three:
                    break
    print(two_count * three_count)


if __name__ == '__main__':
    main(sys.argv[1])
