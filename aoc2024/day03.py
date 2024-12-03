from collections import Counter
import re
import sys
import re


MULTIPLY_REGEX = re.compile(r'mul\((\d+),(\d+)\)')
MULTIPLY_CONDITIONAL_REGEX = re.compile(r"(do(?:n't)?)\(\)|mul\((\d+),(\d+)\)")


def main():
    with open(sys.argv[1]) as f:
        content = f.read()

    sum_product = 0
    for m in MULTIPLY_REGEX.finditer(content):
        f1 = int(m.group(1))
        f2 = int(m.group(2))
        sum_product += f1 * f2
    print(sum_product)

    enabled = True
    enabled_sum_product = 0
    for m in MULTIPLY_CONDITIONAL_REGEX.finditer(content):
        op = m.group(1)
        if op == 'do':
            enabled = True
        elif op == "don't":
            enabled = False
        elif enabled:
            f1 = int(m.group(2))
            f2 = int(m.group(3))
            enabled_sum_product += f1 * f2
    print(enabled_sum_product)


if __name__ == '__main__':
    main()
