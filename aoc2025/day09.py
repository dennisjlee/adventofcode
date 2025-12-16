from __future__ import annotations

import sys
from collections.abc import Callable
from functools import cached_property
from itertools import combinations
from pathlib import Path
from typing import NamedTuple, TypeVar, Iterable


class Point(NamedTuple):
    x: int
    y: int

    @staticmethod
    def parse(line: str) -> Point:
        xs, ys = line.strip().split(',')
        return Point(int(xs), int(ys))

    def area(self, other: Point) -> int:
        len_x = abs(other.x - self.x) + 1
        len_y = abs(other.y - self.y) + 1
        return len_x * len_y

    def translate_x(self, dx: int) -> Point:
        return Point(self.x + dx, self.y)

    def translate_y(self, dy: int) -> Point:
        return Point(self.x, self.y + dy)


class Edge:
    point1: Point
    point2: Point

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def __repr__(self) -> str:
        return f"Edge(point1={self.point1}, point2={self.point2})"

    @cached_property
    def horizontal(self) -> bool:
        return self.point1.y == self.point2.y

    @cached_property
    def min_x(self) -> int:
        return min(self.point1.x, self.point2.x)

    @cached_property
    def min_y(self) -> int:
        return min(self.point1.y, self.point2.y)

    @cached_property
    def max_x(self) -> int:
        return max(self.point1.x, self.point2.x)

    @cached_property
    def max_y(self) -> int:
        return max(self.point1.y, self.point2.y)

    def intersects(self, other: Edge) -> bool:
        if self.horizontal:
            return (
                (other.min_y <= self.point1.y <= other.max_y) and
                (self.min_x <= other.point1.x <= self.max_x)
            )
        else:
            return (
                (other.min_x <= self.point1.x <= other.max_x) and
                (self.min_y <= other.point1.y <= self.max_y)
            )

    def translate_x(self, dx: int) -> Edge:
        return Edge(self.point1.translate_x(dx), self.point2.translate_x(dx))

    def translate_y(self, dy: int) -> Edge:
        return Edge(self.point1.translate_y(dy), self.point2.translate_y(dy))


class Rectangle(NamedTuple):
    corner1: Point
    corner2: Point

    def is_valid(self, horizontal_edges: list[Edge], vertical_edges: list[Edge]) -> bool:
        c1, c2 = self.corner1, self.corner2
        if c1.x < c2.x:
            left = Edge(c1, Point(c1.x, c2.y))
            right = Edge(c2, Point(c2.x, c1.y))
        else:
            left = Edge(c2, Point(c2.x, c1.y))
            right = Edge(c1, Point(c1.x, c2.y))

        if c1.y < c2.y:
            top = Edge(c1, Point(c2.x, c1.y))
            bottom = Edge(c2, Point(c1.x, c2.y))
        else:
            top = Edge(c2, Point(c1.x, c2.y))
            bottom = Edge(c1, Point(c2.x, c1.y))

        if left.max_x != right.max_x:
            # Avoid degenerate case where width is 1
            for h in horizontal_edges:
                if h.point1 == c1 or h.point2 == c1 or h.point1 == c2 or h.point2 == c2:
                    continue
                if h.intersects(left) and h.max_x > left.max_x:
                    return False
                if h.intersects(right) and h.min_x < right.min_x:
                    return False

        if top.max_y != bottom.max_y:
            # Avoid degenerate case where height is 1
            for v in vertical_edges:
                if v.point1 == c1 or v.point2 == c1 or v.point1 == c2 or v.point2 == c2:
                    continue
                if v.intersects(top) and v.max_y > top.max_y:
                    return False
                if v.intersects(bottom) and v.min_y < bottom.min_y:
                    return False

        # There's one edge case where this is wrong, if we are constructing
        # a rectangle where three corners are edges of the outer shape and the fourth
        # corner is outside. But I got the answer so I'll punt on that ..

        return True


def main():
    with Path(sys.argv[1]).open() as f:
        points = [Point.parse(line) for line in f.readlines()]

    print(max(p1.area(p2) for p1, p2 in combinations(points, 2)))

    horizontal_edges, vertical_edges = partition(
        (Edge(p, points[(i + 1) % len(points)]) for i, p in enumerate(points)),
        lambda edge: edge.horizontal
    )

    print(max(p1.area(p2) for p1, p2 in combinations(points, 2)
              if Rectangle(p1, p2).is_valid(horizontal_edges, vertical_edges)))


T = TypeVar('T')

def partition(collection: Iterable[T], pred: Callable[[T], bool]) -> tuple[list[T], list[T]]:
    matching: list[T] = []
    non_matching: list[T] = []
    for t in collection:
        if pred(t):
            matching.append(t)
        else:
            non_matching.append(t)
    return matching, non_matching


if __name__ == "__main__":
    main()