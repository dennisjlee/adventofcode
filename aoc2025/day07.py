from __future__ import annotations

import sys
from collections import defaultdict
from math import prod
from pathlib import Path
from typing import cast, Literal, NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def main():
    with Path(sys.argv[1]).open() as f:
        lines = f.readlines()

    start_x = lines[0].index("S")

    splitter_x_rows: list[set[int]] = [set()]
    for y in range(1, len(lines)):
        splitter_x = set()
        line = lines[y]
        x = -1
        while True:
            try:
                x = line.index("^", x + 1)
            except ValueError:
                break
            else:
                splitter_x.add(x)
        splitter_x_rows.append(splitter_x)

    x_indices = {start_x}
    activated_splitters: set[Point] = set()
    for y in range(1, len(lines)):
        new_x_indices = set()
        for x in x_indices:
            if x not in splitter_x_rows[y]:
                new_x_indices.add(x)
            else:
                activated_splitters.add(Point(x, y))
                new_x_indices.add(x - 1)
                new_x_indices.add(x + 1)
        x_indices = new_x_indices

    print(len(activated_splitters))

    path_count = {start_x: 1}
    for y in range(1, len(lines)):
        new_path_count: dict[int, int] = defaultdict(int)
        for x, count in path_count.items():
            if x not in splitter_x_rows[y]:
                new_path_count[x] += count
            else:
                new_path_count[x - 1] += count
                new_path_count[x + 1] += count
        path_count = new_path_count

    print(sum(path_count.values()))









if __name__ == "__main__":
    main()