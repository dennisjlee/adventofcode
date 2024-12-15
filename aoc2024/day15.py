from __future__ import annotations
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def with_move(self, m: Move):
        return Point(self.x + m.dx, self.y + m.dy)

class Move(NamedTuple):
    dx: int
    dy: int


MOVES = {
    '<': Move(-1, 0),
    '>': Move(1, 0),
    '^': Move(0, -1),
    'v': Move(0, 1),
}


def main():
    with open(sys.argv[1]) as f:
        grid_input, move_input = f.read().split('\n\n')
        grid = [list(line.strip()) for line in grid_input.strip().split('\n')]
        moves = move_input.strip().replace('\n', '')

    h = len(grid)
    w = len(grid[0])
    r = next(Point(x, y) for y in range(h) for x in range(w) if grid[y][x] == '@')
    assert r
    grid[r.y][r.x] = '.'

    for m in moves:
        move = MOVES[m]
        neighbor = r.with_move(move)
        c = grid[neighbor.y][neighbor.x]
        if c == '#':
            continue
        elif c == '.':
            r = neighbor
        elif c == 'O':
            nn = neighbor
            while (c := grid[nn.y][nn.x]) == 'O':
                nn = nn.with_move(move)
            if c == '#':
                # whole set of boxes were blocked by a wall behind
                continue
            elif c == '.':
                grid[neighbor.y][neighbor.x] = '.'
                grid[nn.y][nn.x] = 'O'
                r = neighbor

    gps_sum = 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 'O':
                gps_sum += 100 * y + x
    print(gps_sum)


if __name__ == "__main__":
    main()
