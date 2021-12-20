from __future__ import annotations

import itertools
import math
import sys
from collections import deque
from functools import reduce
from typing import *

import numpy as np

SIN = {
    0: 0,
    90: 1,
    180: 0,
    270: -1
}

COS = {
    0: 1,
    90: 0,
    180: -1,
    270: 0
}


class Point3(NamedTuple):
    coords: tuple[int, int, int]

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def z(self):
        return self.coords[2]

    def reorient(self, axis_order: tuple[int, int, int], axis_signs: tuple[int, int, int]):
        new_coords = tuple(self.coords[order] * sign for order, sign in zip(axis_order, axis_signs))
        assert len(new_coords) == 3
        return Point3(new_coords)

    def __repr__(self):
        return f'({self.x},{self.y},{self.z})'

    def __sub__(self, other: Point3):
        return Point3((self.x - other.x, self.y - other.y, self.z - other.z))


class Scanner:
    id: int
    detected: list[np.array]
    internal_differences: dict[tuple[int, int, int], tuple[np.array, np.array]]
    origin: np.array

    def __init__(self, scanner_id: int, detected: list[np.array], origin=None):
        self.id = scanner_id
        self.detected = detected
        self.internal_differences = {}
        for a, b in itertools.combinations(self.detected, 2):
            if tuple(a) < tuple(b):
                self.internal_differences[tuple(b - a)] = (b, a)
            else:
                self.internal_differences[tuple(a - b)] = (a, b)
        self.origin = np.array([0, 0, 0]) if origin is None else origin

    def rotate(self, rotation_matrix: np.array):
        return Scanner(self.id, [rotation_matrix @ p for p in self.detected], self.origin)

    def translate(self, translation: np.array):
        return Scanner(self.id, [p + translation for p in self.detected], translation)


def main():
    scanners: deque[Scanner] = deque()
    with open(sys.argv[1]) as f:
        scanner_blocks = f.read().strip().split('\n\n')
        for block in scanner_blocks:
            block_lines = block.split('\n')
            scanner_id = int(block_lines[0].split()[2])
            points = [
                np.array([int(s) for s in line.strip().split(',', 2)])
                for line in block_lines[1:]
            ]
            scanners.append(Scanner(scanner_id, points))

    # Thank you Wikipedia..
    unique_rotations = set()
    rotation_matrices = []
    x_rotations = [
        np.array([[1, 0, 0],
                  [0, COS[theta], -SIN[theta]],
                  [0, SIN[theta], COS[theta]]])
        for theta in SIN.keys()
    ]
    y_rotations = [
        np.array([[COS[theta], 0, SIN[theta]],
                  [0, 1, 0],
                  [-SIN[theta], 0, COS[theta]]])
        for theta in SIN.keys()
    ]
    z_rotations = [
        np.array([[COS[theta], -SIN[theta], 0],
                  [SIN[theta], COS[theta], 0],
                  [0, 0, 1]])
        for theta in SIN.keys()
    ]
    for xr in x_rotations:
        for yr in y_rotations:
            for zr in z_rotations:
                r = zr @ yr @ xr
                r_tuple = tupleize(r)
                if r_tuple not in unique_rotations:
                    unique_rotations.add(r_tuple)
                    rotation_matrices.append(r)

    aligned_scanners = [scanners.popleft()]
    aligned_queue = deque(aligned_scanners)
    while scanners:
        aligned = aligned_queue.popleft()
        # print('aligning against scanner', aligned.id)
        next_scanners = deque()
        for scanner in scanners:
            max_overlap_diffs = -1
            best_rotation = None
            best_overlap = None
            realigned_scanner = None
            for rotation_matrix in rotation_matrices:
                turned = scanner.rotate(rotation_matrix)
                overlapping_differences = aligned.internal_differences.keys() & turned.internal_differences.keys()
                if len(overlapping_differences) > max_overlap_diffs:
                    max_overlap_diffs = len(overlapping_differences)
                    best_rotation = rotation_matrix
                    best_overlap = overlapping_differences
                    if max_overlap_diffs >= 66:  # 12 choose 2
                        realigned_scanner = turned
                        break
            if max_overlap_diffs >= 66:
                # print(f'{aligned.id} vs {scanner.id} (rotation: {tupleize(best_rotation)}): {max_overlap_diffs} overlaps')
                diff = next(iter(best_overlap))
                a1, a2 = aligned.internal_differences[diff]
                b1, b2 = realigned_scanner.internal_differences[diff]

                translation = a1 - b1
                assert (translation == (a2 - b2)).all()
                # print(f'{aligned.id} vs {scanner.id} - translation {translation}')

                final_aligned_scanner = scanner.rotate(best_rotation).translate(translation)
                aligned_scanners.append(final_aligned_scanner)
                aligned_queue.append(final_aligned_scanner)
            else:
                next_scanners.append(scanner)
        scanners = next_scanners

    all_points = {
        tuple(p)
        for a in aligned_scanners
        for p in a.detected
    }
    # part 1
    print(len(all_points))

    # part 2
    print(max(manhattan_distance(a.origin, b.origin) for a, b in itertools.combinations(aligned_scanners, 2)))


def manhattan_distance(a: np.array, b: np.array) -> int:
    return np.abs(b - a).sum()


def tupleize(arr: np.array) -> tuple[tuple]:
    return tuple(tuple(row) for row in arr)


if __name__ == '__main__':
    main()
