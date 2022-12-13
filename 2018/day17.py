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
            ''.join(self.grid.get(Point(x, y), '.') for x in range(self.min_x, self.max_x + 1))
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
    print(len(grid))
    print(min_x, min_y, max_x, max_y)

    # for y in range(min_y, max_y + 1):
    #     line_out = []
    #     for x in range(min_x, max_x + 1):
    #         if y == min_y and x == 500:
    #             line_out.append('+')
    #         else:
    #             line_out.append(grid.get(Point(x, y), '.'))
    #     print(''.join(line_out))

    print('area', (max_x - min_x) * (max_y - min_y))
    starting_point = Point(x=500, y=0)
    grid[starting_point] = '+'
    state = State(grid, min_x, max_x, min_y, max_y)
    iterate(state, [starting_point])


def iterate(state: State, current_flow_points: list[Point]):
    while current_flow_points:
        current = current_flow_points.pop()
        print(state, '\n', current, '\n\n')
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
            # we should be on top of clay or standing water
            assert tile_below in {'#', '~'}

            lx = next_point.x - 1
            rx = next_point.x + 1
            blocked_left = False
            blocked_right = False
            for lx in range(next_point.x - 1, state.min_x - 2, -1):
                if state.grid.get(Point(lx, next_point.y)) != '#' or Point(lx, next_point.y - 1) in state.grid:
                    break
            if state.grid.get(Point(lx, next_point.y - 1)) == '#':
                blocked_left = True

            for rx in range(next_point.x + 1, state.max_x + 1):
                if state.grid.get(Point(rx, next_point.y)) != '#' or Point(rx, next_point.y - 1) in state.grid:
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
                    current_flow_points.append(Point(lx, next_point.y - 1))
                if not blocked_right:
                    current_flow_points.append(Point(rx, next_point.y - 1))


if __name__ == '__main__':
    main()
