from __future__ import annotations

import sys
from dataclasses import dataclass, field


@dataclass
class Node:
    id: str
    edges: set[str] = field(init=False, default_factory=set)

    def add_edge(self, other: Node):
        self.edges.add(other.id)
        other.edges.add(self.id)

    def has_edge(self, other_id: str):
        return other_id in self.edges

    def get_cliques(self, nodes: dict[str, Node], size=3) -> list[frozenset[str]]:
        if len(self.edges) < (size - 1):
            return []
        prev_cliques = [frozenset([edge_id]) for edge_id in self.edges]
        next_cliques = []
        for size in range(3, size + 1):
            next_cliques = []
            for smaller_clique_ids in prev_cliques:
                for neighbor_id in self.edges - smaller_clique_ids:
                    neighbor = nodes[neighbor_id]
                    if all(
                        neighbor.has_edge(clique_id) for clique_id in smaller_clique_ids
                    ):
                        next_cliques.append(smaller_clique_ids | {neighbor_id})
            prev_cliques = next_cliques
        return [clique | {self.id} for clique in next_cliques]


@dataclass
class Graph:
    nodes: dict[str, Node] = field(init=False, default_factory=dict)

    def get_or_add_node(self, id: str):
        if id not in self.nodes:
            self.nodes[id] = Node(id)
        return self.nodes[id]

    def get_maximum_clique(self):
        node_ids = sorted(self.nodes.keys())
        curr_cliques = {
            (node_id, edge_id)
            for node_id in node_ids
            for edge_id in self.nodes[node_id].edges
            if node_id < edge_id
        }
        size = 2
        while True:
            next_cliques = set()
            for first_node_id, *other_node_ids in curr_cliques:
                first_node = self.nodes[first_node_id]
                for neighbor_id in first_node.edges - set(other_node_ids):
                    neighbor = self.nodes[neighbor_id]
                    if all(
                        neighbor.has_edge(clique_id) for clique_id in other_node_ids
                    ):
                        next_cliques.add(
                            tuple(sorted([first_node_id, neighbor_id, *other_node_ids]))
                        )

            if next_cliques:
                size += 1
                curr_cliques = next_cliques
                print(f"Found {len(next_cliques)} cliques of {size=}")
            else:
                return curr_cliques.pop()


def main():
    graph = Graph()
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            id1, id2 = line.strip().split("-")
            n1 = graph.get_or_add_node(id1)
            n2 = graph.get_or_add_node(id2)
            n1.add_edge(n2)

    # part 1
    relevant_cliques: set[set[str]] = set()
    for node in graph.nodes.values():
        if node.id.startswith("t"):
            relevant_cliques |= set(node.get_cliques(graph.nodes, size=3))

    print(len(relevant_cliques))
    max_clique = graph.get_maximum_clique()
    print(",".join(max_clique))


if __name__ == "__main__":
    main()
