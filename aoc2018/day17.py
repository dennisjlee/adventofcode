import re
import sys
from typing import NamedTuple, Optional
from copy import copy


class Point(NamedTuple):
    x: int
    y: int


class State(NamedTuple):
    grid: dict[Point, str]
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def __repr__(self):
        return '\n'.join(
            ''.join(self.grid.get(Point(x, y), '.') for x in range(self.min_x - 5, self.max_x + 6))
            for y in range(self.max_y + 1)
        )

"""
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
"""
PARSER = re.compile(r'([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)')

def main():
    grid: dict[Point, str] = {}
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            match = PARSER.match(line)
            dim1 = match.group(1)
            dim1_value = int(match.group(2))
            dim2 = match.group(3)
            dim2_start = int(match.group(4))
            dim2_end = int(match.group(5))
            kwargs = {dim1: dim1_value}
            for dim2_value in range(dim2_start, dim2_end + 1):
                kwargs[dim2] = dim2_value
                grid[Point(**kwargs)] = '#'

    min_y = min(p.y for p in grid.keys())
    max_y = max(p.y for p in grid.keys())
    min_x = min(p.x for p in grid.keys())
    max_x = max(p.x for p in grid.keys())

    starting_point = Point(x=500, y=0)
    grid[starting_point] = '+'
    state = State(grid, min_x, max_x, min_y, max_y)
    iterate(state, [starting_point], verbose=False)

    print(sum(1 for p, v in state.grid.items() if min_y <= p.y <= max_y and v in WATER_TILES))
    print(sum(1 for p, v in state.grid.items() if min_y <= p.y <= max_y and v == '~'))


WATER_TILES = {'|', '~'}

FLOWABLE_TILES = {'|', None}

FIXED_TILES = {'#', '~'}


def iterate(state: State, current_flow_points: list[Point], verbose=True):
    step = 0
    previous_flow_points = set()
    while current_flow_points:
        step += 1
        current = current_flow_points.pop()
        if state.grid.get(current) == '~':
            continue
        if current in previous_flow_points:
            zzz = 1
        else:
            previous_flow_points.add(current)

        if step % 1000 == 0:
            print('step', step, '# of flow points', len(current_flow_points))
            if verbose:
                print(state, '\n', current, '\n\n')
                zzz = 1
        for next_y in range(current.y + 1, state.max_y + 1):
            next_point = Point(current.x, next_y)
            if next_point in state.grid:
                break
            else:
                state.grid[next_point] = '|'
        else:
            # we ran off the bottom without breaking
            next_point = None

        if next_point:
            tile_below = state.grid.get(next_point)
            if tile_below not in FIXED_TILES:
                continue  # flowing onto already flowing water - this will be handled by another flow point

            # we should be on top of clay or standing water
            lx = next_point.x - 1
            rx = next_point.x + 1
            blocked_left = False
            blocked_right = False
            for lx in range(next_point.x - 1, state.min_x - 5, -1):
                if state.grid.get(Point(lx, next_point.y)) not in FIXED_TILES or \
                        state.grid.get(Point(lx, next_point.y - 1)) not in FLOWABLE_TILES:
                    break
            if state.grid.get(Point(lx, next_point.y - 1)) == '#':
                blocked_left = True

            for rx in range(next_point.x + 1, state.max_x + 5):
                if state.grid.get(Point(rx, next_point.y)) not in FIXED_TILES or \
                        state.grid.get(Point(rx, next_point.y - 1)) not in FLOWABLE_TILES:
                    break
            if state.grid.get(Point(rx, next_point.y - 1)) == '#':
                blocked_right = True

            if blocked_left and blocked_right:
                for x in range(lx + 1, rx):
                    state.grid[Point(x, next_point.y - 1)] = '~'
                current_flow_points.append(Point(next_point.x, next_point.y - 2))
            else:
                for x in range(lx + 1, rx):
                    state.grid[Point(x, next_point.y - 1)] = '|'
                if not blocked_left:
                    left_overflow = Point(lx, next_point.y - 1)
                    state.grid[left_overflow] = '|'
                    current_flow_points.append(left_overflow)
                if not blocked_right:
                    right_overflow = Point(rx, next_point.y - 1)
                    state.grid[right_overflow] = '|'
                    current_flow_points.append(right_overflow)
    if verbose:
        print(state)


if __name__ == '__main__':
    main()
