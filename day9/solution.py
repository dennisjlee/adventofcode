from collections import deque 
import re
import sys

def main():
    with open(sys.argv[1]) as f:
        numbers = [int(l.strip()) for l in f]

    current_window = deque(numbers[:25])

    # part 1
    invalid_index = None
    for i in range(25, len(numbers)):
        next_number = numbers[i]
        complements = set()
        found = False
        for n in current_window:
            if next_number - n in complements:
                found = True
                break
            complements.add(n)
        if not found:
            invalid_index = i
            break
        current_window.popleft()
        current_window.append(next_number)
    print(next_number)

    # part 2
    running_totals = numbers[:invalid_index]
    for i in range(1, len(running_totals)):
        running_totals[i] += running_totals[i-1]
    complement_indexes = {}
    for index, total in enumerate(running_totals):
        key = total - next_number
        if key in complement_indexes:
            prev_index = complement_indexes[key]
            break
        complement_indexes[total] = index
    contiguous_range = numbers[prev_index+1:index+1]
    print(min(contiguous_range) + max(contiguous_range))



if __name__ == '__main__':
    main()
