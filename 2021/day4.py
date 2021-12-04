import sys


class BoardState:
    def __init__(self, lines):
        self.board = [
            [int(s) for s in line.strip().split()]
            for line in lines
        ]
        self.reverse_board = {
            self.board[i][j]: (i, j)
            for i in range(5)
            for j in range(5)
        }
        self.marked = [
            [False for _ in range(5)]
            for __ in range(5)
        ]
        self.won = False

    def mark(self, n):
        if n not in self.reverse_board:
            return False
        i, j = self.reverse_board[n]
        self.marked[i][j] = True

        self.won = (
                all(self.marked[ii][j] for ii in range(5))
                or all(self.marked[i][jj] for jj in range(5))
        )
        return self.won

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

    bingo_scores = list(find_bingos(numbers, boards))
    print(bingo_scores[0])
    print(bingo_scores[-1])


def find_bingos(numbers, boards):
    for n in numbers:
        for b in boards:
            if b.won:
                continue
            if b.mark(n):
                yield sum(b.unmarked_numbers()) * n


if __name__ == '__main__':
    main()
