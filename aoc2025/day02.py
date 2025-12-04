import math
import sys
from pathlib import Path
from typing import NamedTuple, Iterator


class Range(NamedTuple):
    start_str: str
    end_str: str

    def invalid_ids(self, n_parts: int, start: int, end: int) -> Iterator[int]:
        n_digits = int(math.log10(start)) + 1
        if n_digits % n_parts != 0:
            return
        shift = int(10 ** (n_digits / n_parts))
        part_start = start // int(shift ** (n_parts - 1))
        part_end = end // int(shift ** (n_parts - 1))
        for part in range(part_start, part_end + 1):
            whole = sum(part * int(shift ** i) for i in range(n_parts))
            if start <= whole <= end:
                yield whole

    def duplicated_numbers1(self) -> Iterator[int]:
        start_len = len(self.start_str)
        end_len = len(self.end_str)
        if start_len == end_len:
            if start_len % 2 == 1:
                return
            start = int(self.start_str)
            end = int(self.end_str)
        else:
            assert end_len == start_len + 1
            if start_len % 2 == 1:
                end = int(self.end_str)
                start = int(10 ** (end_len - 1))
            else:
                start = int(self.start_str)
                end = int(10 ** start_len - 1)

        yield from self.invalid_ids(2, start, end)

    def duplicated_numbers2(self) -> Iterator[int]:
        start_len = len(self.start_str)
        end_len = len(self.end_str)
        if start_len == end_len:
            start = int(self.start_str)
            end = int(self.end_str)
            for n_parts in range(2, start_len + 1):
                yield from self.invalid_ids(n_parts, start, end)
        else:
            assert end_len == start_len + 1
            start1 = int(self.start_str)
            end1 = int(10 ** start_len - 1)
            for n_parts in range(2, start_len + 1):
                yield from self.invalid_ids(n_parts, start1, end1)

            start2 = int(10 ** (end_len - 1))
            end2 = int(self.end_str)
            for n_parts in range(2, end_len + 1):
                yield from self.invalid_ids(n_parts, start2, end2)


def main():
    text = Path(sys.argv[1]).read_text().strip()
    ranges: list[Range] = []
    for r in text.split(","):
        start, end = r.split("-", 1)
        ranges.append(Range(start, end))

    print(sum(n for r in ranges for n in r.duplicated_numbers1()))
    print(sum({n for r in ranges for n in r.duplicated_numbers2()}))


if __name__ == "__main__":
    main()
