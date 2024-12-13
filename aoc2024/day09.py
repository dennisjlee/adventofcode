import itertools
import sys
from collections import defaultdict
from typing import NamedTuple


def main():
    with open(sys.argv[1]) as f:
        disk_map_raw = f.read().strip()
    disk_map = [int(c) for c in disk_map_raw]

    part1(disk_map)
    part2(disk_map)


def part1(disk_map: list[int]):
    disk: list[int | None] = []
    used_indices: list[int] = []
    unused_indices: list[int] = []
    disk_index = 0
    for i, n in enumerate(disk_map):
        if i % 2 == 0:
            id_number = i // 2
            disk.extend([id_number] * n)
            used_indices.extend(range(disk_index, disk_index + n))
            disk_index += n
        else:
            disk.extend([None] * n)
            unused_indices.extend(range(disk_index, disk_index + n))
            disk_index += n

    for unused_i, used_i in zip(unused_indices, reversed(used_indices)):
        if used_i <= unused_i:
            break
        disk[unused_i] = disk[used_i]
        disk[used_i] = None

    checksum = 0
    for i, n in enumerate(disk):
        if n is None:
            break
        checksum += i * n
    print(checksum)


class File(NamedTuple):
    value: int
    start: int
    size: int


class Gap(NamedTuple):
    start: int
    size: int


def part2(disk_map: list[int]):
    files: list[File] = []
    gaps: list[Gap] = []
    disk_index = 0
    for i, n in enumerate(disk_map):
        if i % 2 == 0:
            id_number = i // 2
            files.append(File(id_number, disk_index, n))
            disk_index += n
        else:
            gaps.append(Gap(disk_index, n))
            disk_index += n

    for i in range(len(files) - 1, -1, -1):
        file = files[i]
        for j, gap in enumerate(gaps):
            if gap.start >= file.start:
                break
            if gap.size >= file.size:
                gaps[j] = Gap(gap.start + file.size, gap.size - file.size)
                files[i] = File(file.value, gap.start, file.size)
                break

    checksum = 0
    for f in files:
        for i in range(f.start, f.start + f.size):
            checksum += i * f.value
    print(checksum)


if __name__ == "__main__":
    main()
