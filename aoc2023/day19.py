from __future__ import annotations

import operator
import sys
from bisect import insort_left
from collections import defaultdict
from typing import NamedTuple, Literal
import re


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @staticmethod
    def parse(s: str) -> Part:
        return eval(f'Part({s.strip()[1:-1]})')

    def total(self) -> int:
        return self.x + self.m + self.a + self.s


CONDITION_REGEX = re.compile(r'([xmas])([<>])(\d+):(\w+)')


class Condition(NamedTuple):
    prop: Literal['x', 'm', 'a', 's']
    op: Literal['<', '>']
    comparison: int
    result: str

    @staticmethod
    def parse(s: str):
        match = CONDITION_REGEX.match(s)
        return Condition(match.group(1), match.group(2), int(match.group(3)), match.group(4))

    def eval(self, part: Part) -> str | None:
        op = operator.lt if self.op == '<' else operator.gt
        if op(getattr(part, self.prop), self.comparison):
            return self.result
        return None


WORKFLOW_REGEX = re.compile(r'(\w+){(.*),(\w+)}')


class Workflow(NamedTuple):
    label: str
    conditions: tuple[Condition, ...]
    fallback: str

    @staticmethod
    def parse(line: str):
        match = WORKFLOW_REGEX.match(line)
        label = match.group(1)
        fallback = match.group(3)
        condition_strs = match.group(2).split(',')
        conditions = tuple(Condition.parse(s) for s in condition_strs)
        return Workflow(label, conditions, fallback)

    def eval(self, part: Part) -> str:
        for condition in self.conditions:
            if result := condition.eval(part):
                return result
        return self.fallback


def eval_workflows(keyed_workflows: dict[str, Workflow], part: Part) -> bool:
    label = 'in'
    while label != 'A' and label != 'R':
        workflow = keyed_workflows[label]
        label = workflow.eval(part)

    return label == 'A'


def main():
    with open(sys.argv[1]) as f:
        workflow_block, part_block = f.read().split('\n\n')

    workflows = [Workflow.parse(line) for line in workflow_block.strip().split('\n')]

    keyed_workflows = {
        w.label: w
        for w in workflows
    }

    parts = [Part.parse(line) for line in part_block.strip().split('\n')]
    accepted = [part for part in parts if eval_workflows(keyed_workflows, part)]
    print(sum(a.total() for a in accepted))




if __name__ == '__main__':
    main()
