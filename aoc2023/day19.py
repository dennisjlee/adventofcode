from __future__ import annotations

import operator
import re
import sys
from typing import NamedTuple, Literal


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


class Range(NamedTuple):
    """NOTE: includes start and excludes end, like Python's `range` function"""
    start: int
    end: int

    @property
    def size(self):
        return self.end - self.start


class PartRange(NamedTuple):
    x: Range
    m: Range
    a: Range
    s: Range

    @property
    def combinations(self):
        return self.x.size * self.m.size * self.a.size * self.s.size


class PartRangeResult(NamedTuple):
    part_range: PartRange
    result: str | None


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

    def eval_range(self, part_range: PartRange) -> list[PartRangeResult]:
        results = []
        prop = self.prop
        comparison = self.comparison
        relevant_range: Range = getattr(part_range, prop)
        if self.op == '<':
            if comparison > relevant_range.start:
                if comparison >= relevant_range.end:
                    # condition will always be satisfied
                    results.append(PartRangeResult(part_range, self.result))
                else:
                    low_range = part_range._replace(**{prop: Range(relevant_range.start, comparison)})
                    high_range = part_range._replace(**{prop: Range(comparison, relevant_range.end)})
                    results.append(PartRangeResult(low_range, self.result))
                    results.append(PartRangeResult(high_range, None))
        else:
            if comparison < relevant_range.end - 1:
                if comparison < relevant_range.start:
                    # condition will always be satisfied
                    results.append(PartRangeResult(part_range, self.result))
                else:
                    high_range = part_range._replace(**{prop: Range(comparison + 1, relevant_range.end)})
                    low_range = part_range._replace(**{prop: Range(relevant_range.start, comparison + 1)})
                    results.append(PartRangeResult(high_range, self.result))
                    results.append(PartRangeResult(low_range, None))
        return results


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

    def eval_range(self, part_range: PartRange) -> list[PartRangeResult]:
        part_range_results = []
        part_ranges = [part_range]
        for condition in self.conditions:
            new_part_ranges: list[PartRange] = []
            for part_range in part_ranges:
                condition_results = condition.eval_range(part_range)
                for range_result in condition_results:
                    if range_result.result:
                        part_range_results.append(range_result)
                    else:
                        new_part_ranges.append(range_result.part_range)

            part_ranges = new_part_ranges

        for part_range in part_ranges:
            part_range_results.append(PartRangeResult(part_range, self.fallback))

        return part_range_results


FINAL_LABELS = {'A', 'R'}


def eval_workflows(keyed_workflows: dict[str, Workflow], part: Part) -> bool:
    label = 'in'
    while label not in FINAL_LABELS:
        workflow = keyed_workflows[label]
        label = workflow.eval(part)

    return label == 'A'


def eval_workflow_ranges(keyed_workflows: dict[str, Workflow]) -> list[PartRangeResult]:
    queue = [PartRangeResult(PartRange(Range(1, 4001), Range(1, 4001), Range(1, 4001), Range(1, 4001)), 'in')]
    final_results: list[PartRangeResult] = []
    while queue:
        part_range_result = queue.pop()
        if part_range_result.result in FINAL_LABELS:
            final_results.append(part_range_result)
        else:
            queue.extend(keyed_workflows[part_range_result.result].eval_range(part_range_result.part_range))

    return final_results


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

    total_combinations = 0
    range_results = eval_workflow_ranges(keyed_workflows)
    for part_range, result in range_results:
        if result == 'A':
            total_combinations += part_range.combinations
    print(total_combinations)


if __name__ == '__main__':
    main()
