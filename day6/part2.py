import re
import sys

def main():
    with open(sys.argv[1]) as f:
        batch = f.read()

    total_common_yeses = 0
    groups = batch.split('\n\n')
    for group in groups:
        answers = [set(line) for line in group.strip().split('\n')]
        common_yeses = len(answers[0].intersection(*answers[1:]))
        total_common_yeses += common_yeses

    print(total_common_yeses)



if __name__ == '__main__':
    main()
