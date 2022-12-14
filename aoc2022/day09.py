from __future__ import annotations
import sys
from typing import NamedTuple


class Move(NamedTuple):
    direction: str
    magnitude: int


class Point(NamedTuple):
    x: int
    y: int


class KnotPosition:
    pos: Point
    previous_positions: set[Point]

    def __init__(self):
        self.pos = Point(0, 0)
        self.previous_positions = {self.pos}

    def __repr__(self):
        return repr(self.pos)

    def move(self, new_pos: Point):
        self.pos = new_pos
        self.previous_positions.add(new_pos)

    def move_direction(self, direction: str):
        if direction == 'U':
            new_pos = Point(self.pos.x, self.pos.y - 1)
        elif direction == 'D':
            new_pos = Point(self.pos.x, self.pos.y + 1)
        elif direction == 'L':
            new_pos = Point(self.pos.x - 1, self.pos.y)
        elif direction == 'R':
            new_pos = Point(self.pos.x + 1, self.pos.y)
        self.move(new_pos)

    def chase(self, other: KnotPosition):
        ps = self.pos
        po = other.pos
        if ps.x == po.x and abs(ps.y - po.y) == 2:
            dy = (po.y - ps.y) // 2
            self.move(Point(ps.x, ps.y + dy))
        elif ps.y == po.y and abs(ps.x - po.x) == 2:
            dx = (po.x - ps.x) // 2
            self.move(Point(ps.x + dx, ps.y))
        elif ps.x != po.x and ps.y != po.y and \
                ((abs(ps.x - po.x) + abs(ps.y - po.y)) > 2):
            dx = 1 if po.x > ps.x else -1
            dy = 1 if po.y > ps.y else -1
            self.move(Point(ps.x + dx, ps.y + dy))
        elif abs(ps.x - po.x) + abs(ps.y - po.y) > 2:
            raise Exception('Too far!')


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    moves = []
    for line in lines:
        d, m = line.split()
        moves.append(Move(d, int(m)))

    head = KnotPosition()
    tail = KnotPosition()
    for move in moves:
        for i in range(move.magnitude):
            head.move_direction(move.direction)
            tail.chase(head)

    print(len(tail.previous_positions))

    knots = [KnotPosition() for _ in range(10)]
    for m, move in enumerate(moves):
        for i in range(move.magnitude):
            knots[0].move_direction(move.direction)
            for k in range(1, 10):
                knots[k].chase(knots[k-1])

    print(len(knots[-1].previous_positions))


if __name__ == '__main__':
    main()
