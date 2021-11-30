from collections import Counter
import re
import sys

def main():
    with open(sys.argv[1]) as f:
        joltages = [int(l.strip()) for l in f]

    # part 1
    joltages.append(0)
    joltages.sort()
    difference_counts = Counter()
    difference_counts[3] = 1  # for the device itself
    for i in range(1, len(joltages)):
        diff = joltages[i] - joltages[i-1]
        difference_counts[diff] += 1
    print(difference_counts[1] * difference_counts[3])

    # part 2
    scenarios = generate_scenarios(joltages)
    print(scenarios[0])


# return scenarios with minimum joltage and count of combinations
def generate_scenarios(joltages):
    if len(joltages) == 1:
        return {joltages[0]: 1}
    first = joltages[0]
    scenarios = generate_scenarios(joltages[1:])
    count_including_first = 0
    for min_joltage, count in list(scenarios.items()):
        if min_joltage - first <= 3:
            count_including_first += count
        else:
            # too far apart
            del scenarios[min_joltage]
    if count_including_first:
        scenarios[first] = count_including_first
    return scenarios


if __name__ == '__main__':
    main()
