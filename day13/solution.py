from collections import deque
import sys
from typing import List, Dict, Tuple


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f]

    part1(lines)
    part2(lines)


def part1(lines: List[str]):
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


def part2(lines: List[str]):
    bus_ids: List[Tuple[int, int]] = []
    indexed_buses: Dict[int, int] = {}
    for i, bus_id in enumerate(lines[1].split(',')):
        if bus_id == 'x':
            continue
        bus_id = int(bus_id)
        bus_ids.append((i, bus_id))
        indexed_buses[i] = bus_id

    # list of tuples (coefficient c_i, dict from bus_id to mod)
    coefficients_and_mods: List[Tuple[int, Dict[int, int]]] = []

    remaining_bus_ids = deque(bus_ids)
    index, base = remaining_bus_ids.popleft()
    assert index == 0

    # Build up a set of equations to solve for the minimum timestamp (t) that meets the criteria.
    # Starting with the first number with offset 0 (b_0), assign it a coefficient k_0 such that
    # t = k_0 * b_0
    # Then we can relate k_0 to the other base numbers in the input.
    # For instance, for the input "17,x,13,19", t = 17 * k_0, and we also know that we need to satisfy the conditions
    # t mod 13 = 11, t mod 19 = 16. We use some identity functions to solve for this:
    # (ab) mod n = ((a mod n)(b mod n)) mod n
    # (a + b) mod n = ((a mod n) + (b mod n)) mod n
    # (thanks wikipedia! https://en.wikipedia.org/wiki/Modulo_operation#Properties_(identities)).
    # For example:
    #   (17 * k_0) mod 13 = 11
    #   ((17 mod 13) * (k_0 mod 13)) mod 13 = 11
    #   (4 * (k_0 mod 13)) mod 13 = 11
    #   (4 * 6) mod 13 = 11
    #   k_0 mod 13 = 6
    #
    # Then, we can define new variables for coefficients of the subsequent bus IDs, and continue reducing them this way
    # until we are at the last one. There we'll arrive at one remaining equation like (k mod x = y), and we can pick the
    # minimal possible value of k, which would simply be y.
    coefficients = {}
    for i, other_base in remaining_bus_ids:
        coefficients[other_base] = simplify_mod_product(other_base, base % other_base, (index - i) % other_base)
    coefficients_and_mods.append((base, coefficients))
    while True:
        index, base = remaining_bus_ids.popleft()
        if not remaining_bus_ids:
            break
        last_coefficients: Dict[int, int] = coefficients_and_mods[-1][1]
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


def simplify_mod_product(base: int, factor: int, value: int) -> int:
    """
    Assuming (factor * k) % base == value, return v such that k % base == v
    Also assumes that base is prime.
    There seem to be efficient ways to compute this result (https://en.wikipedia.org/wiki/Modular_arithmetic#Properties)
    but the numbers in this problem are relatively small so brute forcing it is fast enough.
    This function's big O runtime is linear to the magnitude of each base, which is several hundred.
    """
    return next(i for i in range(base) if factor * i % base == value)


if __name__ == '__main__':
    main()
