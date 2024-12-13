from collections import Counter
import re
import sys


def main():
    list1: list[int] = []
    list2: list[int] = []

    with open(sys.argv[1]) as f:
        for line in f.readlines():
            word1, word2 = line.strip().split()
            list1.append(int(word1))
            list2.append(int(word2))

    sum_diffs = 0
    for n1, n2 in zip(sorted(list1), sorted(list2)):
        sum_diffs += abs(n1 - n2)

    print(sum_diffs)

    right_counter = Counter(list2)
    similarity_score = 0
    for n1 in list1:
        similarity_score += n1 * right_counter[n1]

    print(similarity_score)


if __name__ == "__main__":
    main()
