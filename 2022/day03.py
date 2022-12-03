import sys


def priority(c):
    if c >= 'a':
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    total_score = 0
    for line in lines:
        left = set(line[:(len(line) // 2)])
        right = set(line[(len(line) // 2):])
        intersection = left & right
        assert len(intersection) == 1
        total_score += priority(list(intersection)[0])

    print(total_score)

    total_score = 0
    for i in range(0, len(lines), 3):
        s0 = set(lines[i])
        s1 = set(lines[i + 1])
        s2 = set(lines[i + 2])

        intersection = s0 & s1 & s2
        assert len(intersection) == 1
        total_score += priority(list(intersection)[0])

    print(total_score)


if __name__ == '__main__':
    main()
