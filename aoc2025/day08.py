from __future__ import annotations

import sys
import heapq
from math import prod, sqrt
from pathlib import Path
from typing import cast, Literal, NamedTuple


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


    heap1: list[tuple[float, Point3D, Point3D]] = []
    heap2: list[tuple[float, Point3D, Point3D]] = []
    for i, p1 in enumerate(points):
        for p2 in points[i+1:]:
            distance = p1.euclidean_distance(p2)
            heap_item1 = (-distance, p1, p2)
            if len(heap1) < 1000:
                heapq.heappush(heap1, heap_item1)
            else:
                heapq.heappushpop(heap1, heap_item1)
            heap_item2 = (distance, p1, p2)
            heapq.heappush(heap2, heap_item2)

    assert len(heap1) == 1000
    clusters1 = {p: frozenset([p]) for p in points}
    for _distance, p1, p2 in heap1:
        set1 = clusters1[p1]
        set2 = clusters1[p2]
        if set1 is set2:
            continue

        merged = set1 | set2
        for p in merged:
            clusters1[p] = merged

    sorted_clusters = sorted(set(clusters1.values()), key=len, reverse=True)
    print(prod(len(sorted_clusters[i]) for i in range(3)))

    assert len(heap2) == len(points) * (len(points) - 1) // 2
    clusters2 = {p: frozenset([p]) for p in points}
    while len(heap2):
        _distance, p1, p2 = heapq.heappop(heap2)
        set1 = clusters2[p1]
        set2 = clusters2[p2]
        if set1 is set2:
            continue

        merged = set1 | set2
        for p in merged:
            clusters2[p] = merged

        if len(merged) == len(points):
            print(p1.x * p2.x)
            break


if __name__ == "__main__":
    main()