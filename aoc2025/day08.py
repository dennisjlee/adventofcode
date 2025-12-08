from __future__ import annotations

import sys
from math import prod, sqrt
from pathlib import Path
from typing import NamedTuple


class Point3D(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def parse(line: str) -> Point3D:
        xs, ys, zs = line.strip().split(",", 3)
        return Point3D(int(xs), int(ys), int(zs))

    def euclidean_distance(self, other: Point3D) -> float:
        return sqrt((other.x - self.x) ** 2 +
                    (other.y - self.y) ** 2 +
                    (other.z - self.z) ** 2)


def main():
    with Path(sys.argv[1]).open() as f:
        points = [Point3D.parse(line) for line in f.readlines()]

    distances: list[tuple[float, Point3D, Point3D]] = []
    for i, p1 in enumerate(points):
        for p2 in points[i+1:]:
            distance = p1.euclidean_distance(p2)
            distances.append((distance, p1, p2))
    distances.sort()

    clusters = {p: frozenset([p]) for p in points}
    for i, (_distance, p1, p2) in enumerate(distances):
        set1 = clusters[p1]
        set2 = clusters[p2]

        if set1 is not set2:
            merged = set1 | set2
            for p in merged:
                clusters[p] = merged

            if len(merged) == len(points):
                # Part 2
                print(p1.x * p2.x)
                break

        if i == 999:
            # Part 1
            sorted_clusters = sorted(set(clusters.values()), key=len, reverse=True)
            print(prod(len(sorted_clusters[i]) for i in range(3)))


if __name__ == "__main__":
    main()