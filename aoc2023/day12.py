from __future__ import annotations

import functools
import sys
import copy
from typing import NamedTuple


class SpringRow(NamedTuple):
    pattern: str
    group_sizes: tuple[int, ...]

    @staticmethod
    def parse(line: str):
        pattern, groups = line.strip().split(' ')
        group_sizes = tuple(int(s) for s in groups.split(','))
        return SpringRow(pattern, group_sizes)

    @staticmethod
    def parse_unfolded(line: str):
        pattern, groups = line.strip().split(' ')
        group_sizes = tuple(int(s) for s in groups.split(','))
        return SpringRow('?'.join([pattern] * 5), group_sizes * 5)


@functools.cache
def count_options(pattern: str, group_sizes: tuple[int, ...]):
    if not group_sizes:
        return 0 if '#' in pattern else 1
    first_group, *rest_groups = group_sizes
    total_options = 0
    # we need to have room for the first group, and also room for the rest of the groups plus one cell between each group
    max_index = len(pattern) - first_group - sum(rest_groups) - len(rest_groups)
    for start in range(max_index + 1):
        end = start + first_group
        if pattern.find('.', start, end) == -1 and (end == len(pattern) or pattern[end] != '#'):
            total_options += count_options(pattern[end + 1:], tuple(rest_groups))
        if pattern[start] == '#':
            # We can't just walk by and ignore a '#', it has to be included in our matching option
            break
    return total_options


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    rows = [SpringRow.parse(line) for line in lines]
    print(sum(count_options(row.pattern, row.group_sizes) for row in rows))

    unfolded_rows = [SpringRow.parse_unfolded(line) for line in lines]
    print(sum(count_options(row.pattern, row.group_sizes) for row in unfolded_rows))


if __name__ == '__main__':
    main()
