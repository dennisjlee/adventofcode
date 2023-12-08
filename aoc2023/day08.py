from __future__ import annotations

import math
import re
from itertools import cycle
import sys


NODE_REGEX = re.compile(r'(\w+) = \((\w+), (\w+)\)')


class Node:
    label: str
    left: str
    right: str

    def __init__(self, line: str):
        match = NODE_REGEX.match(line)
        self.label = match.group(1)
        self.left = match.group(2)
        self.right = match.group(3)

    def __repr__(self):
        return f'Node({self.label}, l={self.left}, r={self.right})'


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    moves = lines[0].strip()

    nodes_by_label: dict[str, Node] = {}
    for line in lines[2:]:
        node = Node(line)
        nodes_by_label[node.label] = node

    print(nodes_by_label)

    # part 1
    curr = nodes_by_label['AAA']
    for i, move in enumerate(cycle(moves)):
        if curr.label == 'ZZZ':
            print(i)
            break
        next_label = curr.left if move == 'L' else curr.right
        curr = nodes_by_label[next_label]

    # part 2
    curr_nodes = [v for k, v in nodes_by_label.items() if k.endswith('A')]
    z_indexes_by_label = {}
    for start in curr_nodes:
        z_indexes = z_indexes_by_label.setdefault(start.label, {})
        curr = start
        for i, move in enumerate(cycle(moves)):
            if curr.label.endswith('Z'):
                if curr.label in z_indexes:
                    print('label', start.label, 'looped back to z at', i, 'z indexes', z_indexes)
                    break
                z_indexes[curr.label] = i

            next_label = curr.left if move == 'L' else curr.right
            curr = nodes_by_label[next_label]

            if curr is start:
                print('label', start.label, 'looped back to itself at', i, 'z indexes', z_indexes)
                break
    print(z_indexes_by_label)
    print(math.lcm(*[list(z_indexes.values())[0] for z_indexes in z_indexes_by_label.values()]))


if __name__ == '__main__':
    main()
