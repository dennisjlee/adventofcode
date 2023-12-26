from __future__ import annotations

import sys
from collections import defaultdict
from typing import NamedTuple


class Node(NamedTuple):
    label: str
    count: int
    edges: dict[str, int]

    def add_edge(self, other: Node, weight=1):
        self.edges[other.label] = weight
        other.edges[self.label] = weight

    def __repr__(self):
        edge_strings = [
            f'{label}:{weight}' for label, weight in self.edges.items()
        ]
        return f'Component({self.label}, count={self.count}, edges=[{", ".join(edge_strings)}])'


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    nodes_by_label: dict[str, Node] = {}
    for line in lines:
        left, right = line.strip().split(': ')
        left_component = nodes_by_label.setdefault(left, Node(left, 1, defaultdict(int)))
        for label in right.split():
            right_component = nodes_by_label.setdefault(label, Node(label, 1, defaultdict(int)))
            left_component.add_edge(right_component)

    group1_size, group2_size = minimum_cut(nodes_by_label)
    print(group1_size, group2_size, group1_size * group2_size)


# Implement Stoer–Wagner algorithm: https://dl.acm.org/doi/pdf/10.1145/263867.263872

def combine(s_label: str, t_label: str, nodes_by_label: dict[str, Node]):
    s = nodes_by_label[s_label]
    t = nodes_by_label[t_label]
    st = Node(f'{s_label}-{t_label}', s.count + t.count, defaultdict(int))
    nodes_by_label[st.label] = st
    for merged in (s, t):
        for other_label, weight in merged.edges.items():
            if other_label != s_label and other_label != t_label:
                st.edges[other_label] += weight
                other = nodes_by_label[other_label]
                del other.edges[merged.label]
                other.edges[st.label] += weight
        del nodes_by_label[merged.label]


def minimum_cut_phase(nodes_by_label: dict[str, Node], a: Node) -> tuple[int, int, int]:
    """
    MINIMUMCUTPHASE(G, w, a)
    A := {a}
    while A != V
        add to A the most tightly connected vertex
        store the cut-of-the-phase and shrink G by merging the two vertices added last
    """

    visited_labels = {a.label}
    size = len(nodes_by_label)
    s = a.label
    t = ''
    weights_from_visited = {label: a.edges.get(label, 0) for label in nodes_by_label}
    candidate_labels = set(nodes_by_label.keys()) - visited_labels
    for i in range(1, size):
        # TODO: could optimize this with a priority queue but we'd need to keep modifying weights within it
        max_label = max(candidate_labels, key=weights_from_visited.get)
        if i == size - 2:
            s = max_label
        elif i == size - 1:
            t = max_label
        visited_labels.add(max_label)
        candidate_labels.remove(max_label)
        for label, weight in nodes_by_label[max_label].edges.items():
            weights_from_visited[label] += weight

    t_node = nodes_by_label[t]
    cut_of_phase = sum(t_node.edges.values())
    combine(s, t, nodes_by_label)
    total_count = sum(n.count for n in nodes_by_label.values())
    t_count = t_node.count
    return cut_of_phase, t_count, total_count - t_count


def minimum_cut(nodes_by_label: dict[str, Node]):
    """
    MINIMUMCUT(G, w, a)
    while |V| > 1
        MINIMUMCUTPHASE(G, w, a)
        if the cut-of-the-phase is lighter than the current minimum cut
        then store the cut-of-the-phase as the current minimum cut

    Modification for this problem - return as soon as we find a cut of size 3.
    """
    a = next(iter(nodes_by_label.values()))
    while len(nodes_by_label) > 1:
        cut_of_phase, group1_size, group2_size = minimum_cut_phase(nodes_by_label, a)
        if len(nodes_by_label) % 10 == 0:
            print(len(nodes_by_label))
        if cut_of_phase == 3:
            return group1_size, group2_size
    return None, None


if __name__ == '__main__':
    main()
