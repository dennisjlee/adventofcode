from __future__ import annotations

import sys
from typing import NamedTuple, cast


Columns = tuple[int, int, int, int, int]


class Lock(NamedTuple):
    columns: Columns

    @staticmethod
    def parse(grid: list[str]) -> Lock:
        heights = tuple(
            next(y for y in range(6) if grid[y + 1][x] == ".") for x in range(5)
        )
        return Lock(cast(Columns, heights))


class Key(NamedTuple):
    columns: Columns

    @staticmethod
    def parse(grid: list[str]) -> Key:
        heights = tuple(
            next((5 - y) for y in range(5, -1, -1) if grid[y][x] == ".")
            for x in range(5)
        )
        return Key(cast(Columns, heights))

    def fits(self, lock: Lock) -> bool:
        return all((c1 + c2) <= 5 for c1, c2 in zip(self.columns, lock.columns))


def main():
    with open(sys.argv[1]) as f:
        blocks = f.read().strip().split("\n\n")

    locks: list[Lock] = []
    keys: list[Key] = []
    for block in blocks:
        grid = block.strip().split("\n")
        if block[0] == "#":
            locks.append(Lock.parse(grid))
        else:
            keys.append(Key.parse(grid))

    print(sum(1 for lock in locks for key in keys if key.fits(lock)))


if __name__ == "__main__":
    main()
