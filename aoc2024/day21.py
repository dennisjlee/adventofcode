from __future__ import annotations

import functools
import itertools
import sys
from collections import Counter
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@functools.cache
def move_x(new_point: Point, curr: Point) -> str:
    if new_point.x != curr.x:
        move_char = ">" if new_point.x > curr.x else "<"
        return move_char * abs(new_point.x - curr.x)
    return ""


@functools.cache
def move_y(new_point: Point, curr: Point) -> str:
    if new_point.y != curr.y:
        move_char = "v" if new_point.y > curr.y else "^"
        return move_char * abs(new_point.y - curr.y)
    return ""


class NumberPad:
    """
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+
    """

    @staticmethod
    @functools.cache
    def char_to_point(char: str):
        if char == "7":
            return Point(x=0, y=0)
        elif char == "8":
            return Point(x=1, y=0)
        elif char == "9":
            return Point(x=2, y=0)
        elif char == "4":
            return Point(x=0, y=1)
        elif char == "5":
            return Point(x=1, y=1)
        elif char == "6":
            return Point(x=2, y=1)
        elif char == "1":
            return Point(x=0, y=2)
        elif char == "2":
            return Point(x=1, y=2)
        elif char == "3":
            return Point(x=2, y=2)
        elif char == "0":
            return Point(x=1, y=3)
        elif char == "A":
            return Point(x=2, y=3)

    @staticmethod
    @functools.cache
    def press_button(from_char: str, to_char: str) -> str:
        """Return optimal sequence of moves to push the given button"""
        curr = NumberPad.char_to_point(from_char)
        new_point = NumberPad.char_to_point(to_char)

        x_move = move_x(new_point, curr)
        y_move = move_y(new_point, curr)
        if new_point.y == curr.y:
            return x_move + "A"
        elif new_point.x == curr.x:
            return y_move + "A"
        elif curr.y == 3 and new_point.x == 0:
            # move up first to avoid moving left into the blank space
            return y_move + x_move + "A"
        elif new_point.y == 3 and curr.x == 0:
            # move right first to avoid moving down into the blank space
            return x_move + y_move + "A"
        elif new_point.x < curr.x:
            # move horizontally first
            return x_move + y_move + "A"
        else:
            return y_move + x_move + "A"

    @staticmethod
    def press_buttons(characters: str) -> str:
        return "".join(
            NumberPad.press_button(from_char, to_char)
            for from_char, to_char in itertools.pairwise("A" + characters)
        )


class DirectionalPad:
    """
    Directional pad
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """

    @staticmethod
    def char_to_point(char: str):
        if char == "^":
            return Point(x=1, y=0)
        elif char == "A":
            return Point(x=2, y=0)
        elif char == "<":
            return Point(x=0, y=1)
        elif char == "v":
            return Point(x=1, y=1)
        elif char == ">":
            return Point(x=2, y=1)

    @staticmethod
    @functools.cache
    def press_button(from_char: str, to_char: str) -> str:
        """Return optimal sequence of moves to push the given button"""
        curr = DirectionalPad.char_to_point(from_char)
        new_point = DirectionalPad.char_to_point(to_char)

        x_move = move_x(new_point, curr)
        y_move = move_y(new_point, curr)
        if new_point.y == curr.y:
            return x_move + "A"
        elif new_point.x == curr.x:
            return y_move + "A"
        elif curr.y == 0 and new_point.x == 0:
            # move down first to avoid moving left into the blank space
            return y_move + x_move + "A"
        elif new_point.y == 0 and curr.x == 0:
            # move right first to avoid moving up into the blank space
            return x_move + y_move + "A"
        elif new_point.x < curr.x:
            # move horizontally first - prefer `<` to `^` or `v` because it is farther
            # from the `A`
            return x_move + y_move + "A"
        else:
            # move vertically first - prefer `v` to `>` because it is farther from the
            # `A`. If we're dealing with `^` and `>` then it's a wash.
            return y_move + x_move + "A"

    @staticmethod
    def press_buttons(characters: str) -> str:
        return "".join(
            DirectionalPad.press_button(from_char, to_char)
            for from_char, to_char in itertools.pairwise("A" + characters)
        )


def main():
    with open(sys.argv[1]) as f:
        codes = [l.strip() for l in f.readlines()]

    result1 = 0
    for code in codes:
        numeric_code = int(code[:-1])

        next_code = NumberPad.press_buttons(code)
        for _ in range(2):
            next_code = DirectionalPad.press_buttons(next_code)
        result1 += len(next_code) * numeric_code

    print(result1)

    result2 = 0
    for code in codes:
        numeric_code = int(code[:-1])

        next_code = NumberPad.press_buttons(code)
        move_counter: Counter[tuple[str, str]] = Counter(
            itertools.pairwise("A" + next_code)
        )
        for i in range(25):
            next_counter: Counter[tuple[str, str]] = Counter()
            for (from_char, to_char), count in move_counter.items():
                moves = DirectionalPad.press_button(from_char, to_char)
                for from2, to2 in itertools.pairwise("A" + moves):
                    next_counter[(from2, to2)] += count
            move_counter = next_counter
        result2 += move_counter.total() * numeric_code

    print(result2)


if __name__ == "__main__":
    main()
