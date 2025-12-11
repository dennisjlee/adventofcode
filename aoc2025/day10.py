from __future__ import annotations

import re
import sys
from functools import reduce
import heapq
from itertools import combinations
from operator import xor
from pathlib import Path
from typing import Any, Iterable, NamedTuple

import numpy as np


MACHINE_RE = re.compile(r"\[(.+)\] (.*) \{(.+)\}")
TOGGLES_RE = re.compile(r"\(([\d,]+)\)")


def bit_mask(indices: Iterable[int]):
    mask = 0
    for index in indices:
        mask |= 1 << index
    return mask


def parse_ints(string: str) -> list[int]:
    return [int(s) for s in string.split(",")]


class SearchState(NamedTuple):
    move_count: int
    joltages: list[int]  # decrement until we get to zero
    possible_toggles: list[list[int]]

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, SearchState):
            return False
        if self.move_count != other[0]:
            return self.move_count < other[0]
        sum_self = sum(self.joltages)
        sum_other = sum(other.joltages)
        if sum_self != sum_other:
            return sum_self < sum_other
        return len(self.possible_toggles) < len(other.possible_toggles)

    def solved(self) -> bool:
        return all(j == 0 for j in self.joltages)
    
    def updated_joltages(self, toggle: list[int], count: int) -> list[int]:
        new_joltages = self.joltages.copy()
        for i in toggle:
            new_joltages[i] -= count
        return new_joltages
    
    def successors(self) -> Iterable[SearchState]:
        if len(self.possible_toggles) == 0:
            return
        first_toggle = self.possible_toggles[0]
        max_press_count = min(self.joltages[i] for i in first_toggle)

        # Special case for the last toggle - immediately press it the max number of times
        if len(self.possible_toggles) == 1:
            yield SearchState(self.move_count + max_press_count, 
                              self.updated_joltages(first_toggle, max_press_count), 
                              [])
            return

        # Skip the first toggle entirely
        yield SearchState(self.move_count, self.joltages, self.possible_toggles[1:])

        # Try every possible count of the first toggle
        for count in range(1, max_press_count + 1):
            yield SearchState(self.move_count + count, 
                              self.updated_joltages(first_toggle, count), 
                              self.possible_toggles[1:])


class Machine(NamedTuple):
    target: int  # little-endian bit-string
    toggle_masks: list[int]  # bit-masks
    toggle_indices: list[list[int]]
    joltages: list[int]

    @staticmethod
    def parse(line: str) -> Machine:
        match = MACHINE_RE.match(line)
        assert match
        target_str, toggles_str, joltages_str = match.groups()

        num_bits = len(target_str)
        target = bit_mask(i for i in range(num_bits) if target_str[i] == "#")

        toggle_indices = [
            parse_ints(toggle_match.group(1))
            for toggle_match in TOGGLES_RE.finditer(toggles_str)
        ]
        toggle_masks = [bit_mask(indices) for indices in toggle_indices]

        joltages = parse_ints(joltages_str)
        return Machine(target, toggle_masks, toggle_indices, joltages)

    def min_presses1(self) -> int:
        for toggle in self.toggle_masks:
            if toggle == self.target:
                return 1

        for n in range(2, len(self.toggle_masks) + 1):
            for combo in combinations(self.toggle_masks, n):
                if reduce(xor, combo) == self.target:
                    return n
        
        raise RuntimeError("Couldn't find a solution!")

    def min_presses2(self) -> int:
        initial = SearchState(0, self.joltages, self.toggle_indices)
        heap = [initial]
        while heap:
            state = heapq.heappop(heap)
            print(state)
            if state.solved():
                return state.move_count
            for successor in state.successors():
                heapq.heappush(heap, successor)

        raise RuntimeError("Could not solve!")

    def min_presses_joltages(self) -> int:
        target = np.array(self.joltages, dtype=np.int8)
        matrix = np.zeros((len(self.toggle_indices), len(self.joltages)), dtype=np.int8)
        for r, toggle in enumerate(self.toggle_indices):
            matrix[r, toggle] = 1


        return 0


def main():
    with Path(sys.argv[1]).open() as f:
        machines = [Machine.parse(line) for line in f.readlines()]

    print(sum(m.min_presses1() for m in machines))
    # print(sum(m.min_presses2() for m in machines))
    # print(machines[0].min_presses2())


if __name__ == "__main__":
    main()