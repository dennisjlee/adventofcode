from itertools import *
from collections import *
from typing import NamedTuple


def main():
    part1(4, 6)
    part2(4, 6)


def part1(pos1: int, pos2: int):
    score1 = 0
    score2 = 0
    dice = zip(count(1), cycle(range(1, 101)))
    dice_count = 0

    while score1 < 1000 and score2 < 1000:
        next_rolls = list(islice(dice, 3))
        dice_count = next_rolls[-1][0]
        move1 = sum(n[1] for n in next_rolls)
        pos1 = advance(pos1, move1)
        score1 += pos1
        if score1 >= 1000:
            break

        next_rolls = list(islice(dice, 3))
        dice_count = next_rolls[-1][0]
        move2 = sum(n[1] for n in next_rolls)
        pos2 = advance(pos2, move2)
        score2 += pos2

    print(min(score1, score2) * dice_count)


class BoardState(NamedTuple):
    pos1: int
    score1: int
    pos2: int
    score2: int


def part2(pos1: int, pos2: int):
    player1_wins = 0
    player2_wins = 0
    boards = Counter([BoardState(pos1, 0, pos2, 0)])
    player1_turn = True
    WIN_THRESHOLD = 21
    dice_values = [1, 2, 3]
    possible_dice_rolls = Counter([sum(cartesian_product) for cartesian_product in product(dice_values, repeat=3)])
    while boards:
        # In every iteration of this while loop, we compute all possible outcomes of the next move
        new_boards = Counter()
        for board, n_boards in boards.items():
            if player1_turn:
                for d, n_dice_sequences in possible_dice_rolls.items():
                    new_pos1 = advance(board.pos1, d)
                    new_board = BoardState(new_pos1, board.score1 + new_pos1, board.pos2, board.score2)
                    if new_board.score1 >= WIN_THRESHOLD:
                        player1_wins += n_boards * n_dice_sequences
                    else:
                        new_boards[new_board] += n_boards * n_dice_sequences
            else:
                for d, n_dice_sequences in possible_dice_rolls.items():
                    new_pos2 = advance(board.pos2, d)
                    new_board = BoardState(board.pos1, board.score1, new_pos2, board.score2 + new_pos2)
                    if new_board.score2 >= WIN_THRESHOLD:
                        player2_wins += n_boards * n_dice_sequences
                    else:
                        new_boards[new_board] += n_boards * n_dice_sequences

        player1_turn = not player1_turn
        boards = new_boards

    print(max(player1_wins, player2_wins))


def advance(pos: int, move: int) -> int:
    return ((pos - 1 + move) % 10) + 1


if __name__ == '__main__':
    main()
