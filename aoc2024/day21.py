from __future__ import annotations

import functools
import itertools
import sys
from typing import NamedTuple, Iterator, Sequence


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
    def press_button_sequences(from_char: str, to_char: str) -> Sequence[str]:
        """Return every possible optimal sequence of moves that would push the given
        button"""
        curr = NumberPad.char_to_point(from_char)
        new_point = NumberPad.char_to_point(to_char)

        x_move = move_x(new_point, curr)
        y_move = move_y(new_point, curr)
        if new_point.y == curr.y:
            return [x_move + "A"]
        elif new_point.x == curr.x:
            return [y_move + "A"]
        elif curr.y == 3 and new_point.x == 0:
            # move up first to avoid moving left into the blank space
            return [y_move + x_move + "A"]
        elif new_point.y == 3 and curr.x == 0:
            # move right first to avoid moving down into the blank space
            return [x_move + y_move + "A"]
        else:
            # move either horizontally or vertically first (try both ways)
            return [x_move + y_move + "A", y_move + x_move + "A"]

    @staticmethod
    def generate_all_sequences(buttons: str) -> Iterator[str]:
        steps: list[Sequence[str]] = []
        from_char = "A"
        for to_char in buttons:
            steps.append(NumberPad.press_button_sequences(from_char, to_char))
            from_char = to_char
        for product in itertools.product(*steps):
            yield "".join(product)


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
    def press_button_sequences(from_char: str, to_char: str) -> Sequence[str]:
        """Return every possible optimal sequence of moves that would push the given
        button"""
        curr = DirectionalPad.char_to_point(from_char)
        new_point = DirectionalPad.char_to_point(to_char)

        x_move = move_x(new_point, curr)
        y_move = move_y(new_point, curr)
        if new_point.y == curr.y:
            return [x_move + "A"]
        elif new_point.x == curr.x:
            return [y_move + "A"]
        elif curr.y == 0 and new_point.x == 0:
            # move down first to avoid moving left into the blank space
            return [y_move + x_move + "A"]
        elif new_point.y == 0 and curr.x == 0:
            # move right first to avoid moving up into the blank space
            return [x_move + y_move + "A"]
        else:
            # move either horizontally or vertically first (try both ways)
            return [x_move + y_move + "A", y_move + x_move + "A"]

    @staticmethod
    def generate_all_sequences(buttons: str) -> Iterator[str]:
        steps: list[Sequence[str]] = []
        from_char = "A"
        for to_char in buttons:
            steps.append(DirectionalPad.press_button_sequences(from_char, to_char))
            from_char = to_char
        for product in itertools.product(*steps):
            yield "".join(product)


def main():
    with open(sys.argv[1]) as f:
        codes = [l.strip() for l in f.readlines()]

    result1 = 0
    for code in codes:
        numeric_code = int(code[:-1])

        moves = min(
            len(sequence2)
            for sequence0 in NumberPad.generate_all_sequences(code)
            for sequence1 in DirectionalPad.generate_all_sequences(sequence0)
            for sequence2 in DirectionalPad.generate_all_sequences(sequence1)
        )

        result1 += moves * numeric_code

    print(result1)

    result2 = 0
    for code in codes:
        numeric_code = int(code[:-1])

        sequences = NumberPad.generate_all_sequences(code)
        for i in range(25):
            all_next_sequences: set[str] = set(
                itertools.chain.from_iterable(
                    [
                        DirectionalPad.generate_all_sequences(sequence)
                        for sequence in sequences
                    ]
                )
            )
            min_length = min(len(next_seq) for next_seq in all_next_sequences)
            sequences = {
                next_seq
                for next_seq in all_next_sequences
                if len(next_seq) == min_length
            }
            print(
                f"At step {i}, {len(all_next_sequences)} next sequences, {len(sequences)} sequences"
            )
            print("\n".join(list(sequences)[:10]))
        moves = len(sequences.pop())

        result2 += moves * numeric_code

    print(result2)


if __name__ == "__main__":
    main()
