import functools
import re
import sys


def main():
    with open(sys.argv[1]) as f:
        towels_str, patterns_str = f.read().split("\n\n")

    towels = towels_str.strip().split(', ')
    patterns = patterns_str.strip().split('\n')

    towel_regex = re.compile(rf'(?:{"|".join(towels)})+')
    print(sum(1 for pattern in patterns if towel_regex.fullmatch(pattern)))

    print(sum(part2(tuple(towels), pattern, towel_regex, 0) for pattern in patterns))


@functools.cache
def part2(towels: tuple[str], towel_pattern: str, regex: re.Pattern, pos=0) -> int:
    if pos == len(towel_pattern):
        return 1
    if not regex.fullmatch(towel_pattern, pos):
        return 0
    possible_ways = 0
    for towel in towels:
        if towel_pattern.startswith(towel, pos):
            possible_ways += part2(towels, towel_pattern, regex, pos + len(towel))
    return possible_ways


if __name__ == "__main__":
    main()
