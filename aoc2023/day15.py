from __future__ import annotations

import sys
from typing import NamedTuple, Literal
import re


def hash_str(s: str) -> int:
    code = 0
    for c in s:
        code += ord(c)
        code = (17 * code) % 256
    return code


INSTRUCTION_REGEX = re.compile(r'([a-z]+)([-=])(\d?)')


class Step(NamedTuple):
    label: str
    operation: Literal["-", "="]
    value: int | None

    @staticmethod
    def parse(s: str):
        match = INSTRUCTION_REGEX.match(s)
        label = match.group(1)
        operation = match.group(2)
        value = int(match.group(3)) if operation == '=' else None
        return Step(label, operation, value)


def main():
    with open(sys.argv[1]) as f:
        step_strings = f.read().strip().split(',')

    # part 1
    print(sum(hash_str(s) for s in step_strings))

    # part 2
    boxes = [{} for _ in range(256)]
    steps = [Step.parse(s) for s in step_strings]
    for step in steps:
        box = boxes[hash_str(step.label)]
        if step.operation == '-':
            box.pop(step.label, None)
        else:
            box[step.label] = step.value

    focusing_power = 0
    for box_index, box in enumerate(boxes):
        # Take advantage of the fact that Python dicts preserve insertion order!
        for slot_index, value in enumerate(box.values()):
            focusing_power += (box_index + 1) * (slot_index + 1) * value

    print(focusing_power)




if __name__ == '__main__':
    main()
