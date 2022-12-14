#!/usr/bin/env python3

import sys
import string
import re

def main(filename):
    with open(filename) as f:
        polymer = f.readline().strip()

    print(min(react_polymer(remove_letter(letter, polymer))
        for letter in string.ascii_lowercase))


def remove_letter(letter, polymer):
    return re.sub(letter, '', polymer, flags=re.I)


def react_polymer(polymer):
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

    return len(stack)


if __name__ == '__main__':
    main(sys.argv[1])
