from __future__ import annotations
import re
import sys
from collections import deque
from typing import NamedTuple, Optional, Iterable
from copy import deepcopy


class Node(NamedTuple):
    name: str
    flow_rate: int
    edges: dict[str, int]


PARSE_PATTERN = re.compile(r'Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*?)$', re.MULTILINE)


class State(NamedTuple):
    time: int
    pressure_released: int
    node_name: str
    open_valve_names: frozenset[str]
    nodes_by_name: dict[str, Node]

    def can_open(self) -> bool:
        return self.node_name not in self.open_valve_names and \
            self.nodes_by_name[self.node_name].flow_rate > 0

    def iterate_open_valve(self):
        return State(self.time + 1,
                     self.next_pressure_released(),
                     self.node_name,
                     self.open_valve_names | {self.node_name},
                     self.nodes_by_name)

    def neighbors(self) -> list[Node]:
        return self.nodes_by_name[self.node_name].neighbors

    def iterate_move_to(self, new_node: Node):
        return State(self.time + 1,
                     self.next_pressure_released(),
                     new_node.name,
                     self.open_valve_names,
                     self.nodes_by_name)

    def next_pressure_released(self):
        return self.pressure_released + self.current_flow()

    def current_flow(self) -> int:
        return sum(self.nodes_by_name[name].flow_rate for name in self.open_valve_names)


def find_paths_to_relevant_nodes(nodes_by_name: dict[str, Node], node: Node) -> dict[str, int]:
    # run a version of dijkstra on the base graph to construct edges for the meta-graph
    # TODO
    return {}


def main():
    nodes_by_name = {}
    with open(sys.argv[1]) as f:
        contents = f.read()
        for match in PARSE_PATTERN.finditer(contents):
            name = match.group(1)
            flow_rate = int(match.group(2))
            node = Node(name, flow_rate, {})
            nodes_by_name[name] = node

        for match in PARSE_PATTERN.finditer(contents):
            name = match.group(1)
            neighbor_names = match.group(3).split(', ')
            node = nodes_by_name[name]
            node.edges.update({nn: 1 for nn in neighbor_names})

    # Construct meta-graph where only AA and nodes with non-zero flow rate are represented,
    # and every node is connected to every other with weighted edges. Each edge weight between
    # nodes N1 and N2 is defined as the shortest path between N1 and N2 in the base graph.



    # print(nodes_by_name)
    # states = deque([State(0, 0, 'AA', frozenset(), nodes_by_name)])
    # best_pressure_released = 0
    # step = 0
    # while states:
    #     step += 1
    #     state = states.popleft()
    #     if step % 1000 == 0:
    #         print(f'step {step}, # states {len(states)}, current state time {state.time}')
    #     if state.time >= 29:
    #         best_pressure_released = max(best_pressure_released, state.next_pressure_released())
    #         continue
    #     if state.can_open():
    #         states.append(state.iterate_open_valve())
    #     for neighbor in state.neighbors():
    #         states.append(state.iterate_move_to(neighbor))
    #
    # print(best_pressure_released)


if __name__ == '__main__':
    main()
