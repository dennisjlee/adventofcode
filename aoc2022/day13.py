from __future__ import annotations

import sys
from functools import total_ordering
from itertools import zip_longest
from typing import NamedTuple


@total_ordering
class Packet(NamedTuple):
    data: list|int

    def __lt__(self, other: Packet):
        return cmp(self.data, other.data) < 0

    def __eq__(self, other: Packet):
        return cmp(self.data, other.data) == 0


def cmp(v1: list|int, v2: list|int) -> int:
    if isinstance(v1, int) and isinstance(v2, int):
        return v1 - v2
    elif isinstance(v1, list) and isinstance(v2, list):
        for s1, s2 in zip_longest(v1, v2):
            if s1 is None:
                return -1
            elif s2 is None:
                return 1
            if c := cmp(s1, s2):
                return c
        return 0
    else:
        if isinstance(v1, int):
            return cmp([v1], v2)
        else:
            return cmp(v1, [v2])


def main():
    with open(sys.argv[1]) as f:
        raw_pairs = f.read().split('\n\n')

    pairs = []
    for raw_pair in raw_pairs:
        raw_packet1, raw_packet2 = raw_pair.strip().split('\n')
        packet1 = Packet(eval(raw_packet1))
        packet2 = Packet(eval(raw_packet2))
        pairs.append((packet1, packet2))

    print(sum(find_right_order_pairs(pairs)))

    divider1 = Packet([[2]])
    divider2 = Packet([[6]])
    all_packets = [divider1, divider2]
    for pair in pairs:
        all_packets.extend(pair)
    all_packets.sort()
    print((all_packets.index(divider1) + 1) * (all_packets.index(divider2) + 1))


def find_right_order_pairs(pairs):
    for i, pair in enumerate(pairs):
        packet1, packet2 = pair
        if packet1 < packet2:
            yield i + 1


if __name__ == '__main__':
    main()
