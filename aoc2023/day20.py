from __future__ import annotations

import operator
import re
import sys
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


class BroadcastModule(Module):
    def receive_pulse(self, input_label: str, pulse: Pulse) -> Iterable[Pulse]:
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


class ConjunctionModule(Module):
    def __init__(self, label: str, output_labels: list[str]):
        super().__init__(label, output_labels)

        self.last_inputs = {}

    def set_input_labels(self, input_labels: list[str]):
        self.last_inputs = {label: Pulse.LOW for label in input_labels}

    def receive_pulse(self, input_label: str, pulse: Pulse) -> Iterable[Pulse]:
        self.last_inputs[input_label] = pulse
        if all(p == Pulse.HIGH for p in self.last_inputs.values()):
            for output in self.output_labels:
                yield Message(Pulse.LOW, self.label, output)
        else:
            for output in self.output_labels:
                yield Message(Pulse.HIGH, self.label, output)

    def __repr__(self):
        return f'&{self.label}: {", ".join(f"{k}: {1 if v == Pulse.HIGH else 0}" for k, v in self.last_inputs.items())}'


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
    with open(sys.argv[1]) as f:
        lines = f.readlines()

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
    keyed_modules = parse_modules(lines, True)

    queue = deque()
    for i in range(1_000):
        queue.append(Message(Pulse.LOW, 'button', 'broadcaster'))
        while queue:
            pulse, source, target = queue.popleft()
            # if target == 'rx':
            #     print('\n', i, pulse)
            module = keyed_modules[target]
            queue.extend(module.receive_pulse(source, pulse))
    return None


if __name__ == '__main__':
    main()
