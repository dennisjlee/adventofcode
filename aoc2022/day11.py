from __future__ import annotations

import math
from copy import deepcopy
from typing import NamedTuple, Callable
import re
import sys


class Result(NamedTuple):
    item: int
    monkey_index: int


class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    mod_base: int
    true_case: int
    false_case: int

    def __init__(self, items, operation, mod_base, true_case, false_case):
        self.items = items
        self.operation = operation
        self.mod_base = mod_base
        self.true_case = true_case
        self.false_case = false_case
        self.inspected_items = 0

    def inspect_item(self, item, with_divide=True) -> Result:
        self.inspected_items += 1
        item = self.operation(item)
        if with_divide:
            item //= 3
        new_monkey_index = self.true_case if (item % self.mod_base) == 0 else self.false_case
        return Result(item, new_monkey_index)


def run_turn(monkeys: list[Monkey]):
    for monkey_index, monkey in enumerate(monkeys):
        for initial_item in monkey.items:
            item, new_monkey_index = monkey.inspect_item(initial_item)
            next_monkey = monkeys[new_monkey_index]
            next_monkey.items.append(item)
        monkey.items.clear()


def run_turn2(monkeys: list[Monkey], lcd: int):
    for monkey_index, monkey in enumerate(monkeys):
        for initial_item in monkey.items:
            item, new_monkey_index = monkey.inspect_item(initial_item, with_divide=False)
            next_monkey = monkeys[new_monkey_index]
            next_monkey.items.append(item % lcd)
        monkey.items.clear()


MONKEY_REGEX = re.compile(r'Monkey (\d+):\n\s*Starting items: ([\d, ]+)\n\s*Operation: new = (.*?)\n\s*Test: divisible by (\d+)\n\s*If true: throw to monkey (\d+)\n\s*If false: throw to monkey (\d+)')


def main():
    with open(sys.argv[1]) as f:
        content = f.read()

    monkeys = []
    for match in MONKEY_REGEX.finditer(content):
        items = [int(v) for v in match.group(2).split(', ')]
        operation = eval(f'lambda old: {match.group(3)}')
        monkeys.append(Monkey(items,
                              operation,
                              int(match.group(4)),
                              int(match.group(5)),
                              int(match.group(6))))

    monkeys2 = deepcopy(monkeys)

    for i in range(20):
        run_turn(monkeys)

    busiest_monkeys = sorted(monkeys, key=lambda m: m.inspected_items, reverse=True)
    print(busiest_monkeys[0].inspected_items * busiest_monkeys[1].inspected_items)

    lcd = math.prod(m.mod_base for m in monkeys)
    for i in range(10000):
        run_turn2(monkeys2, lcd)

    busiest_monkeys = sorted(monkeys2, key=lambda m: m.inspected_items, reverse=True)
    print(busiest_monkeys[0].inspected_items * busiest_monkeys[1].inspected_items)


if __name__ == '__main__':
    main()
