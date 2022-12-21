from __future__ import annotations

import re
import sys
from operator import add, sub, mul, floordiv
from typing import Optional

NUMBER_REGEX = re.compile(r'-?\d+')

OP_MAP = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': floordiv
}


class Monkey:
    name: str
    left: Optional[str] = None
    op: Optional[str] = None
    right: Optional[str] = None
    result: Optional[int] = None
    has_human: bool = False

    def __init__(self, name: str, expression: str):
        self.name = name
        if NUMBER_REGEX.fullmatch(expression):
            self.result = int(expression)
        else:
            self.left, self.op, self.right = expression.split()

    def compute(self, monkeys: dict[str, Monkey]):
        if self.result is None:
            left = monkeys[self.left].compute(monkeys)
            right = monkeys[self.right].compute(monkeys)
            return OP_MAP[self.op](left, right)
        else:
            return self.result

    def __repr__(self):
        return f'Monkey(name=\'{self.name}\', has_human={self.has_human}, result={self.result}, left={self.left}, op={self.op}, right={self.right})'

    def find_human(self, monkeys: dict[str, Monkey]):
        if self.name == 'humn':
            self.has_human = True
        elif self.left and monkeys[self.left].find_human(monkeys):
            self.has_human = True
        elif self.right and monkeys[self.right].find_human(monkeys):
            self.has_human = True
        return self.has_human

    def solve_for_human(self, monkeys: dict[str, Monkey], desired_result: int):
        if self.name == 'humn':
            self.result = desired_result
            return desired_result
        elif monkeys[self.left].has_human:
            assert self.result is None and self.op is not None
            right_result = monkeys[self.right].compute(monkeys)
            if self.op == '+':
                left_desired_result = desired_result - right_result
            elif self.op == '-':
                left_desired_result = desired_result + right_result
            elif self.op == '*':
                left_desired_result = desired_result // right_result
            else:
                assert self.op == '/'
                left_desired_result = desired_result * right_result

            monkeys[self.left].solve_for_human(monkeys, left_desired_result)
        elif monkeys[self.right].has_human:
            assert self.result is None and self.op is not None
            left_result = monkeys[self.left].compute(monkeys)
            if self.op == '+':
                right_desired_result = desired_result - left_result
            elif self.op == '-':
                right_desired_result = left_result - desired_result
            elif self.op == '*':
                right_desired_result = desired_result // left_result
            else:
                assert self.op == '/'
                right_desired_result = left_result // desired_result
            monkeys[self.right].solve_for_human(monkeys, right_desired_result)


def main():
    monkeys_by_name = {}
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            name, expression = line.strip().split(': ')
            monkey = Monkey(name, expression)
            monkeys_by_name[name] = monkey

    # part 1
    root = monkeys_by_name['root']
    print(root.compute(monkeys_by_name))

    # part 2
    root.find_human(monkeys_by_name)
    if monkeys_by_name[root.left].has_human:
        desired_result = monkeys_by_name[root.right].compute(monkeys_by_name)
        monkeys_by_name[root.left].solve_for_human(monkeys_by_name, desired_result)
    elif monkeys_by_name[root.right].has_human:
        desired_result = monkeys_by_name[root.left].compute(monkeys_by_name)
        monkeys_by_name[root.right].solve_for_human(monkeys_by_name, desired_result)

    print(monkeys_by_name['humn'].result)


if __name__ == '__main__':
    main()
