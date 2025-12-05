from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, NamedTuple


class Interval(NamedTuple):
    start: int
    end: int

    @staticmethod
    def parse(s: str) -> Interval:
        start, end = s.split("-", 2)
        return Interval(int(start), int(end))

    def __contains__(self, i: int) -> bool:
        return self.start <= i <= self.end

    def __len__(self) -> int:
        return self.end - self.start + 1

    def __or__(self, other: Interval) -> Interval:
        return Interval(min(self.start, other.start), max(self.end, other.end))

    def overlaps(self, other: Interval) -> bool:
        return self.end >= other.start and self.start <= other.end

    @staticmethod
    def merge(intervals: list[Interval]) -> list[Interval]:
        sorted_intervals = sorted(intervals)
        results: list[Interval] = []
        curr = sorted_intervals[0]
        for other in sorted_intervals[1:]:
            if curr.overlaps(other):
                curr = curr | other
            else:
                results.append(curr)
                curr = other
        results.append(curr)
        return results

def main():
    input = Path(sys.argv[1]).read_text()
    ranges_str, ingredients_str = input.strip().split("\n\n")

    intervals = [Interval.parse(r) for r in ranges_str.strip().split("\n")]
    ingredients = [int(i) for i in ingredients_str.strip().split("\n")]

    print(sum(1 for i in ingredients if any(i in r for r in intervals)))

    merged = Interval.merge(intervals)
    print(sum(len(interval) for interval in merged))


if __name__ == "__main__":
    main()