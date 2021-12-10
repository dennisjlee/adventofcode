import sys
from collections import Counter


DISPLAY = {
    '0': frozenset('abcefg'),
    '1': frozenset('cf'),
    '2': frozenset('acdeg'),
    '3': frozenset('acdfg'),
    '4': frozenset('bcdf'),
    '5': frozenset('abdfg'),
    '6': frozenset('abdefg'),
    '7': frozenset('acf'),
    '8': frozenset('abcdefg'),
    '9': frozenset('abcdfg'),
}

REVERSE_DISPLAY = {v: k for k, v in DISPLAY.items()}


def main():
    easy_digit_counter = Counter()

    entries = []
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            signal_str, output_str = line.strip().split(' | ')
            outputs = output_str.split()
            for o in outputs:
                easy_digit_counter[len(o)] += 1

            signals = signal_str.split()
            entries.append((signals, outputs))

    # part 1
    print(sum(easy_digit_counter[len(DISPLAY[str(d)])] for d in (1, 4, 7, 8)))

    print(sum(decode(signals, outputs) for signals, outputs in entries))


ALL_LETTERS = set('abcdefg')


def decode(signals: list[str], outputs: list[str]) -> int:
    possible_mappings = {
        letter: set(ALL_LETTERS) for letter in ALL_LETTERS
    }
    signals = sorted(signals, key=len)
    # 1, 7, 4 will be first (segment lengths are 2, 3, 4)
    one_pattern = set(signals[0])
    for letter in one_pattern:
        possible_mappings[letter] &= DISPLAY['1']
    for letter in ALL_LETTERS - one_pattern:
        possible_mappings[letter] -= DISPLAY['1']

    seven_pattern = set(signals[1])
    for letter in seven_pattern:
        possible_mappings[letter] &= DISPLAY['7']
    for letter in ALL_LETTERS - seven_pattern:
        possible_mappings[letter] -= DISPLAY['7']

    four_pattern = set(signals[2])
    for letter in four_pattern:
        possible_mappings[letter] &= DISPLAY['4']
    for letter in ALL_LETTERS - four_pattern:
        possible_mappings[letter] -= DISPLAY['4']

    # 2, 3, 5 will be next in some order (5 segments)
    for pattern in map(set, signals[3:6]):
        for letter in pattern:
            possible_mappings[letter] &= (DISPLAY['2'] | DISPLAY['3'] | DISPLAY['5'])
        if pattern > one_pattern:
            # this is 3, it's the only number that contains all segments from 1
            three_pattern = pattern
            for letter in three_pattern:
                possible_mappings[letter] &= DISPLAY['3']
            for letter in ALL_LETTERS - three_pattern:
                possible_mappings[letter] -= DISPLAY['3']

    # 0, 6, 9 will be next in some order (6 segments)
    for pattern in map(set, signals[6:9]):
        for letter in pattern:
            possible_mappings[letter] &= (DISPLAY['0'] | DISPLAY['6'] | DISPLAY['9'])
        if not pattern > one_pattern:
            # this is 6, it's the only option that does not contain all segments from 1
            six_pattern = pattern
            for letter in six_pattern:
                possible_mappings[letter] &= DISPLAY['6']
            for letter in ALL_LETTERS - six_pattern:
                possible_mappings[letter] -= DISPLAY['6']

    assert all(len(v) == 1 for v in possible_mappings.values())

    digits = []
    for pattern in outputs:
        mapped_pattern = frozenset({next(iter(possible_mappings[letter])) for letter in pattern})
        digits.append(REVERSE_DISPLAY[mapped_pattern])

    return int(''.join(digits))


if __name__ == '__main__':
    main()
