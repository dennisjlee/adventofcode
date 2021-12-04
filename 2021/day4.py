import sys


class BoardState:
    def __init__(self, lines):
        self.board = [
            [int(s) for s in line.strip().split()]
            for line in lines
        ]
        self.numbers = {n for row in self.board for n in row}
        self.marked = [
            [False for _ in range(5)]
            for __ in range(5)
        ]
        self.won = False

    def mark(self, n):
        if n not in self.numbers:
            return False
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == n:
                    self.marked[i][j] = True

                    self.won = (
                            all(self.marked[ii][j] for ii in range(5))
                            or all(self.marked[i][jj] for jj in range(5))
                    )
                    return self.won
        return False

    def unmarked_numbers(self):
        for i in range(5):
            for j in range(5):
                if not self.marked[i][j]:
                    yield self.board[i][j]


def main():
    boards = set()

    with open(sys.argv[1]) as f:
        lines = f.readlines()
        numbers = [int(s) for s in lines[0].strip().split(',')]
        for i in range(1, len(lines), 6):
            board = BoardState(lines[i + 1:i + 6])
            boards.add(board)

    print(find_bingo(numbers, boards))

    print(find_last_bingo(numbers, boards))


def find_bingo(numbers, boards):
    for n in numbers:
        for b in boards:
            is_bingo = b.mark(n)
            if is_bingo:
                return sum(b.unmarked_numbers()) * n


def find_last_bingo(numbers, boards):
    bingo_count = 0
    for n in numbers:
        for b in boards:
            if b.won:
                continue
            is_bingo = b.mark(n)
            if is_bingo:
                bingo_count += 1
                if bingo_count == len(boards) - 1:
                    return sum(b.unmarked_numbers()) * n


if __name__ == '__main__':
    main()
