from __future__ import annotations

import math
from collections import deque, defaultdict
import itertools
import re
import sys
import typing
from copy import copy, deepcopy

SIMPLE_INPUT = """
#############
#...........#
###B#A#C#D###
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

STEP_COSTS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}


class Edge(typing.NamedTuple):
    node_id: str
    distance: int


class Move(typing.NamedTuple):
    dest_id: id
    distance: int


class Node:
    id: str
    capacity: int
    occupants: deque[str]
    edges: list[Edge]
    allowed_types: frozenset[str]

    def __init__(self, id: str, capacity: int):
        self.id = id
        self.capacity = capacity
        self.occupants = deque()
        self.edges = []

    def connect(self, other: Node, distance: int):
        self.edges.append(Edge(other.id, distance))
        other.edges.append(Edge(self.id, distance))

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


class Room(Node):
    def __init__(self, id: str, capacity: int, letter: str):
        super().__init__(id, capacity)
        self.letter = letter

    def is_complete(self):
        return len(self.occupants) == self.capacity and all(o == self.letter for o in self.occupants)

    def possible_moves(self, state: State) -> typing.Iterable[Move]:
        if not self.occupants:
            return
        if all(o == self.letter for o in self.occupants):
            return

        letter_to_move = self.occupants[-1]
        queue = deque([(self.id, 0)])
        distances = defaultdict(lambda: 1000)
        while queue:
            node_id, distance = queue.popleft()
            node = state.nodes[node_id]

            # Prefer moving straight into the appropriate room before considering moves to the hallway
            if node is not self and isinstance(node, Room):
                yield Move(node_id, distance)
                return

            if distance < distances[node.id]:
                distances[node.id] = distance
            else:
                continue

            for edge in node.edges:
                new_distance = distance + edge.distance
                if edge.node_id not in distances and state.nodes[edge.node_id].can_accept(letter_to_move):
                    queue.append((edge.node_id, new_distance))

        for node_id, distance in distances.items():
            if node_id != self.id:
                yield Move(node_id, distance)

    def can_accept(self, letter: str):
        return letter == self.letter and not self.occupied and all(o == self.letter for o in self.occupants)

    def __repr__(self):
        return f'Room(capacity={self.capacity}, letter={self.letter}, occupants=[{",".join(self.occupants)}])'


class Hallway(Node):
    def __init__(self, id: str):
        super().__init__(id, 1)

    def possible_moves(self, state: State) -> typing.Iterable[Move]:
        if not self.occupants:
            return

        letter_to_move = self.occupants[0]
        queue = deque([(self.id, 0)])
        distances = defaultdict(lambda: 1000)
        while queue:
            node_id, distance = queue.popleft()
            node = state.nodes[node_id]
            # Our goal is a move into the appropriate room, so if we find a path to it, take it
            if isinstance(node, Room):
                yield Move(node_id, distance)
                return

            if distance < distances[node.id]:
                distances[node.id] = distance
            else:
                continue
            if node.occupied:
                continue

            for edge in node.edges:
                new_distance = distance + edge.distance
                if edge.node_id not in distances and state.nodes[edge.node_id].can_accept(letter_to_move):
                    queue.append((edge.node_id, new_distance))

    def can_accept(self, letter: str):
        return not self.occupied

    def __repr__(self):
        return f'Hallway(occupants=[{",".join(self.occupants)}])'


class State(typing.NamedTuple):
    nodes: dict[str, Node]
    energy_used: int

    def is_complete(self):
        return all(r.is_complete() for r in self.nodes.values() if isinstance(r, Room))

    def __hash__(self):
        val = tuple(tuple(n.occupants) for _, n in sorted(self.nodes.items()))
        return hash(val)


class Amphipod:
    letter: str
    step_cost: int

    def __init__(self, letter: str):
        self.letter = letter
        self.step_cost = STEP_COSTS[letter]


def main():
    # part 1 solved w/ pen and paper lol - answer was 11536
    print(find_best_solution(SIMPLE_INPUT))

    # print(find_best_solution(PART1_INPUT))

    # part 2
    # print(find_best_solution(PART2_INPUT))


def find_best_solution(raw_input: str):
    raw_lines = raw_input.strip().split('\n')
    initial_state = parse_nodes(raw_lines)

    queue = deque([initial_state])
    state_results = {}
    best_result = math.inf
    # TODO: this just isn't working - the branching factor seems to be too high. Probably need to try to use A* search
    while queue:
        state = queue.popleft()
        if state in state_results and state.energy_used > state_results[state]:
            continue
        state_results[state] = state.energy_used
        print('queue length', len(queue), '; energy', state.energy_used)
        if state.is_complete():
            best_result = min(best_result, state.energy_used)
            continue

        num_successors = 0
        for n_id, node in state.nodes.items():
            possible_moves = list(node.possible_moves(state))
            x = 1
            for move in possible_moves:
                new_nodes = copy(state.nodes)
                src = deepcopy(node)
                new_nodes[n_id] = src
                dest = deepcopy(new_nodes[move.dest_id])
                new_nodes[move.dest_id] = dest

                letter, src_internal_distance = src.pop_occupant()
                dest_internal_distance = dest.push_occupant(letter)
                move_energy = (move.distance + src_internal_distance + dest_internal_distance) * STEP_COSTS[letter]

                new_state = State(new_nodes, state.energy_used + move_energy)
                queue.append(new_state)
                num_successors += 1

        print(f'added {num_successors} successor states')

    return best_result

    # def execute_move(self, move: Move) -> tuple[int, Node, Node]:
    #     amphipod = self.pop_occupant()
    #     internal_distance = move.dest.push_occupant(amphipod)
    #     return (move.distance + internal_distance) * amphipod.step_cost


def parse_nodes(lines: list[str]):
    room_capacity = len(lines) - 3

    nodes: dict[str, Node] = {}
    for col_index, letter in ROOM_NAMES_BY_X.items():
        nodes[letter] = Room(letter, room_capacity, letter)
        fill_room(lines, col_index, nodes[letter])

    left1 = Hallway('L1')
    left2 = Hallway('L2')
    left1.connect(left2, 1)

    left2.connect(nodes['A'], 2)
    ab = Hallway('AB')
    left2.connect(ab, 2)
    ab.connect(nodes['A'], 2)
    ab.connect(nodes['B'], 2)

    bc = Hallway('BC')
    bc.connect(ab, 2)
    bc.connect(nodes['B'], 2)
    bc.connect(nodes['C'], 2)

    cd = Hallway('CD')
    cd.connect(bc, 2)
    cd.connect(nodes['C'], 2)
    cd.connect(nodes['D'], 2)

    right2 = Hallway('R2')
    right2.connect(cd, 2)
    right2.connect(nodes['D'], 2)

    right1 = Hallway('R1')
    right1.connect(right2, 1)

    for h in (left1, left2, ab, bc, cd, right2, right1):
        nodes[h.id] = h
    return State(nodes, 0)


def fill_room(lines: list[str], col_index: int, room: Node):
    for y in range(len(lines) - 2, 1, -1):
        letter = lines[y][col_index]
        assert letter in 'ABCD'
        room.push_occupant(letter)


if __name__ == '__main__':
    main()
