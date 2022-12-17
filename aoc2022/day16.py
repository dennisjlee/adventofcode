from __future__ import annotations
import re
import sys
from collections import deque, defaultdict
from heapq import heappop, heappush
from typing import NamedTuple, Optional


class Node(NamedTuple):
    name: str
    flow_rate: int
    edges: dict[str, int]


PARSE_PATTERN = re.compile(r'Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*?)$', re.MULTILINE)


class State(NamedTuple):
    time_remaining: int
    score: int
    curr_name: str
    visited: frozenset[str]


def find_paths_to_relevant_nodes(graph: dict[str, Node], start: Node) -> dict[str, int]:
    # run a version of dijkstra on the base graph to construct edges for the meta-graph
    visited: set[str] = set()
    tentative_distance = defaultdict(lambda: sys.maxsize)
    tentative_distance[start.name] = 0
    heap = [(0, start)]
    while heap:
        dist, curr = heappop(heap)

        visited.add(curr.name)

        for neighbor_name, cost in curr.edges.items():
            if neighbor_name not in visited:
                neighbor = graph[neighbor_name]
                if dist + cost < tentative_distance[neighbor_name]:
                    tentative_distance[neighbor_name] = dist + cost
                    heappush(heap, (tentative_distance[neighbor_name], neighbor))

    # edge cost in the metagraph includes 1 for opening the valve after arriving at a node
    return {
        name: dist + 1 for name, dist in tentative_distance.items()
        if name != start.name and graph[name].flow_rate > 0
    }


def main():
    graph: dict[str, Node] = {}
    with open(sys.argv[1]) as f:
        contents = f.read()
        for match in PARSE_PATTERN.finditer(contents):
            name = match.group(1)
            flow_rate = int(match.group(2))
            node = Node(name, flow_rate, {})
            graph[name] = node

        for match in PARSE_PATTERN.finditer(contents):
            name = match.group(1)
            neighbor_names = match.group(3).split(', ')
            node = graph[name]
            node.edges.update({nn: 1 for nn in neighbor_names})

    # Construct meta-graph where only AA and nodes with non-zero flow rate are represented,
    # and every node is connected to every other with weighted edges. Each edge weight between
    # nodes N1 and N2 is defined as the shortest path between N1 and N2 in the base graph.
    metagraph: dict[str, Node] = {}
    for node in graph.values():
        if node.flow_rate > 0 or node.name == 'AA':
            new_edges = find_paths_to_relevant_nodes(graph, node)
            metanode = Node(node.name, node.flow_rate, new_edges)
            metagraph[metanode.name] = metanode

    part1(metagraph)
    print()
    part2(metagraph)


def part1(metagraph: dict[str, Node]):
    # part 1 - one person for 30 min
    queue = deque([State(30, 0, 'AA', frozenset({'AA'}))])
    best_score = 0
    step = 0
    while queue:
        step += 1
        state = queue.popleft()
        if step % 100_000 == 0:
            print(f'step {step}, # states {len(queue)}, current state time remaining {state.time_remaining}')
        found_successor = False
        curr = metagraph[state.curr_name]
        for neighbor_name, cost in curr.edges.items():
            if neighbor_name not in state.visited and cost <= state.time_remaining:
                found_successor = True
                neighbor = metagraph[neighbor_name]
                new_time_remaining = state.time_remaining - cost
                new_score = state.score + new_time_remaining * neighbor.flow_rate
                queue.append(State(new_time_remaining,
                                   new_score,
                                   neighbor_name,
                                   state.visited.union({neighbor_name})))
        if not found_successor:
            # we have nowhere else to go or no time remaining - run out the clock and check the score
            if state.score > best_score:
                best_score = state.score
    print(best_score)


class Visitor(NamedTuple):
    next_node_name: str
    time_remaining: int


class State2(NamedTuple):
    score: int
    time_remaining: int
    visitor1: Visitor
    visitor2: Visitor
    visited: frozenset[str]

    def lower_bound(self, metagraph: dict[str, Node]):
        return self.score - sum(node.flow_rate * (self.time_remaining - 2)
                                for name, node in metagraph.items()
                                if name not in self.visited)


def part2(metagraph: dict[str, Node]):
    # part 2 - one person and one elephant for 26 min
    heap = [State2(0, 26, Visitor('AA', 0), Visitor('AA', 0), frozenset({'AA'}))]
    best_score = 0
    step = 0
    # in this version, we track the score as a negative number to make it easier to use
    # heapq
    while heap:
        step += 1
        state = heappop(heap)
        if step % 100_000 == 0:
            print(f'step {step}, # states {len(heap)}, current state time remaining {state.time_remaining}, best score {best_score}')

        if state.lower_bound(metagraph) > best_score:
            continue

        curr1 = metagraph[state.visitor1.next_node_name]
        curr2 = metagraph[state.visitor2.next_node_name]

        options1: list[Optional[tuple[str, int]]] = [
            (neighbor_name1, cost1) for neighbor_name1, cost1 in curr1.edges.items()
            if neighbor_name1 not in state.visited and cost1 <= state.time_remaining
        ] if state.visitor1.time_remaining == 0 else []
        options2: list[Optional[tuple[str, int]]] = [
            (neighbor_name2, cost2) for neighbor_name2, cost2 in curr2.edges.items()
            if neighbor_name2 not in state.visited and cost2 <= state.time_remaining
        ] if state.visitor2.time_remaining == 0 else []

        if options1 and options2:
            for neighbor_name1, cost1 in options1:
                for neighbor_name2, cost2 in options2:
                    if neighbor_name2 == neighbor_name1:
                        continue
                    time_step = max(1, min(cost1, cost2))
                    new_visitor1 = Visitor(neighbor_name1, cost1 - time_step)
                    new_visitor2 = Visitor(neighbor_name2, cost2 - time_step)
                    neighbor1 = metagraph[neighbor_name1]
                    neighbor2 = metagraph[neighbor_name2]
                    time_remaining = state.time_remaining
                    new_score = (
                        state.score -
                        (time_remaining - cost1) * neighbor1.flow_rate -
                        (time_remaining - cost2) * neighbor2.flow_rate
                    )

                    new_state = State2(new_score, time_remaining - time_step, new_visitor1, new_visitor2,
                                       state.visited.union({neighbor_name1, neighbor_name2}))
                    if new_state.lower_bound(metagraph) < best_score:
                        heappush(heap, new_state)
        elif options1:
            for neighbor_name1, cost1 in options1:
                time_step = max(1, min(cost1, state.visitor2.time_remaining))
                new_visitor1 = Visitor(neighbor_name1, cost1 - time_step)
                new_visitor2 = Visitor(state.visitor2.next_node_name, state.visitor2.time_remaining - time_step)
                neighbor1 = metagraph[neighbor_name1]
                time_remaining = state.time_remaining
                new_score = state.score - (time_remaining - cost1) * neighbor1.flow_rate

                new_state = State2(new_score, time_remaining - time_step, new_visitor1, new_visitor2,
                                   state.visited.union({neighbor_name1}))
                if new_state.lower_bound(metagraph) < best_score:
                    heappush(heap, new_state)
        elif options2:
            for neighbor_name2, cost2 in options2:
                time_step = max(1, min(cost2, state.visitor1.time_remaining))
                new_visitor1 = Visitor(state.visitor1.next_node_name, state.visitor1.time_remaining - time_step)
                new_visitor2 = Visitor(neighbor_name2, cost2 - time_step)
                neighbor2 = metagraph[neighbor_name2]
                time_remaining = state.time_remaining
                new_score = state.score - (time_remaining - cost2) * neighbor2.flow_rate

                new_state = State2(new_score, time_remaining - time_step, new_visitor1, new_visitor2,
                                   state.visited.union({neighbor_name2}))
                if new_state.lower_bound(metagraph) < best_score:
                    heappush(heap, new_state)
        elif state.time_remaining > 0:
            time_step = max(1, min(state.visitor1.time_remaining, state.visitor2.time_remaining))
            new_visitor1 = Visitor(state.visitor1.next_node_name, state.visitor1.time_remaining - time_step)
            new_visitor2 = Visitor(state.visitor2.next_node_name, state.visitor2.time_remaining - time_step)
            new_state = State2(state.score, state.time_remaining - time_step, new_visitor1, new_visitor2, state.visited)
            if new_state.lower_bound(metagraph) < best_score:
                heappush(heap, new_state)
        else:
            # we have no time remaining - run out the clock and check the score
            if state.score < best_score:
                best_score = state.score
    print(-best_score)


if __name__ == '__main__':
    main()
