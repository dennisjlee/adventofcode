from __future__ import annotations

import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Grid(NamedTuple):
    height: int
    width: int
    round_rocks: frozenset[Point]
    cube_rocks: frozenset[Point]

    @staticmethod
    def parse(grid_string: str) -> Grid:
        round_rocks = set()
        cube_rocks = set()
        rows = grid_string.strip().split('\n')
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == '#':
                    cube_rocks.add(Point(x, y))
                elif c == 'O':
                    round_rocks.add(Point(x, y))

        return Grid(len(rows), len(rows[0]), frozenset(round_rocks), frozenset(cube_rocks))

    def roll_north(self) -> Grid:
        new_round_rocks = set()
        for x in range(self.width):
            y_start = 0
            while y_start < self.height:
                round_count = 0
                y = y_start
                for y in range(y_start, self.height):
                    p = Point(x, y)
                    if p in self.round_rocks:
                        round_count += 1
                    elif p in self.cube_rocks:
                        break
                for yr in range(y_start, y_start + round_count):
                    new_round_rocks.add(Point(x, yr))
                y_start = y + 1

        return Grid(self.height, self.width, frozenset(new_round_rocks), self.cube_rocks)

    def roll_south(self) -> Grid:
        new_round_rocks = set()
        for x in range(self.width):
            y_start = self.height - 1
            while y_start >= 0:
                round_count = 0
                y = y_start
                for y in range(y_start, -1, -1):
                    p = Point(x, y)
                    if p in self.round_rocks:
                        round_count += 1
                    elif p in self.cube_rocks:
                        break
                for yr in range(y_start, y_start - round_count, -1):
                    new_round_rocks.add(Point(x, yr))
                y_start = y - 1

        return Grid(self.height, self.width, frozenset(new_round_rocks), self.cube_rocks)

    def roll_west(self) -> Grid:
        new_round_rocks = set()
        for y in range(self.height):
            x_start = 0
            while x_start < self.width:
                round_count = 0
                x = x_start
                for x in range(x_start, self.width):
                    p = Point(x, y)
                    if p in self.round_rocks:
                        round_count += 1
                    elif p in self.cube_rocks:
                        break
                for xr in range(x_start, x_start + round_count):
                    new_round_rocks.add(Point(xr, y))
                x_start = x + 1

        return Grid(self.height, self.width, frozenset(new_round_rocks), self.cube_rocks)

    def roll_east(self) -> Grid:
        new_round_rocks = set()
        for y in range(self.height):
            x_start = self.width - 1
            while x_start >= 0:
                round_count = 0
                x = x_start
                for x in range(x_start, -1, -1):
                    p = Point(x, y)
                    if p in self.round_rocks:
                        round_count += 1
                    elif p in self.cube_rocks:
                        break
                for xr in range(x_start, x_start - round_count, -1):
                    new_round_rocks.add(Point(xr, y))
                x_start = x - 1

        return Grid(self.height, self.width, frozenset(new_round_rocks), self.cube_rocks)

    def cycle(self) -> Grid:
        return self.roll_north().roll_west().roll_south().roll_east()

    def get_load(self) -> int:
        return sum(self.height - p.y for p in self.round_rocks)

    def __repr__(self):
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                p = Point(x, y)
                if p in self.round_rocks:
                    row.append('O')
                elif p in self.cube_rocks:
                    row.append('#')
                else:
                    row.append('.')
            rows.append(''.join(row))
        return '\n'.join(rows)


def main():
    with open(sys.argv[1]) as f:
        initial_grid = Grid.parse(f.read())

    # part 1
    print(initial_grid.roll_north().get_load())

    # part 2 - look for where the grids start to repeat, and use that cycle to predict the billionth result
    curr_grid = initial_grid
    grid_indexes = {curr_grid: 0}
    loop_start = 0
    loop_end = 0
    for i in range(1, 1000):
        curr_grid = curr_grid.cycle()
        if curr_grid in grid_indexes:
            loop_start = grid_indexes[curr_grid]
            loop_end = i
            break
        else:
            grid_indexes[curr_grid] = i

    loop_size = loop_end - loop_start
    target_index = loop_start + (1_000_000_000 - loop_start) % loop_size
    for grid, i in grid_indexes.items():
        if i == target_index:
            print(grid.get_load())


if __name__ == '__main__':
    main()
