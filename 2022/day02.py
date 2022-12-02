import sys

ROCK = 0
PAPER = 1
SCISSORS = 2

LEFT = {
    'A': ROCK,
    'B': PAPER,
    'C': SCISSORS
}

RIGHT = {
    'X': ROCK,
    'Y': PAPER,
    'Z': SCISSORS
}


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    total_score = 0
    for line in lines:
        left_sym, right_sym = line.strip().split(' ')
        left_move = LEFT[left_sym]
        right_move = RIGHT[right_sym]
        total_score += get_score(left_move, right_move)

    print(total_score)

    total_score = 0
    for line in lines:
        left_sym, right_sym = line.strip().split(' ')
        left_move = LEFT[left_sym]
        if right_sym == 'X':
            # right should lose
            right_move = (left_move - 1) % 3
        elif right_sym == 'Y':
            right_move = left_move
        else:
            # right should win
            right_move = (left_move + 1) % 3

        total_score += get_score(left_move, right_move)

    print(total_score)


def get_score(left_move, right_move):
    if left_move == right_move:
        return right_move + 4
    elif (left_move + 1) % 3 == right_move:
        # right wins
        return 7 + right_move
    else:
        return 1 + right_move


if __name__ == '__main__':
    main()
