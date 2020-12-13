from collections import defaultdict, deque
import itertools
import sys


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f]

    timestamp = int(lines[0])
    bus_ids = [int(s) for s in lines[1].split(',') if s != 'x']

    # part1
    best = 1000000
    best_bus = None
    for bus in bus_ids:
        delay = bus - (timestamp % bus)
        if delay < best:
            best_bus = bus
            best = delay
    print(best * best_bus)

    # part2
    bus_ids = []
    indexed_buses = {}
    for i, bus_id in enumerate(lines[1].split(',')):
        if bus_id == 'x':
            continue
        bus_id = int(bus_id)
        bus_ids.append((i, bus_id))
        indexed_buses[i] = bus_id

    # list of tuples (coefficient c_i, dict from bus_id to mod)
    coefficients_and_mods = []

    remaining_bus_ids = deque(bus_ids)
    index, base = remaining_bus_ids.popleft()
    assert index == 0
    coefficients = {}
    for i, other_base in remaining_bus_ids:
        coefficients[other_base] = simplify_mod_product(other_base, base % other_base, (index - i) % other_base)
    coefficients_and_mods.append((base, coefficients))
    while True:
        index, base = remaining_bus_ids.popleft()
        if not remaining_bus_ids:
            break
        last_coefficients = coefficients_and_mods[-1][1]
        coefficients = {}
        for i, other_base in remaining_bus_ids:
            coefficients[other_base] = simplify_mod_product(other_base,
                                                            base % other_base,
                                                            (last_coefficients[other_base] - last_coefficients[base])
                                                            % other_base)
        coefficients_and_mods.append((base, coefficients))

    current_coefficient = None
    prev_base = None
    for base, coefficients in reversed(coefficients_and_mods):
        if prev_base is None:
            _, prev_mod = next(item for item in coefficients.items())
            current_coefficient = prev_mod
            prev_base = base
        else:
            current_coefficient = prev_base * current_coefficient + coefficients[prev_base]
            prev_base = base

    print(current_coefficient * prev_base)


def simplify_mod_product(base, factor, value):
    """
    Assuming (factor * k) % base == value, return v such that k % base == v
    Also assumes that base is prime.
    """
    return next(i for i in range(base) if factor * i % base == value)


if __name__ == '__main__':
    main()
