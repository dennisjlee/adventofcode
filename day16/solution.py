from functools import reduce
import operator
import re
import sys
from typing import Iterable, List, Optional, Set

RULE_RE = re.compile(r'(.*?): (\d+)-(\d+) or (\d+)-(\d+)')


class Rule:
    def __init__(self, rule_line):
        match = RULE_RE.match(rule_line)
        self.field_name = match.group(1)
        self.range1 = (int(match.group(2)), int(match.group(3)))
        self.range2 = (int(match.group(4)), int(match.group(5)))

    def matches(self, value):
        return (self.range1[0] <= value <= self.range1[1]) \
            or (self.range2[0] <= value <= self.range2[1])


def parse_ticket(line: str):
    return [int(s) for s in line.strip().split(',')]


def main():
    with open(sys.argv[1]) as f:
        sections = f.read().split('\n\n')

    rules = [Rule(line) for line in sections[0].split('\n')]

    my_ticket = parse_ticket(sections[1].split('\n')[1])

    nearby_tickets = [parse_ticket(line) for line in sections[2].strip().split('\n')[1:]]

    valid_tickets = list(part1(rules, nearby_tickets))
    part2(rules, my_ticket, valid_tickets)


def part1(rules: List[Rule], nearby_tickets: List[List[int]]) -> Iterable[List[int]]:
    invalid_value_sum = 0
    for ticket in nearby_tickets:
        valid_ticket = True
        for value in ticket:
            has_match = any(rule.matches(value) for rule in rules)
            if not has_match:
                invalid_value_sum += value
                valid_ticket = False
        if valid_ticket:
            yield ticket
    print(invalid_value_sum)


def matching_rules(rules: List[Rule], value: int) -> Set[Rule]:
    return {rule for rule in rules if rule.matches(value)}


def part2(rules: List[Rule], my_ticket: List[int], valid_tickets: List[List[int]]):
    possible_rules: List[Optional[Set[Rule]]] = [matching_rules(rules, value) for value in my_ticket]
    for ticket in valid_tickets:
        for i, value in enumerate(ticket):
            possible_rules[i] &= matching_rules(rules, value)

    final_rules: List[Optional[Rule]] = [None for _ in my_ticket]
    while any(possible_rules):
        for i, ruleset in enumerate(possible_rules):
            if ruleset and len(ruleset) == 1:
                rule = ruleset.pop()
                final_rules[i] = rule
                possible_rules[i] = None
                for other_ruleset in possible_rules:
                    if other_ruleset:
                        other_ruleset.remove(rule)

    matching_ticket_fields = [
        value for i, value in enumerate(my_ticket)
        if final_rules[i].field_name.startswith('departure')
    ]
    print(reduce(operator.mul, matching_ticket_fields, 1))


if __name__ == '__main__':
    main()
