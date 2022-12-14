from __future__ import annotations
import sys
from typing import NamedTuple, Literal


FORWARD_DIRECTIONS = [
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]


class Point(NamedTuple):
    x: int
    y: int


OPEN = '.'
TREES = '|'
LUMBER = '#'

AcreContents = Literal['.', '|', '#']

Grid = list[list[AcreContents]]


class Acre:
    contents_now: AcreContents
    contents_next: AcreContents
    neighbors: list[Acre]

    def __init__(self, contents: AcreContents):
        self.contents_now = contents
        self.contents_next = contents
        self.neighbors = []

    def is_changed(self):
        return self.contents_now == self.contents_next


def get_or_add_acre(grid: Grid, acre_map: dict[Point, Acre], x: int, y: int) -> Acre:
    point = Point(x, y)
    acre = acre_map.get(point)
    if not acre:
        acre = Acre(grid[y][x])
        acre_map[point] = acre
    return acre


def build_graph(grid: Grid):
    height = len(grid)
    width = len(grid[0])

    acre_map: dict[Point, Acre] = {}

    for y in range(height):
        for x in range(width):
            acre = get_or_add_acre(grid, acre_map, x, y)
            # Only look in half the directions, and trust that seats we iterated
            # over earlier would have established neighbor relationships in the
            # "backwards" directions by the time we get to any given seat
            for dy, dx in FORWARD_DIRECTIONS:
                ny = y + dy
                nx = x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    neighbor_acre = get_or_add_acre(grid, acre_map, nx, ny)
                    acre.neighbors.append(neighbor_acre)
                    neighbor_acre.neighbors.append(acre)

    return acre_map


def main():
    with open(sys.argv[1]) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    print(simulate(grid, 10))
    print(simulate(grid, 1_000_000_000))


def simulate(grid: Grid, steps: int) -> int:
    acre_map = build_graph(grid)

    for i in range(steps):
        if i % 1000 == 0:
            print('step', i)
        if not iterate(acre_map):
            print(f'no more changes after step {i}!')
            break
    wood_count = sum(1 for acre in acre_map.values() if acre.contents_now == TREES)
    lumberyard_count = sum(1 for acre in acre_map.values() if acre.contents_now == LUMBER)
    return wood_count * lumberyard_count


def iterate(acre_map: dict[Point, Acre]) -> bool:
    any_change = False
    for acre in acre_map.values():
        if acre.contents_now == OPEN:
            acre.contents_next = OPEN
            count = 0
            for neighbor in acre.neighbors:
                if neighbor.contents_now == TREES:
                    count += 1
                    if count >= 3:
                        any_change = True
                        acre.contents_next = TREES
                        break
        elif acre.contents_now == TREES:
            acre.contents_next = TREES
            count = 0
            for neighbor in acre.neighbors:
                if neighbor.contents_now == LUMBER:
                    count += 1
                    if count >= 3:
                        any_change = True
                        acre.contents_next = LUMBER
                        break
        else:
            acre.contents_next = OPEN
            found_lumber = False
            found_trees = False
            for neighbor in acre.neighbors:
                if neighbor.contents_now == LUMBER:
                    found_lumber = True
                if neighbor.contents_now == TREES:
                    found_trees = True
                if found_lumber and found_trees:
                    any_change = True
                    acre.contents_next = LUMBER

    for acre in acre_map.values():
        acre.contents_now = acre.contents_next

    return any_change


if __name__ == '__main__':
    main()
