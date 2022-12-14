import sys
from collections import Counter


def main():
    rules = {}

    with open(sys.argv[1]) as f:
        contents = f.read()
        polymer_template, rules_lines = contents.split('\n\n')
        polymer_template = polymer_template.strip()
        for line in rules_lines.strip().split('\n'):
            left, right = line.strip().split(' -> ')
            rules[left] = right

    current = polymer_template
    for step in range(10):
        current = react_polymer(current, rules)

    counts = Counter(current)
    sorted_counts = sorted(counts.values())
    print(sorted_counts[-1] - sorted_counts[0])

    # part 2
    polymer_counter = Counter()
    for i in range(len(polymer_template) - 1):
        polymer_counter[polymer_template[i:i+2]] += 1

    for step in range(40):
        polymer_counter = fast_react_polymer(polymer_counter, rules)

    letter_counter = Counter()
    for i, item in enumerate(polymer_counter.items()):
        pair, count = item
        letter_counter[pair[0]] += count

    # The very last original letter will still be last, and needs to be counted in addition to the first of every pair
    letter_counter[polymer_template[-1]] += 1

    sorted_counts = sorted(letter_counter.values())
    print(sorted_counts[-1] - sorted_counts[0])


def react_polymer(polymer, rules):
    output = []
    for i in range(len(polymer) - 1):
        output.append(polymer[i])
        output.append(rules[polymer[i:i+2]])
    output.append(polymer[-1])
    return ''.join(output)


def fast_react_polymer(polymer_counter: Counter[str], rules: dict[str, str]) -> Counter[str]:
    new_polymer = Counter()
    for pair, count in polymer_counter.items():
        insert_letter = rules[pair]
        new_polymer[pair[0] + insert_letter] += count
        new_polymer[insert_letter + pair[1]] += count
    return new_polymer


if __name__ == '__main__':
    main()
