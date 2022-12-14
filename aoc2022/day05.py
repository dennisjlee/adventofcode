from __future__ import annotations
import re
import sys
from collections import namedtuple, deque
from copy import deepcopy


class Move(namedtuple('Move', ['num', 'src', 'dest'])):
    pass


MOVE_REGEX = re.compile(r'move (\d+) from (\d+) to (\d+)')


def main():
    with open(sys.argv[1]) as f:
        crates_raw, moves_raw = f.read().strip().split('\n\n')

    stacks = {}
    for line_num, crate_line in enumerate(reversed(crates_raw.split('\n'))):
        if line_num == 0:
            for n in range(1, 10):
                stacks[n] = deque()
        else:
            for n in range(1, 10):
                i = 4 * (n - 1) + 1
                if crate_line[i] != ' ':
                    stacks[n].append(crate_line[i])

    moves: list[Move] = []
    for move_line in moves_raw.split('\n'):
        match = MOVE_REGEX.match(move_line)
        moves.append(Move(int(match.group(1)), int(match.group(2)), int(match.group(3))))

    stacks_new = deepcopy(stacks)

    for m in moves:
        src = stacks[m.src]
        dest = stacks[m.dest]
        for c in range(m.num):
            dest.append(src.pop())

    print(''.join(stacks[n][-1] for n in range(1, 10)))

    for m in moves:
        src = stacks_new[m.src]
        dest = stacks_new[m.dest]
        temp = deque()
        for c in range(m.num):
            temp.appendleft(src.pop())
        dest.extend(temp)

    print(''.join(stacks_new[n][-1] for n in range(1, 10)))


if __name__ == '__main__':
    main()
