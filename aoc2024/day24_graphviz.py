from __future__ import annotations

import sys
from day24 import LogicGate, RULE_REGEX


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

    # determined manually by inspecting the graph output (by piping the output of this
    # script to `dot -Tsvg > aoc2024/inputs/day24.svg`)
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

    print("strict digraph {")
    print("rankdir=LR;")

    # print x/y nodes first in sorted order, in the first rank
    for gate_id, gate in gates_by_id.items():
        if not gate.op:
            print(gate_id)
    print(
        f"{{ rank=min; {' '.join(gate.id + ';' for gate in gates_by_id.values() if gate.op is None)} }}"
    )

    sorted_input_ids = [
        t[1]
        for t in sorted(
            (int(gate.id[1:]), gate.id) for gate in gates_by_id.values() if not gate.op
        )
    ]

    # https://stackoverflow.com/a/64007295
    print(f"""
    {{
        rank = same;
        rankdir = TB;
        // Here we enforce the desired order with "invisible" edges and arrowheads
        edge [style=invis];
        {' -> '.join(sorted_input_ids)};
    }}
    """)

    for gate_id, gate in sorted(gates_by_id.items()):
        if gate.op and gate.left and gate.right:
            if gate_id.startswith("z"):
                print(f'{gate_id} [style="filled"]')
            else:
                print(gate_id)
            operation_node_label = f"{gate.left}_{gate.right}_{gate.op}"
            print(f'{operation_node_label} [label="{gate.op}"]')
            print(f"{gate.left} -> {operation_node_label}")
            print(f"{gate.right} -> {operation_node_label}")
            print(f"{operation_node_label} -> {gate_id}")
    # print(
    #     f"{{ rank=max; {' '.join(label + ';' for label in gates_by_id.keys() if label.startswith('z'))} }}"
    # )

    print("}")


if __name__ == "__main__":
    main()
