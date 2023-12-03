import operator
import re
import sys
from collections import defaultdict
from functools import reduce
from typing import NamedTuple


class Coord(NamedTuple):
    x: int
    y: int


def main():
    symbol_regex = re.compile(r'[^\d.]')
    number_regex = re.compile(r'\d+')
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    symbols: dict[Coord, str] = {}
    for y, line in enumerate(lines):
        for match in symbol_regex.finditer(line.strip()):
            symbol = match.group(0)
            coord = Coord(match.start(), y)
            symbols[coord] = symbol

    part_number_sum = 0
    gear_numbers = defaultdict(list)
    for y, line in enumerate(lines):
        for match in number_regex.finditer(line.strip()):
            number = int(match.group(0))
            for yy in range(max(0, y-1), min(len(lines), y+2)):
                for x in range(max(0, match.start()-1), min(len(line), match.end()+1)):
                    coord = Coord(x, yy)
                    if coord in symbols:
                        part_number_sum += number
                        if symbols[coord] == '*':
                            gear_numbers[coord].append(number)

    print(part_number_sum)

    gear_ratio_sum = 0
    for numbers in gear_numbers.values():
        if len(numbers) == 2:
            gear_ratio_sum += numbers[0] * numbers[1]
    print(gear_ratio_sum)



if __name__ == '__main__':
    main()
