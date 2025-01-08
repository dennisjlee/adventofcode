from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import Literal, Iterator

LogicGateOperand = Literal["AND", "OR", "XOR", None]


@dataclass
class LogicGate:
    id: str
    op: LogicGateOperand
    left: str | None = None
    right: str | None = None
    output: int | None = None

    def get_output(self, gates_by_id: dict[str, LogicGate]) -> int:
        if self.output is not None:
            return self.output

        assert self.left and self.right
        left_out = gates_by_id[self.left].get_output(gates_by_id)
        right_out = gates_by_id[self.right].get_output(gates_by_id)
        if self.op == "AND":
            output = left_out & right_out
        elif self.op == "OR":
            output = left_out | right_out
        elif self.op == "XOR":
            output = left_out ^ right_out
        else:
            raise ValueError("invalid state")
        self.output = output
        return output

    def get_ancestors(self, gates_by_id: dict[str, LogicGate]) -> Iterator[str]:
        if self.left is not None:
            yield self.left
            yield from gates_by_id[self.left].get_ancestors(gates_by_id)
        if self.right is not None:
            yield self.right
            yield from gates_by_id[self.right].get_ancestors(gates_by_id)

    def reset(self):
        self.output = None


RULE_REGEX = re.compile(r"([a-z0-9]+) ([A-Z]+) ([a-z0-9]+) -> ([a-z0-9]+)")


def main():
    with open(sys.argv[1]) as f:
        initial_states_str, rules_str = f.read().split("\n\n")

    gates_by_id: dict[str, LogicGate] = {}
    for initial_state_line in initial_states_str.strip().split("\n"):
        label, value = initial_state_line.split(": ")
        gates_by_id[label] = LogicGate(id=label, op=None, output=int(value))

    for rule_line in rules_str.strip().split("\n"):
        match = RULE_REGEX.fullmatch(rule_line.strip())
        assert match
        left = match.group(1)
        op = match.group(2)
        right = match.group(3)
        label = match.group(4)
        gates_by_id[label] = LogicGate(id=label, op=op, left=left, right=right)

    max_index = 0
    part1_output = 0
    for label, gate in gates_by_id.items():
        if label.startswith("z"):
            index = int(label[1:])
            max_index = max(index, max_index)
            part1_output |= gate.get_output(gates_by_id) << index

    print(part1_output)

    print("n gates:", len(gates_by_id))

    # part 2 - note use of big endian

    # swaps were determined manually by inspecting the graph output (see day24_graphviz.py)
    swaps = [("kwb", "z12"), ("tgr", "z24"), ("jqn", "cph"), ("z16", "qkf")]
    for label1, label2 in swaps:
        gate1 = gates_by_id[label1]
        gate2 = gates_by_id[label2]
        gates_by_id[label1] = LogicGate(
            id=label1, op=gate2.op, left=gate2.left, right=gate2.right
        )
        gates_by_id[label2] = LogicGate(
            id=label2, op=gate1.op, left=gate1.left, right=gate1.right
        )

    for gate in gates_by_id.values():
        if gate.op:
            gate.reset()

    x_bits = [
        gates_by_id[f"x{index:02d}"].get_output(gates_by_id)
        for index in range(max_index - 1, -1, -1)
    ]
    y_bits = [
        gates_by_id[f"y{index:02d}"].get_output(gates_by_id)
        for index in range(max_index - 1, -1, -1)
    ]
    z_bits = [
        gates_by_id[f"z{index:02d}"].get_output(gates_by_id)
        for index in range(max_index, -1, -1)
    ]
    x_bits_str = "".join(str(b) for b in x_bits)
    y_bits_str = "".join(str(b) for b in y_bits)
    z_bits_str = "".join(str(b) for b in z_bits)
    print("ACTUAL")
    print(" " + x_bits_str)
    print(" " + y_bits_str)
    print(z_bits_str)

    x_val = int(x_bits_str, 2)
    y_val = int(y_bits_str, 2)
    expected_z_val = x_val + y_val
    expected_z_bits_str = f"{expected_z_val:b}"
    print("\nEXPECTED")
    print(" " + x_bits_str)
    print(" " + y_bits_str)
    print(expected_z_bits_str)

    if z_bits_str == expected_z_bits_str:
        print(",".join(sorted(s for swap in swaps for s in swap)))
    else:
        print("Not the right swaps!")


if __name__ == "__main__":
    main()
