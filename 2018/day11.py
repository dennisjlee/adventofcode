from __future__ import annotations

import math
from collections import namedtuple
from typing import Optional


def main():
    serial_number = 9445
    grid: list[list[int]] = [[0] * 300 for _ in range(300)]
    for y in range(1, 301):
        for x in range(1, 301):
            grid[y - 1][x - 1] = compute_power_level(x, y, serial_number)

    part1(grid)

    # too slow by far!
    # part2_direct(grid)

    # still kinda slow
    part2_dynamic(grid)


def part1(grid: list[list[int]]):
    subtotals: list[list[Optional[int]]] = [[None] * 298 for _ in range(298)]
    max_sum = -math.inf
    best_coord = None
    for y in range(298):
        for x in range(298):
            subtotals[y][x] = sum(grid[y + dy][x + dx]
                                  for dy in range(3)
                                  for dx in range(3))
            if subtotals[y][x] > max_sum:
                max_sum = subtotals[y][x]
                best_coord = (x, y)

    print(f'{best_coord[0] + 1},{best_coord[1] + 1}')


Segment = namedtuple('Segment', ['start_x', 'start_y', 'end_x', 'end_y'])
Square = namedtuple('Square', ['start_x', 'start_y', 'size'])


def part2_direct(grid: list[list[int]]):
    best_total = -math.inf
    best_square = None

    for size in range(1, 301):
        print('Checking size', size)
        for y in range(301 - size):
            for x in range(301 - size):
                subtotal = sum(grid[y + dy][x + dx]
                               for dy in range(size)
                               for dx in range(size))
                if subtotal > best_total:
                    best_total = subtotal
                    best_square = Square(x, y, size)

    print(f'{best_square.start_x + 1},{best_square.start_y + 1},{best_square.size}')


def part2_dynamic(grid: list[list[int]]):
    segment_totals: dict[Segment, int] = {}

    # row segments
    print('Computing row segments')
    for y in range(300):
        running_total = 0
        for x in range(300):
            running_total += grid[y][x]
            segment_totals[Segment(0, y, x, y)] = running_total

    # column segments
    print('Computing column segments')
    for x in range(300):
        running_total = 0
        for y in range(300):
            running_total += grid[y][x]
            segment_totals[Segment(x, 0, x, y)] = running_total

    best_total = -math.inf
    best_square = None
    subtotals: list[list[Optional[int]]] = [
        [None] * 300
        for _ in range(300)
    ]
    for y in range(300):
        for x in range(300):
            subtotal = grid[y][x]
            subtotals[y][x] = subtotal
            if subtotal > best_total:
                best_total = subtotal
                best_square = Square(x, y, 1)

    for size in range(2, 301):
        print('Computing subtotals for size', size)
        n = 301 - size
        next_subtotals: list[list[Optional[int]]] = [
            [None] * n
            for _ in range(n)
        ]
        for y in range(n):
            for x in range(n):
                end_x = x + size - 1
                end_y = y + size - 1
                if x == 0 and y == 0:
                    smaller_square_total = subtotals[0][0]
                    last_column_total = segment_totals[Segment(end_x, 0, end_x, end_y)]
                    last_row_total = segment_totals[Segment(0, end_y, end_x, end_y)]
                    subtotal = (
                            smaller_square_total +
                            last_row_total +
                            last_column_total -
                            grid[end_y][end_x]
                    )
                elif x == 0:
                    square_above_total = next_subtotals[y - 1][0]
                    prev_top_row_total = segment_totals[Segment(0, y - 1, end_x, y - 1)]
                    bottom_row_total = segment_totals[Segment(0, end_y, end_x, end_y)]
                    subtotal = square_above_total - prev_top_row_total + bottom_row_total
                elif y == 0:
                    square_left_total = next_subtotals[0][x - 1]
                    prev_left_col_total = segment_totals[Segment(x - 1, 0, x - 1, end_y)]
                    right_col_total = segment_totals[Segment(end_x, 0, end_x, end_y)]
                    subtotal = square_left_total - prev_left_col_total + right_col_total
                else:
                    square_left_total = next_subtotals[y][x - 1]
                    prev_left_col_total = segment_totals[Segment(x - 1, 0, x - 1, end_y)] - \
                                          segment_totals[Segment(x - 1, 0, x - 1, y - 1)]
                    right_col_total = segment_totals[Segment(end_x, 0, end_x, end_y)] - \
                                      segment_totals[Segment(end_x, 0, end_x, y - 1)]
                    subtotal = square_left_total - prev_left_col_total + right_col_total

                next_subtotals[y][x] = subtotal
                if subtotal > best_total:
                    best_total = subtotal
                    best_square = Square(x, y, size)

        subtotals = next_subtotals

    print(f'{best_square.start_x + 1},{best_square.start_y + 1},{best_square.size}')


def compute_power_level(x: int, y: int, serial_number: int):
    rack_id = x + 10
    power_level = rack_id * y + serial_number
    power_level *= rack_id
    power_level = power_level // 100 % 10
    return power_level - 5


if __name__ == '__main__':
    main()
