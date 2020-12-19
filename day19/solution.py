import re
import sys

RULE_PARSER = re.compile(r'(\d+): (?:"(\w)")?(\d.*)?')


class Rule:
    def __init__(self, line):
        match = RULE_PARSER.match(line)
        self.index = int(match.group(1))
        if match.group(2):
            self.terminal_symbol = match.group(2)
            self.options = ()
        else:
            self.terminal_symbol = None
            rest = match.group(3)
            self.options = [
                [int(s) for s in option.strip().split(' ')]
                for option in rest.split('|')
            ]

    def __repr__(self):
        if self.terminal_symbol:
            return f'{self.index} -> `{self.terminal_symbol}`'
        else:
            return f'{self.index} -> {repr(self.options)}'

    def matches_whole_string(self, indexed_rules, message: str):
        for possible_match_end in self.possible_matches(indexed_rules, message, 0):
            if possible_match_end == len(message):
                return True
        return False

    def possible_matches(self, indexed_rules, message: str, start=0):
        """
        :param indexed_rules:
        :param message:
        :param start:
        :return: generator of the indexes into this string that we could possibly match up to
        """
        if start >= len(message):
            return
        if self.terminal_symbol:
            if message[start] == self.terminal_symbol:
                yield start+1
            else:
                return
        for option in self.options:
            next_indexes = {start}
            for rule_index in option:
                rule_matches = set()
                sub_rule = indexed_rules[rule_index]
                for start_index in next_indexes:
                    rule_matches |= set(
                        sub_rule.possible_matches(indexed_rules, message, start_index))
                next_indexes = rule_matches
                if not next_indexes:
                    break
            if next_indexes:
                for next_index in next_indexes:
                    yield next_index
            else:
                continue


def main():
    with open(sys.argv[1]) as f:
        sections = f.read().split('\n\n')

    rule_lines = sections[0].strip().split('\n')
    messages = sections[1].strip().split('\n')

    indexed_rules = {}
    for line in rule_lines:
        rule = Rule(line)
        indexed_rules[rule.index] = rule

    # part1
    rule0 = indexed_rules[0]
    match_count = sum(
        1 for message in messages
        if rule0.matches_whole_string(indexed_rules, message))
    print(match_count)

    # part2
    indexed_rules2 = indexed_rules.copy()
    indexed_rules2[8] = Rule('8: 42 | 42 8')
    indexed_rules2[11] = Rule('11: 42 31 | 42 11 31')
    match_count = sum(
        1 for message in messages
        if rule0.matches_whole_string(indexed_rules2, message))
    print(match_count)


if __name__ == '__main__':
    main()
