from __future__ import annotations
import re
import sys
from enum import Enum
from collections import Counter
from functools import total_ordering
from typing import NamedTuple
import math


CARD_VALUES = {
    char: i
    for i, char in enumerate('23456789TJQKA')
}

WILDCARD_VALUES = {
    char: i
    for i, char in enumerate('J23456789TQKA')
}


@total_ordering
class Type(Enum):
    FIVE = 7
    FOUR = 6
    FULL = 5
    THREE = 4
    TWO_PAIR = 3
    PAIR = 2
    HIGH = 1

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def grade_hand(counts: Counter):
    card_counts = sorted(counts.values())
    if card_counts == [5]:
        return Type.FIVE
    elif card_counts == [1, 4]:
        return Type.FOUR
    elif card_counts == [2, 3]:
        return Type.FULL
    elif card_counts == [1, 1, 3]:
        return Type.THREE
    elif card_counts == [1, 2, 2]:
        return Type.TWO_PAIR
    elif card_counts == [1, 1, 1, 2]:
        return Type.PAIR
    else:
        return Type.HIGH


@total_ordering
class Hand:
    cards: str
    bid: int
    type: Type
    card_values: tuple

    def __init__(self, line: str):
        cards, bid_str = line.strip().split()
        self.cards = cards
        self.bid = int(bid_str)
        self.type = self.get_type(cards)
        self.card_values = tuple(CARD_VALUES[c] for c in cards)

    @staticmethod
    def get_type(cards: str) -> Type:
        return grade_hand(Counter(cards))

    def __lt__(self, other: Hand):
        if self.type == other.type:
            return self.card_values < other.card_values
        else:
            return self.type < other.type

    def __repr__(self):
        return f'Hand(cards={self.cards}, bid={self.bid}, type={self.type})'


@total_ordering
class WildcardHand:
    cards: str
    bid: int
    type: Type
    card_values: tuple

    def __init__(self, line: str):
        cards, bid_str = line.strip().split()
        self.cards = cards
        self.bid = int(bid_str)
        self.type = self.get_type(cards)
        self.card_values = tuple(WILDCARD_VALUES[c] for c in cards)

    @staticmethod
    def get_type(cards: str) -> Type:
        counts = Counter(cards)
        if 'J' in counts:
            jack_count = counts['J']
            if jack_count < 5:
                del counts['J']
                [(most_common, count)] = counts.most_common(1)
                counts[most_common] += jack_count

        return grade_hand(counts)

    def __lt__(self, other: WildcardHand):
        if self.type == other.type:
            return self.card_values < other.card_values
        else:
            return self.type < other.type

    def __repr__(self):
        return f'WildcardHand(cards={self.cards}, bid={self.bid}, type={self.type})'


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    # part 1
    hands = [Hand(line) for line in lines]
    sorted_hands = sorted(hands)
    print(sum(
        (i + 1) * hand.bid
        for i, hand in enumerate(sorted_hands)
    ))

    # part 2
    wildcard_hands = [WildcardHand(line) for line in lines]
    sorted_wildcard_hands = sorted(wildcard_hands)
    print(sum(
        (i + 1) * hand.bid
        for i, hand in enumerate(sorted_wildcard_hands)
    ))


if __name__ == '__main__':
    main()
