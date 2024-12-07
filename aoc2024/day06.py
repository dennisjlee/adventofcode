import sys
from collections import defaultdict

# represent points and vectors as complex numbers - real component is x, imaginary component is y
Point = complex
Vector = complex

VECTOR_UP = -1j

ROTATE_RIGHT = 1j


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    start: Point | None = None
    for y, line in enumerate(lines):
        x = line.find('^')
        if x >= 0:
            start = x + y * 1j
            break
    assert start is not None

    grid = [list(line) for line in lines]
    visited_positions = walk_grid(grid, start)
    print(len(visited_positions))

    obstacle_positions: set[Point] = set()
    for p in visited_positions:
        if p == start:
            continue
        x, y = int(p.real), int(p.imag)
        alternate_grid = [
            grid[yy]
            if yy != y
            else [c if xx != x else '#' for xx, c in enumerate(grid[y])]
            for yy in range(len(grid))
        ]
        try:
            walk_grid(alternate_grid, start)
        except LoopError:
            obstacle_positions.add(p)
    print(len(obstacle_positions))


class LoopError(Exception):
    pass


def walk_grid(grid: list[list[str]], start: Point) -> set[Point]:
    curr_p = start
    vector = VECTOR_UP
    visited_positions: dict[Point, set[Vector]] = defaultdict(set)

    w = len(grid[0])
    h = len(grid)
    while True:
        if vector in visited_positions[curr_p]:
            raise LoopError
        else:
            visited_positions[curr_p].add(vector)

        next_p = curr_p + vector
        x, y = int(next_p.real), int(next_p.imag)
        if not ((0 <= x < w) and (0 <= y < h)):
            break
        if grid[y][x] == '#':
            vector *= ROTATE_RIGHT
        else:
            curr_p = next_p

    return set(visited_positions.keys())


if __name__ == '__main__':
    main()
