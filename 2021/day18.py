from __future__ import annotations

import itertools
import math
import sys
from functools import reduce
from typing import *


class SnailfishNumber:
    left: Union[int, SnailfishNumber]
    right: Union[int, SnailfishNumber]
    parent: SnailfishNumber
    depth: int

    def __init__(self, lst: list, depth: int = 0):
        assert len(lst) == 2
        self.depth = depth
        if isinstance(lst[0], int):
            self.left = lst[0]
        else:
            self.left = SnailfishNumber(lst[0], depth + 1)

        if isinstance(lst[1], int):
            self.right = lst[1]
        else:
            self.right = SnailfishNumber(lst[1], depth + 1)

    def __str__(self):
        return f'[{self.left},{self.right}]'

    def try_explode(self):
        if isinstance(self.left, int) and isinstance(self.right, int):
            if self.depth == 4:
                return True, self.left, self.right
            return False, None, None

        if isinstance(self.left, SnailfishNumber):
            exploded, send_left, send_right = self.left.try_explode()
            if exploded:
                if send_left is not None and send_right is not None:
                    # our immediate child exploded
                    self.left = 0

                if send_right is not None:
                    if isinstance(self.right, int):
                        self.right += send_right
                    else:
                        self.right.add_leftmost(send_right)

                return True, send_left, None

        if isinstance(self.right, SnailfishNumber):
            exploded, send_left, send_right = self.right.try_explode()
            if exploded:
                if send_left is not None and send_right is not None:
                    # our immediate child exploded
                    self.right = 0

                if send_left is not None:
                    if isinstance(self.left, int):
                        self.left += send_left
                    else:
                        self.left.add_rightmost(send_left)

                return True, None, send_right

        return False, None, None

    def add_leftmost(self, to_add):
        if isinstance(self.left, int):
            self.left += to_add
        else:
            self.left.add_leftmost(to_add)

    def add_rightmost(self, to_add):
        if isinstance(self.right, int):
            self.right += to_add
        else:
            self.right.add_rightmost(to_add)

    def try_split(self):
        if isinstance(self.left, int):
            if self.left >= 10:
                n = self.left
                self.left = SnailfishNumber([n // 2, int(math.ceil(n / 2))], self.depth + 1)
                return True
        elif self.left.try_split():
            return True

        if isinstance(self.right, int):
            if self.right >= 10:
                n = self.right
                self.right = SnailfishNumber([n // 2, int(math.ceil(n / 2))], self.depth + 1)
                return True
        elif self.right.try_split():
            return True

        return False

    def reduce(self):
        assert self.depth == 0

        while True:
            exploded, _, _ = self.try_explode()
            if exploded:
                continue
            split = self.try_split()
            if split:
                continue
            break

    def with_increased_depth(self):
        new_number = SnailfishNumber([0, 0], self.depth + 1)
        if isinstance(self.left, SnailfishNumber):
            new_number.left = self.left.with_increased_depth()
        else:
            new_number.left = self.left

        if isinstance(self.right, SnailfishNumber):
            new_number.right = self.right.with_increased_depth()
        else:
            new_number.right = self.right
        return new_number

    def magnitude(self):
        left_magnitude = 3 * (self.left if isinstance(self.left, int) else self.left.magnitude())
        right_magnitude = 2 * (self.right if isinstance(self.right, int) else self.right.magnitude())
        return left_magnitude + right_magnitude

    @staticmethod
    def parse(string):
        lst = eval(string)  # lazy, but quite effective
        return SnailfishNumber(lst, depth=0)

    @staticmethod
    def add(first: SnailfishNumber, second: SnailfishNumber) -> SnailfishNumber:
        result = SnailfishNumber([0, 0])
        result.left = first.with_increased_depth()
        result.right = second.with_increased_depth()
        result.reduce()
        return result


def main():
    with open(sys.argv[1]) as f:
        numbers = [SnailfishNumber.parse(line.strip()) for line in f.readlines()]

    final_sum = reduce(SnailfishNumber.add, numbers)
    print(final_sum.magnitude())

    best_magnitude = -math.inf
    for n1, n2 in itertools.combinations(numbers, 2):
        best_magnitude = max(best_magnitude, SnailfishNumber.add(n1, n2).magnitude(), SnailfishNumber.add(n2, n1).magnitude())

    print(best_magnitude)


def test_explode(lst):
    n = SnailfishNumber(lst)
    print(n)
    print('explodes to')
    n.try_explode()
    print(n)


if __name__ == '__main__':
    main()
