from collections import Counter
import re
import sys

HEIGHT = 0
WIDTH = 0

def main():
    with open(sys.argv[1]) as f:
        waiting_room = [list(l.strip()) for l in f]

    global HEIGHT
    global WIDTH

    original_room = waiting_room
    HEIGHT = len(waiting_room)
    WIDTH = len(waiting_room[0])

    # part 1
    while True:
        new_room = iterate_room1(waiting_room)
        if waiting_room == new_room:
            print(count_occupied(waiting_room))
            break
        waiting_room = new_room

    # part 2
    waiting_room = original_room
    while True:
        new_room = iterate_room2(waiting_room)
        if waiting_room == new_room:
            print(count_occupied(waiting_room))
            break
        waiting_room = new_room

def count_occupied(room):
    return sum(sum(1 for char in row if char == '#') for row in room)

def print_room(room):
    print('\n'.join(''.join(row) for row in room))
    print()

def iterate_room1(waiting_room):
    new_room = [
        ['.'] * len(waiting_room[0]) 
        for r in range(len(waiting_room))
    ]
    for r in range(HEIGHT):
        for c in range(WIDTH):
            cur = waiting_room[r][c]
            if cur == 'L':
                new_room[r][c] = '#' if should_become_occupied1(waiting_room, r, c) else 'L'
            elif cur == '#':
                new_room[r][c] = 'L' if should_become_empty1(waiting_room, r, c) else '#'
    return new_room

def should_become_occupied1(waiting_room, r, c):
    for ny in range(max(0, r-1), min(r+2, HEIGHT)):
        for nx in range(max(0, c-1), min(c+2, WIDTH)):
            if ny == r and nx == c:
                continue
            if waiting_room[ny][nx] == '#':
                return False
    return True

def should_become_empty1(waiting_room, r, c):
    neighbors_occupied = 0
    for ny in range(max(0, r-1), min(r+2, HEIGHT)):
        for nx in range(max(0, c-1), min(c+2, WIDTH)):
            if ny == r and nx == c:
                continue
            if waiting_room[ny][nx] == '#':
                neighbors_occupied += 1
            if neighbors_occupied >= 4:
                return True
    return False

def iterate_room2(waiting_room):
    new_room = [
        ['.'] * len(waiting_room[0]) 
        for r in range(len(waiting_room))
    ]
    for r in range(HEIGHT):
        for c in range(WIDTH):
            cur = waiting_room[r][c]
            if cur == 'L':
                new_room[r][c] = '#' if should_become_occupied2(waiting_room, r, c) else 'L'
            elif cur == '#':
                new_room[r][c] = 'L' if should_become_empty2(waiting_room, r, c) else '#'
    return new_room

def sees_occupied_seat(waiting_room, r, c, dy, dx):
    ny = r
    nx = c
    while True:
        ny += dy
        nx += dx
        if 0 <= ny < HEIGHT and 0 <= nx < WIDTH:
            cur = waiting_room[ny][nx]
            if cur == 'L':
                return False
            elif cur == '#':
                return True
        else:
            # out of bounds
            return False

DIRECTIONS = [
  (-1, -1),
  (-1, 0),
  (-1, 1),
  (0, -1),
  (0, 1),
  (1, -1),
  (1, 0),
  (1, 1)
]


def should_become_occupied2(waiting_room, r, c):
    for dy, dx in DIRECTIONS:
        if sees_occupied_seat(waiting_room, r, c, dy, dx):
            return False
    return True

def should_become_empty2(waiting_room, r, c):
    visible_occupied = 0
    for dy, dx in DIRECTIONS:
        if sees_occupied_seat(waiting_room, r, c, dy, dx):
            visible_occupied += 1
        if visible_occupied >= 5:
            return True
    return False



if __name__ == '__main__':
    main()
