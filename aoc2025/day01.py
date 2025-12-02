from pathlib import Path
import sys
from typing import NamedTuple, Literal


class Move(NamedTuple):
    direction: Literal["L", "R"]
    size: int


def main():

    moves: list[Move] = []
    with Path(sys.argv[1]).open() as f:
        for line in f.readlines():
            line = line.strip()
            direction = line[0]
            assert direction in ("L", "R")
            size = int(line[1:])
            moves.append(Move(direction, size))

    current = 50
    zeroes_part1 = 0
    zeroes_part2 = 0
    for move in moves:
        if move.direction == "R":
            temp = current + move.size
            # Count the number of times we went past 0 going right
            zeroes_part2 += temp // 100
        else:
            temp = current - move.size
            # Count the number of times we went past 0 going left
            zeroes_part2 += (temp // -100) + (1 if current > 0 else 0)
        current = temp % 100
        if current == 0:
            zeroes_part1 += 1

    print(zeroes_part1)
    print(zeroes_part2)


if __name__ == "__main__":
    main()
