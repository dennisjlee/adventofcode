from __future__ import annotations

import math
import operator
import re
import sys
from argparse import ArgumentParser
from collections import defaultdict, deque
from enum import Enum
from typing import NamedTuple, Literal, Iterable


class Pulse(Enum):
    LOW = 1
    HIGH = 2


class Message(NamedTuple):
    pulse: Pulse
    source: str
    target: str


class Module:
    label: str
    output_labels: list[str]

    def __init__(self, label: str, output_labels: list[str]):
        self.label = label
        self.output_labels = output_labels

    def receive_pulse(self, input_label: str, pulse: Pulse) -> Iterable[Message]:
        return []

    def __repr__(self):
        return self.label

    def __str__(self):
        return self.label


class BroadcastModule(Module):
    def receive_pulse(self, input_label: str, pulse: Pulse) -> Iterable[Message]:
        for output in self.output_labels:
            yield Message(pulse, self.label, output)


class FlipFlopModule(Module):
    enabled: bool

    def __init__(self, label: str, output_labels: list[str]):
        super().__init__(label, output_labels)
        self.enabled = False

    def receive_pulse(self, input_label: str, pulse: Pulse) -> Iterable[Message]:
        if pulse == Pulse.LOW:
            self.enabled = not self.enabled
            for output in self.output_labels:
                yield Message(Pulse.HIGH if self.enabled else Pulse.LOW, self.label, output)

    def __repr__(self):
        return f'%{self.label}: {1 if self.enabled else 0}'

    def __str__(self):
        return f'%{self.label}'


class ConjunctionModule(Module):
    def __init__(self, label: str, output_labels: list[str]):
        super().__init__(label, output_labels)

        self.last_inputs: dict[str, Pulse] = {}

    def set_input_labels(self, input_labels: list[str]):
        self.last_inputs = {label: Pulse.LOW for label in input_labels}

    def receive_pulse(self, input_label: str, pulse: Pulse) -> Iterable[Message]:
        self.last_inputs[input_label] = pulse
        if all(p == Pulse.HIGH for p in self.last_inputs.values()):
            for output in self.output_labels:
                yield Message(Pulse.LOW, self.label, output)
        else:
            for output in self.output_labels:
                yield Message(Pulse.HIGH, self.label, output)

    def __repr__(self):
        return f'&{self.label}: {", ".join(f"{k}: {1 if v == Pulse.HIGH else 0}" for k, v in self.last_inputs.items())}'

    def __str__(self):
        return f'&{self.label}'


PARSE_REGEX = re.compile(r'([&%]?)(\w+) -> (.*)$')


def parse(line: str) -> Module:
    match = PARSE_REGEX.match(line.strip())
    kind = match.group(1)
    label = match.group(2)
    output_labels = match.group(3).split(', ')
    if label == 'broadcaster':
        return BroadcastModule(label, output_labels)
    elif kind == '%':
        return FlipFlopModule(label, output_labels)
    elif kind == '&':
        return ConjunctionModule(label, output_labels)
    else:
        return Module(label, output_labels)


def parse_modules(lines: list[str], verbose=False) -> dict[str, Module]:
    modules = [parse(line) for line in lines]

    inputs_by_label = defaultdict(list)
    keyed_modules = {m.label: m for m in modules}
    for module in modules:
        for output in module.output_labels:
            inputs_by_label[output].append(module.label)
            if output not in keyed_modules:
                # blank output-only module
                keyed_modules[output] = Module(output, [])

    for module in modules:
        if isinstance(module, ConjunctionModule):
            module.set_input_labels(inputs_by_label[module.label])

    if verbose:
        queue = deque(['rx'])
        visited = set()
        while queue:
            label = queue.popleft()
            if label in visited:
                continue
            visited.add(label)
            inputs = inputs_by_label[label]
            kind = ''
            module = keyed_modules[label]
            if isinstance(module, FlipFlopModule):
                kind = '%'
            elif isinstance(module, ConjunctionModule):
                kind = '&'
            print(f'{kind}{label} <- {", ".join(inputs)}')
            queue.extend(inputs)

    return keyed_modules


def main():
    parser = ArgumentParser()
    parser.add_argument('--graphviz', action='store_true')
    parser.add_argument('input', help='input file')

    args = parser.parse_args()

    with open(args.input) as f:
        lines = f.readlines()

    if args.graphviz:
        print_graphviz(lines)
    else:
        print(part1(lines))
        print(part2(lines))


def part1(lines: list[str]):
    keyed_modules = parse_modules(lines)
    queue: deque[Message] = deque()
    pulse_counts = {
        Pulse.LOW: 0,
        Pulse.HIGH: 0
    }
    for i in range(1000):
        queue.append(Message(Pulse.LOW, 'button', 'broadcaster'))
        while queue:
            pulse, source, target = queue.popleft()
            pulse_counts[pulse] += 1
            module = keyed_modules[target]
            queue.extend(module.receive_pulse(source, pulse))
    return pulse_counts[Pulse.LOW] * pulse_counts[Pulse.HIGH]


def part2(lines: list[str]):
    keyed_modules = parse_modules(lines)

    queue = deque()
    first_high_pulse: dict[str, int] = {}
    for i in range(1, 10_000):
        queue.append(Message(Pulse.LOW, 'button', 'broadcaster'))
        while queue:
            pulse, source, target = queue.popleft()

            # `kj` is the conjunction module that is the only input to `rx`,
            # so it needs to receive 4 HIGH pulses from each of its inputs.
            # Based on observation, each of those inputs will produce a HIGH
            # on a recurring cycle, which happens to be a prime around 4000.
            if target == 'kj' and pulse == Pulse.HIGH:
                if source not in first_high_pulse:
                    first_high_pulse[source] = i
            module = keyed_modules[target]
            queue.extend(module.receive_pulse(source, pulse))
        if len(first_high_pulse) == 4:
            return math.lcm(*first_high_pulse.values())
    return None


def print_graphviz(lines: list[str]):
    # pipe this output to `dot -Tsvg > aoc2023/inputs/day20.svg`)

    keyed_modules = parse_modules(lines)
    ranks_by_module = {}
    queue = deque([('broadcaster', 0)])
    while queue:
        label, rank = queue.popleft()
        if label in ranks_by_module:
            continue
        ranks_by_module[label] = rank
        for output_label in keyed_modules[label].output_labels:
            queue.append((output_label, rank + 1))

    modules_by_rank = defaultdict(list)
    for label, rank in ranks_by_module.items():
        modules_by_rank[rank].append(label)

    print("strict digraph {")
    print("rankdir=LR;")
    print("node[ordering = out];")

    for module in keyed_modules.values():
        print(f'{module.label} [label="{str(module)}"];')
        for output_label in module.output_labels:
            print(f"{module.label} -> {output_label};")

    print(f"""
    {{
        rank = source;
        broadcaster;
    }}
    """)
    print(f"""
    {{
        rank = sink;
        rx;
    }}
    """)
    #
    # for rank, labels in sorted(modules_by_rank.items()):
    #     # https://stackoverflow.com/a/64007295
    #     print(f"""
    #     {{
    #         rank = same;
    #         rankdir = TB;
    #         // Here we enforce the desired order with "invisible" edges and arrowheads
    #         edge [style=invis];
    #         {' -> '.join(labels)};
    #     }}
    #     """)

    print("}")


if __name__ == '__main__':
    main()
