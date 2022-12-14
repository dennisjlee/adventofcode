#!/usr/bin/env python3

import sys
from collections import Counter

def main(filename):
    with open(filename) as f:
        ids = [l.strip() for l in f.readlines()]
    # There's probably a better way than doing a brute force N*N comparison..
    # But the inputs not that long in the end
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            substitution_count = 0
            sub_index = -1
            for k, (c1, c2) in enumerate(zip(ids[i], ids[j])):
                if c1 != c2:
                    sub_index = k
                    substitution_count += 1
                    if substitution_count > 1:
                        break
            if substitution_count == 1:
                matching_id = ids[i]
                print(matching_id[:sub_index] + matching_id[sub_index+1:])
                return


if __name__ == '__main__':
    main(sys.argv[1])
