import operator
import re
import sys
from collections import Counter
from functools import reduce

id_regex = re.compile(r'Game (\d+): (.*)')

def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    id_total = 0
    power_total = 0
    comparison = Counter({'red': 12, 'green': 13, 'blue': 14})

    for line in lines:
        match = id_regex.search(line)
        id = match.group(1)
        outcomes = match.group(2).split('; ')

        outcome_counters = []
        for outcome in outcomes:
            counts = {}
            for count_str in outcome.split(', '):
                count, color = count_str.split(' ')
                counts[color] = int(count)
            outcome_counters.append(Counter(counts))

        if all(comparison > counter for counter in outcome_counters):
            id_total += int(id)

        union = reduce(operator.or_, outcome_counters, Counter())
        power_total += union['red'] * union['green'] * union['blue']


    print(id_total)
    print(power_total)


if __name__ == '__main__':
    main()
