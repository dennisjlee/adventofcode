from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def neighbors(self, height: int, width: int) -> Iterable[Position]:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                new_y = self.y + dy
                new_x = self.x + dx
                if 0 <= new_x < width and 0 <= new_y < height and not (
                        new_x == self.x and new_y == self.y):
                    yield Position(new_x, new_y)


def main():
    grid = Path(sys.argv[1]).read_text().split("\n")
    neighbor_count: dict[Position, int] = defaultdict(int)
    paper_positions: set[Position] = set()
    height = len(grid)
    width = len(grid[0])
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "@":
                pos = Position(x, y)
                paper_positions.add(pos)
                for n in pos.neighbors(height, width):
                    neighbor_count[n] += 1

    print(sum(1 for p in paper_positions if neighbor_count[p] < 4))

    removed = 0
    while removable := {p for p in paper_positions if neighbor_count[p] < 4}:
        paper_positions -= removable
        removed += len(removable)
        for pos in removable:
            for n in pos.neighbors(height, width):
                neighbor_count[n] -= 1

    print(removed)

if __name__ == "__main__":
    main()