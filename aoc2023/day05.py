import re
import sys
import bisect
import math
from typing import NamedTuple


class Range(NamedTuple):
    start: int
    end: int


class RangeDest(NamedTuple):
    range: Range
    dest_start: int


class RangeMap:
    ranges: list[RangeDest]

    def __init__(self):
        self.ranges = []

    def add(self, dest_start: int, source_start: int, length: int):
        r = Range(source_start, source_start + length)
        range_dest = RangeDest(r, dest_start)
        bisect.insort(self.ranges, range_dest)

    def get_dest(self, source: int) -> int:
        i = bisect.bisect_right(self.ranges, source, key=lambda r: r.range.start)
        if i > 0:
            r, dest_start = self.ranges[i - 1]
            if r.start <= source < r.end:
                return dest_start + source - r.start
        return source

    def get_dest_ranges(self, source: Range) -> list[Range]:
        i = bisect.bisect_right(self.ranges, source.start, key=lambda r: r.range.start)
        if i > 0:
            r, dest_start = self.ranges[i - 1]
            if r.start <= source.start < r.end:
                if source.end < r.end:
                    return [Range(dest_start + source.start - r.start, dest_start + source.end - r.start)]
                else:
                    split_range = Range(r.end, source.end)
                    return [
                        Range(dest_start + source.start - r.start, dest_start + r.end - r.start),
                        *self.get_dest_ranges(split_range)
                    ]

        return [source]


def main():
    with open(sys.argv[1]) as f:
        all_text = f.read()

    blocks = all_text.split('\n\n')
    initial_seeds = [int(s) for s in blocks[0].split(': ')[1].split()]

    maps: list[RangeMap] = []
    for block in blocks[1:]:
        range_map = RangeMap()
        for line in block.splitlines()[1:]:
            numbers = [int(s) for s in line.strip().split()]
            range_map.add(*numbers)
        maps.append(range_map)

    # part 1
    outputs = []
    for seed in initial_seeds:
        for range_map in maps:
            seed = range_map.get_dest(seed)
        outputs.append(seed)
    print(min(outputs))

    # part 2
    seed_ranges = []
    min_output = math.inf
    for i in range(0, len(initial_seeds), 2):
        start = initial_seeds[i]
        length = initial_seeds[i+1]
        seed_ranges.append(Range(start, start + length))

    for seed_range in seed_ranges:
        current_ranges = [seed_range]
        for range_map in maps:
            next_ranges = []
            for r in current_ranges:
                next_ranges.extend(range_map.get_dest_ranges(r))
            current_ranges = next_ranges

        min_output = min(min_output, min(r.start for r in current_ranges))
    print(min_output)


if __name__ == '__main__':
    main()
