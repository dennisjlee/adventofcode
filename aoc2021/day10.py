import sys
from collections import deque

MATCHING_OPEN_CHARS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}
MATCHING_CLOSE_CHARS = {v: k for k, v in MATCHING_OPEN_CHARS.items()}

OPEN_CHARS = set(MATCHING_OPEN_CHARS.values())
CLOSE_CHARS = set(MATCHING_OPEN_CHARS.keys())

INVALID_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

INCOMPLETE_POINTS = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    incomplete_lines = []

    # part1
    total_points = 0
    for line in lines:
        score = get_invalid_score(line)
        total_points += score
        if score == 0:
            incomplete_lines.append(line)

    print(total_points)

    # part2
    incomplete_scores = sorted(get_incomplete_score(line) for line in incomplete_lines)
    print(incomplete_scores[len(incomplete_scores) // 2])


def get_invalid_score(line):
    stack = deque()
    for i, c in enumerate(line):
        if c in OPEN_CHARS:
            stack.append(c)
        elif c in CLOSE_CHARS:
            top = stack.pop()
            if MATCHING_OPEN_CHARS[c] != top:
                return INVALID_POINTS[c]
    return 0


def get_incomplete_score(line):
    stack = deque()
    for i, c in enumerate(line):
        if c in OPEN_CHARS:
            stack.append(c)
        elif c in CLOSE_CHARS:
            top = stack.pop()
            assert MATCHING_OPEN_CHARS[c] == top

    score = 0
    while stack:
        top = stack.pop()
        score = score * 5 + INCOMPLETE_POINTS[top]

    return score


if __name__ == '__main__':
    main()
