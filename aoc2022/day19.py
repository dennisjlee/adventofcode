from __future__ import annotations

from collections import Counter
import re
import sys
from typing import NamedTuple


class State(NamedTuple):
    time: int
    resources: Counter
    robots: Counter

    def __hash__(self):
        return hash((self.time, tuple(self.resources.items()), tuple(self.robots.items())))


KEYS = [
    'ore',
    'clay',
    'obsidian',
    'geode'
]

class Blueprint(NamedTuple):
    id: int
    robot_costs: tuple[Counter, Counter, Counter, Counter]

    def optimize_geodes(self, total_minutes: int, verbose=False) -> int:
        states = [
            State(time=1, resources=Counter(), robots=Counter({'ore': 1}))
        ]
        most_geodes = 0
        best_state = None
        step = 0
        seen_states = set()
        while states:
            step += 1
            if verbose and step % 100_000 == 0:
                print(f'step {step}, {len(states)} states and {len(seen_states)} seen states; most_geodes {most_geodes}')
            state = states.pop()
            if state in seen_states:
                continue
            seen_states.add(state)
            if state.time > total_minutes:
                if state.resources['geode'] > most_geodes:
                    most_geodes = state.resources['geode']
                    best_state = state
                # if verbose:
                #     print(f'finished a state in {step} steps, most_geodes {most_geodes}')
                continue
            else:
                # assume best possible scenario - that we make a new geode robot every turn for the remaining turns
                time_left = total_minutes - state.time + 1
                most_possible_geodes = state.resources['geode'] + (time_left * state.robots['geode']) + \
                    (time_left * (time_left - 1)) // 2
                if most_possible_geodes < most_geodes:
                    # print(f'skipping a state by heuristic at step {step}')
                    continue

            built_robot = False
            for i in range(4):
                cost = self.robot_costs[i]
                if set(state.robots) >= set(cost):
                    # we have the right robots to produce this robot, but possibly not enough resources yet
                    new_time = state.time
                    resources = state.resources

                    # NOTE: for Counters, >= is not the opposite of <!
                    while not (resources >= cost) and new_time < total_minutes:
                        new_time += 1
                        resources = resources + state.robots

                    if resources >= cost:
                        built_robot = True
                        new_resources = resources - cost + state.robots
                        new_robots = state.robots + Counter([KEYS[i]])
                        states.append(State(new_time + 1, new_resources, new_robots))

            if not built_robot:
                states.append(State(state.time + 1, state.resources + state.robots, state.robots))

        if verbose:
            print(most_geodes, best_state)
        return most_geodes


# Example input line (wrapped):
# Blueprint 1: Each ore robot costs 4 ore.
# Each clay robot costs 4 ore.
# Each obsidian robot costs 4 ore and 17 clay.
# Each geode robot costs 4 ore and 20 obsidian.

PARSE_PATTERN = re.compile(r'^Blueprint (\d+):\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)')


def main():
    blueprints: list[Blueprint] = []
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            match = PARSE_PATTERN.match(line)
            blueprints.append(Blueprint(
                id=int(match.group(1)),
                robot_costs=(
                    Counter({'ore': int(match.group(2))}),
                    Counter({'ore': int(match.group(3))}),
                    Counter({'ore': int(match.group(4)), 'clay': int(match.group(5))}),
                    Counter({'ore': int(match.group(6)), 'obsidian': int(match.group(7))}),
                )
            ))

    # part1(blueprints)
    part2(blueprints)

def part1(blueprints: list[Blueprint]):
    total_quality_level = 0
    for blueprint in blueprints:
        most_geodes = blueprint.optimize_geodes(total_minutes=24)
        print(blueprint.id, most_geodes)
        total_quality_level += blueprint.id * most_geodes
    print(total_quality_level)


def part2(blueprints: list[Blueprint]):
    result = 1
    for blueprint in blueprints[:3]:
        most_geodes = blueprint.optimize_geodes(total_minutes=32, verbose=True)
        print(blueprint.id, most_geodes)
        result *= most_geodes
    print(result)


if __name__ == '__main__':
    main()
