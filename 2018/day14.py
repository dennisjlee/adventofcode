from __future__ import annotations

import collections.abc
import math
from abc import abstractmethod
from collections import deque
from typing import Sequence, overload, Iterable, MutableSequence

INPUT = '157901'

MAX_SIZE = 10_000_000


def main():
    # print(part1(INPUT))
    print(part2(INPUT))
    # print(part2_numeric(INPUT))
    # print(part2_list(INPUT))
    # print(part2_deque(INPUT))
    # print(part2_paged(INPUT))


def part1(target: str):
    state = [3, 7]
    i = 0
    j = 1
    count = int(target)
    while len(state) < count + 10:
        score1 = state[i]
        score2 = state[j]
        next_num = score1 + score2
        if next_num >= 10:
            state.append(1)
        state.append(next_num % 10)
        i = (i + 1 + score1) % len(state)
        j = (j + 1 + score2) % len(state)

    return int(''.join(str(d) for d in state[count:count + 10]))


def array_has_suffix(arr: Sequence[int], suffix: Sequence[int]):
    suffix_len = len(suffix)
    if len(arr) < suffix_len:
        return False
    return all(arr[-suffix_len + i] == suffix[i] for i in range(suffix_len))


def array_has_suffix2(arr: Sequence[int], arr_len: int, suffix: Sequence[int], suffix_len: int):
    if arr_len < suffix_len:
        return False
    for i in range(suffix_len):
        if arr[-suffix_len + i] != suffix[i]:
            return False
    return True


def part2_list(target: str):
    state = [3, 7]
    i = 0
    j = 1
    target_array = [int(c) for c in target]
    target_len = len(target_array)
    size = len(state)
    while not array_has_suffix2(state, size, target_array, target_len) and size < MAX_SIZE:
        score1 = state[i]
        score2 = state[j]
        next_num = score1 + score2
        if next_num >= 10:
            size += 1
            state.append(1)
        state.append(next_num % 10)
        size += 1
        i = (i + 1 + score1) % size
        j = (j + 1 + score2) % size

    return len(state) - target_len


def part2(target: str):
    state = bytearray([3, 7])
    i = 0
    j = 1
    target_array = bytearray([int(c) for c in target])
    target_len = len(target_array)
    size = len(state)
    while not state.endswith(target_array) and size < MAX_SIZE:
        score1 = state[i]
        score2 = state[j]
        next_num = score1 + score2
        if next_num >= 10:
            size += 1
            state.append(1)
        state.append(next_num % 10)
        size += 1
        i = (i + 1 + score1) % size
        j = (j + 1 + score2) % size

    return len(state) - target_len


def part2_numeric(target: str):
    state = 37
    i = 0
    j = 1
    size = 2
    target_num = int(target)
    suffix_mask = 10 ** len(target)
    while (state % suffix_mask != target_num) and size < MAX_SIZE:
        i_factor = 10 ** (size - i - 1)
        j_factor = 10 ** (size - j - 1)
        score1 = (state // i_factor) % 10
        score2 = (state // j_factor) % 10
        next_num = score1 + score2
        if next_num >= 10:
            size += 2
            state = state * 100 + next_num
        else:
            size += 1
            state = state * 10 + next_num

        i = (i + 1 + score1) % size
        j = (j + 1 + score2) % size

    print('bits:', state.bit_length())
    return int(math.ceil(math.log10(state))) - len(target)


def part2_deque(target: str):
    state = bytearray([3, 7])
    i = 0
    j = 1
    target_array = deque(int(c) for c in target)
    target_len = len(target_array)
    last_n = deque(state, target_len)
    size = len(state)

    while last_n != target_array and size < MAX_SIZE:
        score1 = state[i]
        score2 = state[j]
        next_num = score1 + score2
        if next_num >= 10:
            size += 1
            last_n.append(1)
            state.append(1)
        new_digit = next_num % 10
        last_n.append(new_digit)
        state.append(new_digit)
        size += 1
        i = (i + 1 + score1) % size
        j = (j + 1 + score2) % size

    return len(state) - target_len


def part2_paged(target: str):
    state = PagedByteArray([3, 7])
    i = 0
    j = 1
    target_array = [int(c) for c in target]
    target_len = len(target_array)
    size = len(state)
    while not array_has_suffix2(state, size, target_array, target_len) and size < MAX_SIZE:
        score1 = state[i]
        score2 = state[j]
        next_num = score1 + score2
        if next_num >= 10:
            size += 1
            state.append(1)
        state.append(next_num % 10)
        size += 1
        i = (i + 1 + score1) % size
        j = (j + 1 + score2) % size

    return len(state) - target_len


class PagedByteArray(collections.abc.MutableSequence):
    _PAGE_SIZE = 2 ** 20
    # _PAGE_SIZE = 5

    __slots__ = ["_pages", "_size", "_page_count"]

    def __init__(self, seq: Sequence[int]):
        self._pages = []
        self._page_count = 0
        first_page = self._add_page()
        for i, v in enumerate(seq):
            first_page[i] = v
        self._size = len(seq)

    def _add_page(self):
        page = bytearray(self._PAGE_SIZE)
        self._pages.append(page)
        self._page_count += 1
        return page

    def insert(self, index: int, value: int) -> None:
        for _ in range((index // self._PAGE_SIZE) + 1 - self._page_count):
            self._add_page()
        page = self._pages[index // self._PAGE_SIZE]
        page[index % self._PAGE_SIZE] = value
        self._size = max(self._size, index + 1)

    @overload
    @abstractmethod
    def __getitem__(self, i: int) -> int:
        return self.__getitem__(i)

    @overload
    @abstractmethod
    def __getitem__(self, s: slice) -> MutableSequence[int]: ...

    def __getitem__(self, i: int) -> int:
        page = self._pages[i // self._PAGE_SIZE]
        return page[i % self._PAGE_SIZE]

    @overload
    @abstractmethod
    def __setitem__(self, i: int, o: int) -> None:
        self.__setitem__(i, o)

    @overload
    @abstractmethod
    def __setitem__(self, s: slice, o: Iterable[int]) -> None: ...

    def __setitem__(self, i: int, o: int) -> None:
        page = self._pages[i // self._PAGE_SIZE]
        page[i % self._PAGE_SIZE] = o

    @overload
    @abstractmethod
    def __delitem__(self, i: int) -> None: ...

    @overload
    @abstractmethod
    def __delitem__(self, i: slice) -> None: ...

    def __delitem__(self, i: int) -> None:
        pass

    def __len__(self) -> int:
        return self._size


if __name__ == '__main__':
    main()
