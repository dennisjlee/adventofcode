import sys
from collections import Counter


def main():
    with open(sys.argv[1]) as f:
        orig_fish = [int(w) for w in f.readline().strip().split(',')]

    # part 1
    fish = orig_fish
    for _ in range(80):
        new_fish = []
        for f in fish:
            if f == 0:
                new_fish.append(6)
                new_fish.append(8)
            else:
                new_fish.append(f - 1)
        fish = new_fish

    print(len(fish))

    # part 2
    fish_counts = Counter(orig_fish)

    for _ in range(256):
        new_fish_counts = Counter()
        for f, count in fish_counts.items():
            if f == 0:
                new_fish_counts[6] += count
                new_fish_counts[8] += count
            else:
                new_fish_counts[f-1] += count
        fish_counts = new_fish_counts

    print(sum(fish_counts.values()))


if __name__ == '__main__':
    main()
