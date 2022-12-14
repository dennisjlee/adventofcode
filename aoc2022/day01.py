import sys


def main():
    grouped_calories = []
    with open(sys.argv[1]) as f:
        groups = f.read().strip().split('\n\n')
        for group in groups:
            grouped_calories.append([int(line.strip()) for line in group.split('\n')])

    print(max(sum(group) for group in grouped_calories))

    desc_totals = sorted([sum(group) for group in grouped_calories], reverse=True)
    print(sum(desc_totals[:3]))


if __name__ == '__main__':
    main()
