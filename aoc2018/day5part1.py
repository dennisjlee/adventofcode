#!/usr/bin/env python3

import sys

def main(filename):
    with open(filename) as f:
        polymer = f.readline().strip()

    stack = []
    for c in polymer:
        val = ord(c)
        # Lower-case and upper-case versions of an ASCII letter are always 32 apart
        # (e.g. 'A' => 65, 'a' => 97), so XORing two chars will yield 32 if they are
        # opposite cases of the same letter.
        if len(stack) > 0 and (stack[-1] ^ val == 32):
            stack.pop()
        else:
            stack.append(val)

    print(len(stack))


if __name__ == '__main__':
    main(sys.argv[1])
