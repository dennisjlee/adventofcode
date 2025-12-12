from __future__ import annotations

import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import NamedTuple


class Node(NamedTuple):
    label: str
    outputs: list[str]

    @staticmethod
    def parse(line: str) -> Node:
        label, outputs_str = line.strip().split(': ')
        return Node(label, outputs_str.split())


def main() -> None:
    with Path(sys.argv[1]).open() as f:
        nodes = [Node.parse(line) for line in f.readlines()]
    
    nodes_lookup = {node.label: node for node in nodes}
    nodes_lookup["out"] = Node("out", [])
    print(count_paths(nodes_lookup, "you", "out"))

    print(
        (
        count_paths_dynamic(nodes_lookup, "svr", "dac") *
        count_paths_dynamic(nodes_lookup, "dac", "fft") *
        count_paths_dynamic(nodes_lookup, "fft", "out")
        ) +
        (
        count_paths_dynamic(nodes_lookup, "svr", "fft") *
        count_paths_dynamic(nodes_lookup, "fft", "dac") *
        count_paths_dynamic(nodes_lookup, "dac", "out")
        )
    )


def count_paths(nodes_lookup: dict[str, Node], source: str, target: str) -> int:
    count = 0
    q: deque[list[str]] = deque([[source]])
    while q:
        path = q.popleft()
        cur_label = path[-1]
        if cur_label == "out":
            count += 1
        else:
            node = nodes_lookup[cur_label]
            for next_label in node.outputs:
                if next_label in path:
                    print("warning: cycle detected")
                else:
                    q.append([*path, next_label])
    return count


def count_paths_dynamic(nodes_lookup: dict[str, Node], source: str, target: str) -> int:
    predecessors: dict[str, set[str]] = defaultdict(set)
    visited: set[str] = set()
    q: deque[str] = deque([source])
    i = 0
    while q:
        i += 1
        curr = q.popleft()
        if curr in visited or curr == target:
            continue
        visited.add(curr)
        for neighbor in nodes_lookup[curr].outputs:
            predecessors[neighbor].add(curr)
            if neighbor not in visited:
                q.append(neighbor)
    
    path_counts: dict[str, int] = {}
    path_counts[source] = 1

    nodes_to_process = {n for n in nodes_lookup.keys() if n != source}
    while nodes_to_process:
        for n in nodes_to_process:
            if all(p in path_counts for p in predecessors[n]):
                path_counts[n] = sum(path_counts[p] for p in predecessors[n])
                nodes_to_process.remove(n)
                break
    
    return path_counts[target]


if __name__ == "__main__":
    main()