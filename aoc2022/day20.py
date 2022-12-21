from __future__ import annotations

import sys
from collections import defaultdict
from itertools import cycle
from typing import NamedTuple, Iterable, Optional


class LinkedList:
    val: int
    next: Optional[LinkedList]
    prev: Optional[LinkedList]

    def __init__(self, val: int):
        self.val = val
        self.next = None
        self.prev = None

    def __repr__(self):
        return f'LinkedList(val={self.val}, prev={self.prev.val if self.prev else None}, next={self.next.val if self.next else None})'

    def walk(self, steps: int, forward: bool):
        curr = self
        if forward:
            for _ in range(steps):
                curr = curr.next
        else:
            for _ in range(steps):
                curr = curr.prev
        return curr

    def to_list(self):
        values = [self.val]
        curr = self.next
        while curr != self:
            values.append(curr.val)
            curr = curr.next
        return values


def parse():
    with open(sys.argv[1]) as f:
        items = [
            LinkedList(int(line.strip()))
            for line in f.readlines()
        ]

    n = len(items)
    for i in range(n):
        j = (i + 1) % n
        items[i].next = items[j]
        items[j].prev = items[i]
    return items

def main():
    items = parse()
    part1(items)

    items2 = parse()
    part2(items2)


def part1(items: list[LinkedList]):
    zero = next(item for item in items if item.val == 0)
    mix(items)
    print(get_coordinate_sum(zero))


def get_coordinate_sum(zero: LinkedList):
    coord1 = zero.walk(1000, True)
    coord2 = coord1.walk(1000, True)
    coord3 = coord2.walk(1000, True)
    return coord1.val + coord2.val + coord3.val


def part2(items: list[LinkedList]):
    decryption_key = 811589153
    for item in items:
        item.val *= decryption_key
    zero = next(item for item in items if item.val == 0)
    for _ in range(10):
        mix(items)
    print(get_coordinate_sum(zero))


def mix(items):
    n = len(items)
    for item in items:
        if item.val == 0:
            continue
        target = item.walk(abs(item.val) % (n - 1), forward=item.val > 0)

        # snip out item
        item.next.prev = item.prev
        item.prev.next = item.next

        if item.val > 0:
            # insert item after target
            new_next = target.next
            item.next = new_next
            new_next.prev = item
            item.prev = target
            target.next = item
        else:
            # insert item before target
            new_prev = target.prev
            item.prev = new_prev
            new_prev.next = item
            item.next = target
            target.prev = item


if __name__ == '__main__':
    main()
