from __future__ import annotations

import functools
import heapq
import math
import time
from collections import deque, defaultdict
import itertools
import re
import sys
import typing
from typing import Optional
from copy import copy, deepcopy

SIMPLE_INPUT = """
#############
#...........#
###A#B#A#D###
###B#C#C#D###
  #########
"""

EXAMPLE_INPUT = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

PART1_INPUT = """
#############
#...........#
###C#A#B#D###
  #C#A#D#B#
  #########
"""

PART2_INPUT = """
#############
#...........#
###C#A#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #C#A#D#B#
  #########
"""

ROOM_NAMES_BY_X = {
    3: 'A',
    5: 'B',
    7: 'C',
    9: 'D'
}

X_BY_ROOM_NAME = {
    v: k for k, v in ROOM_NAMES_BY_X.items()
}

STEP_COSTS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}


class Edge(typing.NamedTuple):
    node_x: int
    distance: int


class Move(typing.NamedTuple):
    dest_x: int
    distance: int


class Node:
    x: int
    id: str
    capacity: int
    occupants: list[str]
    edges: list[Edge]

    def __init__(self, x: int, id: str, capacity: int):
        self.x = x
        self.id = id
        self.capacity = capacity
        self.occupants = []
        self.edges = []

    def connect(self, other: Node, distance: int):
        self.edges.append(Edge(other.x, distance))
        other.edges.append(Edge(self.x, distance))

    def push_occupant(self, occupant: str) -> int:
        self.occupants.append(occupant)
        internal_distance = self.capacity - len(self.occupants)
        assert internal_distance >= 0
        return internal_distance

    def pop_occupant(self) -> tuple[str, int]:
        internal_distance = self.capacity - len(self.occupants)
        return self.occupants.pop(), internal_distance

    @property
    def occupied(self):
        return len(self.occupants) == self.capacity

    def can_accept(self, letter: str):
        raise NotImplemented

    def possible_moves(self, state: State) -> typing.Iterable[Move]:
        raise NotImplemented

    def clone(self):
        raise NotImplemented


class Room(Node):
    letter: str

    def __init__(self, x: int, id: str, capacity: int, letter: str):
        super().__init__(x, id, capacity)
        self.letter = letter

    def is_complete(self):
        return len(self.occupants) == self.capacity and all(o == self.letter for o in self.occupants)

    def possible_moves(self, state: State) -> typing.Iterable[Move]:
        if not self.occupants:
            return
        if all(o == self.letter for o in self.occupants):
            return

        letter_to_move = self.occupants[-1]
        queue = deque([(self.x, 0)])
        distances = defaultdict(lambda: 1000)
        while queue:
            node_x, distance = queue.popleft()
            node = state.nodes[node_x]

            # Prefer moving straight into the appropriate room before considering moves to the hallway
            if node is not self and isinstance(node, Room):
                yield Move(node_x, distance)
                return

            if distance < distances[node.x]:
                distances[node.x] = distance
            else:
                continue

            for edge in node.edges:
                new_distance = distance + edge.distance
                if edge.node_x not in distances and state.nodes[edge.node_x].can_accept(letter_to_move):
                    queue.append((edge.node_x, new_distance))

        for node_x, distance in distances.items():
            if node_x != self.x:
                yield Move(node_x, distance)

    def can_accept(self, letter: str):
        return letter == self.letter and not self.occupied and all(o == self.letter for o in self.occupants)

    def __repr__(self):
        return f'Room(x={self.x}, capacity={self.capacity}, letter={self.letter}, occupants=[{",".join(self.occupants)}])'

    def clone(self):
        clone = Room(self.x, self.id, self.capacity, self.letter)
        clone.edges = self.edges
        clone.occupants[:] = self.occupants
        return clone


class Hallway(Node):
    def __init__(self, x: int, id: str):
        super().__init__(x, id, 1)

    def possible_moves(self, state: State) -> typing.Iterable[Move]:
        if not self.occupants:
            return

        letter_to_move = self.occupants[0]
        dest_x = X_BY_ROOM_NAME[letter_to_move]
        if self.x < dest_x:
            for x in range(self.x + 1, dest_x):
                if x not in ROOM_NAMES_BY_X and state.nodes[x].occupied:
                    return
        else:
            for x in range(dest_x + 1, self.x):
                if x not in ROOM_NAMES_BY_X and state.nodes[x].occupied:
                    return

        if not state.nodes[dest_x].can_accept(letter_to_move):
            return

        yield Move(dest_x, abs(dest_x - self.x) + 1)

    def can_accept(self, letter: str):
        return not self.occupied

    def __repr__(self):
        return f'Hallway(x={self.x}, occupants=[{",".join(self.occupants)}])'

    def clone(self):
        clone = Hallway(self.x, self.id)
        clone.edges = self.edges
        clone.occupants[:] = self.occupants
        return clone


@functools.total_ordering
class State:
    nodes: list[Optional[Node]]
    energy_used: int

    def __init__(self, nodes: list[Optional[Node]], energy_used: int):
        self.nodes = nodes
        self.energy_used = energy_used

    def is_complete(self):
        return all(r.is_complete() for r in self.nodes if r and isinstance(r, Room))

    def __hash__(self):
        val = tuple(tuple(n.occupants) for n in self.nodes if n)
        return hash((self.energy_used, val))

    @functools.cached_property
    def heuristic(self):
        h = 0
        for x, node in enumerate(self.nodes):
            if x == 0:
                continue
            elif x in {3, 5, 7, 9}:
                if node.occupants:
                    current_height = len(node.occupants)
                    try:
                        non_matching_index = next(i for i, v in enumerate(node.occupants) if v != node.letter)
                        for j in range(non_matching_index, current_height):
                            letter = node.occupants[j]
                            dest_x = X_BY_ROOM_NAME[letter]
                            h += (current_height - j + 1 + abs(node.x - dest_x)) * STEP_COSTS[letter]
                            if j < current_height - 1:
                                # this amphipod is blocked, so give it an additional penalty
                                h += 3 * STEP_COSTS[letter]
                    except StopIteration:
                        # no non-matching indexes found
                        continue
            elif node.occupants:
                letter = node.occupants[0]
                dest_x = X_BY_ROOM_NAME[letter]
                h += (1 + abs(node.x - dest_x)) * STEP_COSTS[letter]
        return h

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __lt__(self, other):
        return (self.energy_used + self.heuristic) < (other.energy_used + other.heuristic)

    def __repr__(self):
        return f'State(energy_used={self.energy_used}, heuristic={self.heuristic})'

    def successor_states(self) -> typing.Iterable[State]:
        for n_x, node in enumerate(self.nodes):
            if n_x == 0:
                continue
            for move in node.possible_moves(self):
                new_nodes = copy(self.nodes)
                src = node.clone()
                new_nodes[n_x] = src
                dest = new_nodes[move.dest_x].clone()
                new_nodes[move.dest_x] = dest

                letter, src_internal_distance = src.pop_occupant()
                dest_internal_distance = dest.push_occupant(letter)
                move_energy = (move.distance + src_internal_distance + dest_internal_distance) * STEP_COSTS[letter]

                yield State(new_nodes, self.energy_used + move_energy)


class Amphipod:
    letter: str
    step_cost: int

    def __init__(self, letter: str):
        self.letter = letter
        self.step_cost = STEP_COSTS[letter]


def main():
    start = time.perf_counter()
    # part 1 solved w/ pen and paper lol - answer was 11536

    # print(find_best_solution1(SIMPLE_INPUT))
    # print(find_best_solution2(SIMPLE_INPUT))

    print(find_best_solution1(PART1_INPUT))
    # print(find_best_solution1(EXAMPLE_INPUT))

    # part 2
    print(find_best_solution1(PART2_INPUT))
    end = time.perf_counter()
    print(f'time: {end - start}s')


def find_best_solution1(raw_input: str):
    raw_lines = raw_input.strip().split('\n')
    initial_state = parse_nodes(raw_lines)
    return a_star_search(initial_state)


def find_best_solution2(raw_input: str):
    raw_lines = raw_input.strip().split('\n')
    initial_state = parse_nodes(raw_lines)

    best_solution = preferential_dfs(initial_state)
    return best_solution.energy_used


def preferential_dfs(state):
    if state.is_complete():
        return state

    successors = sorted(state.successor_states())
    best_solution = None
    for successor in successors:
        if best_solution and successor > best_solution:
            continue
        candidate_solution = preferential_dfs(successor)
        if candidate_solution:
            best_solution = candidate_solution if best_solution is None else min(best_solution, candidate_solution)
    return best_solution


def a_star_search(initial_state):
    heap = [initial_state]
    # state_results = {}
    counter = 0
    while heap:
        counter += 1
        state = heapq.heappop(heap)
        # if state in state_results and state.energy_used > state_results[state]:
        #     continue
        # state_results[state] = state.energy_used
        if counter % 1000 == 0:
            print(f'counter {counter}; queue length {len(heap)}; current state: {state}')
        if state.is_complete():
            print(f'found solution! counter {counter}; queue length {len(heap)}; current state: {state}')
            return state.energy_used

        num_successors = 0
        for new_state in state.successor_states():
            heapq.heappush(heap, new_state)
            num_successors += 1

        # print(f'added {num_successors} successor states')
    return math.inf

    # def execute_move(self, move: Move) -> tuple[int, Node, Node]:
    #     amphipod = self.pop_occupant()
    #     internal_distance = move.dest.push_occupant(amphipod)
    #     return (move.distance + internal_distance) * amphipod.step_cost


def parse_nodes(lines: list[str]):
    room_capacity = len(lines) - 3

    nodes: list[Optional[Node]] = [None] * 12
    for col_index, letter in ROOM_NAMES_BY_X.items():
        nodes[col_index] = Room(col_index, letter, room_capacity, letter)
        fill_room(lines, col_index, nodes[col_index])

    left1 = Hallway(1, 'L1')
    left2 = Hallway(2, 'L2')
    left1.connect(left2, 1)

    left2.connect(nodes[3], 2)
    ab = Hallway(4, 'AB')
    left2.connect(ab, 2)
    ab.connect(nodes[3], 2)
    ab.connect(nodes[5], 2)

    bc = Hallway(6, 'BC')
    bc.connect(ab, 2)
    bc.connect(nodes[5], 2)
    bc.connect(nodes[7], 2)

    cd = Hallway(8, 'CD')
    cd.connect(bc, 2)
    cd.connect(nodes[7], 2)
    cd.connect(nodes[9], 2)

    right2 = Hallway(10, 'R2')
    right2.connect(cd, 2)
    right2.connect(nodes[9], 2)

    right1 = Hallway(11, 'R1')
    right1.connect(right2, 1)

    for h in (left1, left2, ab, bc, cd, right2, right1):
        nodes[h.x] = h
    return State(nodes, 0)


def fill_room(lines: list[str], col_index: int, room: Node):
    for y in range(len(lines) - 2, 1, -1):
        letter = lines[y][col_index]
        assert letter in 'ABCD'
        room.push_occupant(letter)


if __name__ == '__main__':
    main()
