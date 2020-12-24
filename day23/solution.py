import itertools
import sys


class Node:
    def __init__(self, label):
        self.next = None
        self.prev = None
        self.label: int = label

    def set_next(self, next_node):
        self.next = next_node
        next_node.prev = self

    def __repr__(self):
        return f'Node(label={self.label})'


def main():
    with open(sys.argv[1]) as f:
        initial_input = [int(c) for c in f.read().strip()]

    part1(initial_input)
    part2(initial_input)


def part1(initial_input):
    first = Node(initial_input[0])
    current = first
    indexed_nodes = {initial_input[0]: first}
    for v in initial_input[1:]:
        node = Node(v)
        indexed_nodes[v] = node
        current.set_next(node)
        current = node
    current.set_next(first)

    current = first
    for i in range(100):
        current = iterate(current, indexed_nodes, 9)

    print(get_output(indexed_nodes[1]))


def part2(initial_input):
    max_val = max(initial_input)
    extended_input = itertools.chain(
        initial_input[1:],
        range(max_val + 1, 1_000_001))
    first = Node(initial_input[0])
    current = first
    indexed_nodes = {initial_input[0]: first}
    for v in extended_input:
        node = Node(v)
        indexed_nodes[v] = node
        current.set_next(node)
        current = node
    current.set_next(first)

    current = first
    for i in range(10_000_000):
        current = iterate(current, indexed_nodes, 1_000_000)
        if i % 100_000 == 0:
            print('iteration', i)

    next_cup = indexed_nodes[1].next
    next_next_cup = next_cup.next
    print(next_cup.label * next_next_cup.label)


def get_output(node1):
    current = node1.next
    labels = [current.label]
    while True:
        next_node = current.next
        if next_node == node1:
            break
        labels.append(next_node.label)
        current = next_node
    return ''.join(str(label) for label in labels)


def iterate(current, indexed_nodes, max_val):
    first_removed = current.next
    second_removed = first_removed.next
    third_removed = second_removed.next
    removed_cups = {first_removed, second_removed, third_removed}
    current.set_next(third_removed.next)

    current_label = current.label
    while True:
        new_label = current_label - 1 if current_label > 1 else max_val
        destination = indexed_nodes[new_label]
        current_label = new_label
        if destination not in removed_cups:
            break

    old_destination_next = destination.next
    destination.set_next(first_removed)
    third_removed.set_next(old_destination_next)
    return current.next


if __name__ == '__main__':
    main()
