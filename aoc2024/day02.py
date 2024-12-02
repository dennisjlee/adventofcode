from collections import Counter
import re
import sys


def main():
    reports: list[list[int]] = []

    with open(sys.argv[1]) as f:
        for line in f.readlines():
            words = line.strip().split()
            reports.append([int(w) for w in words])

    safe_count = 0
    dampened_safe_count = 0
    for report in reports:
        if is_safe(report):
            safe_count += 1
            dampened_safe_count += 1
        else:
            for i in range(len(report)):
                if is_safe(report[:i] + report[i + 1:]):
                    dampened_safe_count += 1
                    break

    print(safe_count)
    print(dampened_safe_count)


def is_safe(report: list[int]):
    diff = report[1] - report[0]
    lower_bound = 1 if diff >= 0 else -3
    upper_bound = 3 if diff >= 0 else -1
    if lower_bound <= diff <= upper_bound:
        for i in range(2, len(report)):
            diff = report[i] - report[i - 1]
            if not (lower_bound <= diff <= upper_bound):
                return False
        else:
            return True
    return False


if __name__ == '__main__':
    main()
