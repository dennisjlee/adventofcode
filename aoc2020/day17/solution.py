import sys
from typing import List


def main():
    with open(sys.argv[1]) as f:
        original_state = [[list(l.strip()) for l in f]]

    # part 1
    state = original_state
    for i in range(6):
        new_state = iterate_state_3d(state)
        state = new_state
    print(count_active_3d(state))

    # part 2
    state4 = [original_state]
    for i in range(6):
        new_state4 = iterate_state_4d(state4)
        state4 = new_state4
    print(count_active_4d(state4))


def count_active_3d(state):
    return sum(sum(sum(1 for char in row if char == '#')
                   for row in plane)
               for plane in state)


def iterate_state_3d(state: List[List[List[str]]]) -> List[List[List[str]]]:
    old_width = len(state[0][0])
    old_height = len(state[0])
    old_depth = len(state)
    width = old_width + 2
    height = old_height + 2
    depth = old_depth + 2
    new_state = [
        [
            ['.'] * width for y in range(height)
        ] for z in range(depth)
    ]

    for z in range(depth):
        for y in range(height):
            for x in range(width):
                if 0 <= z-1 < old_depth and \
                        0 <= y-1 < old_height and \
                        0 <= x-1 < old_width:
                    cur = state[z-1][y-1][x-1]
                else:
                    cur = '.'

                if cur == '.':
                    new_state[z][y][x] = '#' if should_become_active_3d(state, x - 1, y - 1, z - 1) else '.'
                elif cur == '#':
                    new_state[z][y][x] = '.' if should_become_inactive_3d(state, x - 1, y - 1, z - 1) else '#'
    return new_state


def should_become_active_3d(state, x, y, z):
    active_neighbors = 0
    for nz in range(max(0, z-1), min(z+2, len(state))):
        for ny in range(max(0, y-1), min(y+2, len(state[0]))):
            for nx in range(max(0, x-1), min(x+2, len(state[0][0]))):
                if nz == z and ny == y and nx == x:
                    continue
                if state[nz][ny][nx] == '#':
                    active_neighbors += 1
                    if active_neighbors > 3:
                        return False

    return active_neighbors == 3


def should_become_inactive_3d(state, x, y, z):
    active_neighbors = 0
    for nz in range(max(0, z-1), min(z+2, len(state))):
        for ny in range(max(0, y-1), min(y+2, len(state[0]))):
            for nx in range(max(0, x-1), min(x+2, len(state[0][0]))):
                if nz == z and ny == y and nx == x:
                    continue
                if state[nz][ny][nx] == '#':
                    active_neighbors += 1
                    if active_neighbors > 3:
                        return True

    return active_neighbors < 2


def iterate_state_4d(state: List[List[List[List[str]]]]) -> List[List[List[List[str]]]]:
    old_width = len(state[0][0][0])
    old_height = len(state[0][0])
    old_depth = len(state[0])
    old_hyperdepth = len(state)
    width = old_width + 2
    height = old_height + 2
    depth = old_depth + 2
    hyperdepth = old_hyperdepth + 2
    new_state = [
        [
            [
                ['.'] * width for y in range(height)
            ] for z in range(depth)
        ] for w in range(hyperdepth)
    ]

    for w in range(hyperdepth):
        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    if 0 <= w-1 < old_hyperdepth and \
                            0 <= z-1 < old_depth and \
                            0 <= y-1 < old_height and \
                            0 <= x-1 < old_width:
                        cur = state[w-1][z-1][y-1][x-1]
                    else:
                        cur = '.'

                    if cur == '.':
                        new_state[w][z][y][x] = '#' if should_become_active_4d(state, x-1, y-1, z-1, w-1) else '.'
                    elif cur == '#':
                        new_state[w][z][y][x] = '.' if should_become_inactive_4d(state, x-1, y-1, z-1, w-1) else '#'
    return new_state


def should_become_active_4d(state, x, y, z, w):
    active_neighbors = 0
    for nw in range(max(0, w-1), min(w+2, len(state))):
        for nz in range(max(0, z-1), min(z+2, len(state[0]))):
            for ny in range(max(0, y-1), min(y+2, len(state[0][0]))):
                for nx in range(max(0, x-1), min(x+2, len(state[0][0][0]))):
                    if nw == w and nz == z and ny == y and nx == x:
                        continue
                    if state[nw][nz][ny][nx] == '#':
                        active_neighbors += 1
                        if active_neighbors > 3:
                            return False

    return active_neighbors == 3


def should_become_inactive_4d(state, x, y, z, w):
    active_neighbors = 0
    for nw in range(max(0, w-1), min(w+2, len(state))):
        for nz in range(max(0, z-1), min(z+2, len(state[0]))):
            for ny in range(max(0, y-1), min(y+2, len(state[0][0]))):
                for nx in range(max(0, x-1), min(x+2, len(state[0][0][0]))):
                    if nw == w and nz == z and ny == y and nx == x:
                        continue
                    if state[nw][nz][ny][nx] == '#':
                        active_neighbors += 1
                        if active_neighbors > 3:
                            return True

    return active_neighbors < 2


def count_active_4d(state):
    return sum(sum(sum(sum(1 for char in row if char == '#')
                       for row in plane)
                   for plane in space)
               for space in state)


if __name__ == '__main__':
    main()

