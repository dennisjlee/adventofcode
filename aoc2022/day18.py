from __future__ import annotations

import sys
from typing import NamedTuple


class Point3D(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def parse(s: str) -> Point3D:
        xs, ys, zs = s.split(',')
        return Point3D(int(xs), int(ys), int(zs))

    def adjacent_points(self):
        yield Point3D(self.x - 1, self.y, self.z)
        yield Point3D(self.x + 1, self.y, self.z)
        yield Point3D(self.x, self.y - 1, self.z)
        yield Point3D(self.x, self.y + 1, self.z)
        yield Point3D(self.x, self.y, self.z - 1)
        yield Point3D(self.x, self.y, self.z + 1)


class BoundingBox(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int


def main():
    with open(sys.argv[1]) as f:
        points = set(Point3D.parse(line.strip()) for line in f.readlines())

    # part1
    exposed_faces = calculate_exposed_faces(points)
    print(exposed_faces)

    # part2
    bounding_box = BoundingBox(
        min(p.x for p in points),
        max(p.x for p in points),
        min(p.y for p in points),
        max(p.y for p in points),
        min(p.z for p in points),
        max(p.z for p in points)
    )

    neighbors = set()
    for p in points:
        for adjacent in p.adjacent_points():
            if adjacent not in points:
                neighbors.add(adjacent)

    all_visited = set()
    internal_faces = 0
    for n in neighbors:
        if n in all_visited:
            continue
        internal_faces += explore_empty_space(n, points, bounding_box, all_visited)
    print('exterior faces', exposed_faces - internal_faces)


def explore_empty_space(n: Point3D, shape_points: set[Point3D], bb: BoundingBox, all_visited: set[Point3D]) -> int:
    """
    Return number of exposed faces in an internal "bubble" inside a given shape.
    If the point n is exterior to the shape, then return 0.
    """
    visited = set()
    queue = [n]
    interior = True
    while queue:
        node = queue.pop()
        if node in visited:
            continue
        visited.add(node)
        for adjacent in node.adjacent_points():
            if adjacent not in shape_points:
                if (adjacent.x < bb.min_x - 1 or adjacent.x > bb.max_x + 1
                        or adjacent.y < bb.min_y - 1 or adjacent.y > bb.max_y + 1
                        or adjacent.z < bb.min_z - 1 or adjacent.z > bb.max_z + 1):
                    # we're running into empty space outside the shape, so this area
                    # is not internal
                    interior = False
                else:
                    queue.append(adjacent)
    all_visited.update(visited)
    return calculate_exposed_faces(visited) if interior else 0


def calculate_exposed_faces(points: set[Point3D]) -> int:
    exposed_sides = 0
    for p in points:
        exposed_sides += sum(1 for neighbor in p.adjacent_points() if neighbor not in points)
    return exposed_sides


if __name__ == '__main__':
    main()
