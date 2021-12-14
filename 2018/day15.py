from __future__ import annotations

import sys
from collections import namedtuple, deque
from typing import Union

Point = namedtuple('Point', ['x', 'y'])
DEBUG = False


class Unit:
    next_id = 1

    def __init__(self, x: int, y: int, side: str):
        self.id = Unit.next_id
        Unit.next_id += 1
        self.position = Point(x, y)
        self.side = side
        self.attack = 3
        self.hp = 200

    @property
    def enemy_side(self):
        return 'G' if self.side == 'E' else 'E'

    def move(self, new_position: Point, grid: Grid):
        grid[self.position.y][self.position.x] = '.'
        self.position = new_position
        grid[self.position.y][self.position.x] = self

    def process_attack(self, attack: int, grid: Grid, units_by_side: dict[str, dict[int, Unit]]):
        self.hp -= attack
        if self.hp <= 0:
            grid[self.position.y][self.position.x] = '.'
            units_for_side = units_by_side[self.side]
            del units_for_side[self.id]

    def __repr__(self):
        return f'{self.side}({self.hp})'


Grid = list[list[Union[str, Unit]]]


def main():
    units_by_side: dict[str, dict[int, Unit]] = {
        'G': {},
        'E': {}
    }

    with open(sys.argv[1]) as f:
        grid: Grid = [
            list(line.strip())
            for line in f.readlines()
        ]

    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            value = grid[y][x]
            if value == 'G' or value == 'E':
                unit = Unit(x, y, value)
                units_by_side[value][unit.id] = unit
                grid[y][x] = unit

    round = 0
    while True:
        print('\nStarting round', round + 1)
        try:
            units_in_order = get_units(grid)
            for unit in units_in_order:
                process_turn(unit, grid, units_by_side)

            if DEBUG:
                for y in range(height):
                    for x in range(width):
                        value = grid[y][x]
                        if isinstance(value, Unit):
                            sys.stdout.write(value.side)
                        else:
                            sys.stdout.write(value)
                    sys.stdout.write('\n')
        except CombatFinished:
            if DEBUG:
                print('Combat finished')
            break
        round += 1

    remaining_hit_points = sum(
        sum(unit.hp for unit in units.values())
        for units in units_by_side.values())
    print(round * remaining_hit_points)


def get_units(grid):
    units = []

    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            value = grid[y][x]
            if isinstance(value, Unit):
                units.append(value)
    return units


def process_turn(unit: Unit, grid: list[list[str]], units_by_side: dict[str, dict[int, Unit]]):
    if len(units_by_side[unit.enemy_side]) == 0:
        raise CombatFinished

    if unit.hp <= 0:
        # it ded
        return

    height = len(grid)
    width = len(grid[0])

    path = find_path_to_enemy(unit, grid)
    if path:
        if len(path) > 1:
            unit.move(path[0], grid)
            path = path[1:]

        if len(path) == 1:
            # we're next to at least one enemy - also need to check for other neighboring enemies in order
            # to target the one with fewest hit points
            enemies: list[Unit] = []
            for direction in DIRECTIONS:
                pos = unit.position
                newpos = Point(pos.x + direction.x, pos.y + direction.y)
                if 0 <= newpos.x < width and 0 < newpos.y <= height:
                    neighbor = grid[newpos.y][newpos.x]
                    if isinstance(neighbor, Unit) and neighbor.side == unit.enemy_side:
                        enemies.append(neighbor)

            target = min(enemies, key=lambda u: u.hp)
            target.process_attack(unit.attack, grid, units_by_side)


DIRECTIONS = [Point(0, -1), Point(-1, 0), Point(1, 0), Point(0, 1)]


# return path to an enemy unit if possible (path excludes the unit's point and includes the enemy's point)
def find_path_to_enemy(unit, grid) -> list[Point] | None:
    queue = deque()
    visited = {unit.position}
    for direction in DIRECTIONS:
        new_point = Point(unit.position.x + direction.x, unit.position.y + direction.y)
        queue.append([new_point])

    height = len(grid)
    width = len(grid[0])

    while queue:
        path = queue.popleft()
        pos = path[-1]
        if pos.x < 0 or pos.x >= width or pos.y < 0 or pos.y >= height or pos in visited:
            continue
        visited.add(pos)

        val = grid[pos.y][pos.x]
        if isinstance(val, Unit) and val.side == unit.enemy_side:
            return path

        if val == '.':
            for direction in DIRECTIONS:
                new_point = Point(pos.x + direction.x, pos.y + direction.y)
                if new_point:
                    queue.append(path + [new_point])

    return None


class CombatFinished(Exception):
    pass


if __name__ == '__main__':
    main()
