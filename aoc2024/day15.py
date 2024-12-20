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
    "<": Move(-1, 0),
    ">": Move(1, 0),
    "^": Move(0, -1),
    "v": Move(0, 1),
}


def part2_update_line(line: str):
    return (
        line.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
    )


def main():
    with open(sys.argv[1]) as f:
        grid_input, move_input = f.read().split("\n\n")
        grid = [list(line.strip()) for line in grid_input.strip().split("\n")]
        grid2 = [
            list(part2_update_line(line.strip()))
            for line in grid_input.strip().split("\n")
        ]
        moves = move_input.strip().replace("\n", "")

    part1(grid, moves)

    print("\n".join("".join(row) for row in grid2))
    part2(grid2, moves)
    print()
    print("\n".join("".join(row) for row in grid2))


def part1(grid: list[list[str]], moves: str):
    h = len(grid)
    w = len(grid[0])
    r = next(Point(x, y) for y in range(h) for x in range(w) if grid[y][x] == "@")
    assert r
    grid[r.y][r.x] = "."

    for m in moves:
        move = MOVES[m]
        neighbor = r.with_move(move)
        c = grid[neighbor.y][neighbor.x]
        if c == "#":
            continue
        elif c == ".":
            r = neighbor
        elif c == "O":
            nn = neighbor
            while (c := grid[nn.y][nn.x]) == "O":
                nn = nn.with_move(move)
            if c == "#":
                # whole set of boxes were blocked by a wall behind
                continue
            elif c == ".":
                grid[neighbor.y][neighbor.x] = "."
                grid[nn.y][nn.x] = "O"
                r = neighbor

    gps_sum = 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "O":
                gps_sum += 100 * y + x
    print(gps_sum)


def part2(grid2: list[list[str]], moves: str):
    h = len(grid2)
    w = len(grid2[0])
    r = next(Point(x, y) for y in range(h) for x in range(w) if grid2[y][x] == "@")
    assert r
    grid2[r.y][r.x] = "."

    for m in moves:
        move = MOVES[m]
        neighbor = r.with_move(move)
        c = grid2[neighbor.y][neighbor.x]
        if c == "#":
            continue
        elif c == ".":
            r = neighbor
        elif c in "[]":
            if move.dx:
                # horizontal move into a box
                nn = neighbor
                while (c := grid2[nn.y][nn.x]) in "[]":
                    nn = nn.with_move(move)
                if c == "#":
                    # whole row of boxes were blocked by a wall behind
                    continue
                elif c == ".":
                    grid2[neighbor.y][neighbor.x] = "."
                    for x in range(neighbor.x + move.dx, nn.x + move.dx, move.dx * 2):
                        grid2[nn.y][min(x, x + move.dx)] = "["
                        grid2[nn.y][max(x, x + move.dx)] = "]"
                    r = neighbor
            elif move.dy:
                # vertical move into a box
                pushed_box_rows: list[set[Point]] = [
                    {
                        neighbor,
                        Point(
                            x=neighbor.x + 1 if c == "[" else neighbor.x - 1,
                            y=neighbor.y,
                        ),
                    }
                ]
                while True:
                    last_row = pushed_box_rows[-1]
                    next_points = [p.with_move(move) for p in last_row]
                    next_objs = [grid2[pn.y][pn.x] for pn in next_points]
                    if "#" in next_objs:
                        # the whole arrangement of boxes is blocked
                        break
                    if all(c == "." for c in next_objs):
                        for pushed_row in reversed(pushed_box_rows):
                            for p in pushed_row:
                                pn = p.with_move(move)
                                grid2[pn.y][pn.x] = grid2[p.y][p.x]
                                grid2[p.y][p.x] = "."
                        r = neighbor
                        break
                    # we're pushing into at least one other box
                    new_row = set()
                    for nn, c in zip(next_points, next_objs):
                        if c in "[]":
                            new_row.add(nn)
                            new_row.add(
                                Point(
                                    x=nn.x + 1 if c == "[" else nn.x - 1,
                                    y=nn.y,
                                )
                            )
                    pushed_box_rows.append(new_row)

    gps_sum = 0
    for y in range(h):
        for x in range(w):
            if grid2[y][x] == "[":
                gps_sum += 100 * y + x
    print(gps_sum)


if __name__ == "__main__":
    main()
