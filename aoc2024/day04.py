from collections import Counter
import re
import sys
import re
from typing import Generator

XMAS = re.compile('XMAS')
XMAS_REV = re.compile('SAMX')


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    xmas_count = 0

    w = len(lines[0])
    h = len(lines)

    for line in lines:
        xmas_count += get_xmas_count(line)

    for x in range(w):
        column = ''.join(line[x] for line in lines)
        xmas_count += get_xmas_count(column)

    for x0 in range(w):
        diagonal_southeast = ''.join(get_diagonal(x0, 0, 1, 1, lines, w, h))
        xmas_count += get_xmas_count(diagonal_southeast)

        diagonal_southwest = ''.join(get_diagonal(x0, 0, -1, 1, lines, w, h))
        xmas_count += get_xmas_count(diagonal_southwest)

    for y0 in range(1, h):
        diagonal_southeast = ''.join(get_diagonal(0, y0, 1, 1, lines, w, h))
        xmas_count += get_xmas_count(diagonal_southeast)

        diagonal_southwest = ''.join(get_diagonal(w - 1, y0, -1, 1, lines, w, h))
        xmas_count += get_xmas_count(diagonal_southwest)

    print(xmas_count)

    # part 2, "x-mas"
    cross_count = 0
    target_diag = {'M', 'S'}
    for y in range(1, h - 1):
        line = lines[y]
        x = 0
        while 0 < (x := line.find('A', x + 1)) < w - 1:
            diag1 = {lines[y-1][x-1], lines[y+1][x+1]}
            if diag1 == target_diag:
                diag2 = {lines[y-1][x+1], lines[y+1][x-1]}
                if diag2 == target_diag:
                    cross_count += 1

    print(cross_count)


def get_xmas_count(s: str):
    return len(XMAS.findall(s)) + len(XMAS_REV.findall(s))


def get_diagonal(x0: int, y0: int, dx: int, dy: int, lines: list[str], w: int, h: int) -> Generator[str]:
    x = x0
    y = y0
    while 0 <= x < w and 0 <= y < h:
        yield lines[y][x]
        x += dx
        y += dy


if __name__ == '__main__':
    main()
