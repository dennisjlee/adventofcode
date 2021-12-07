import re
import sys


def main():
    with open(sys.argv[1]) as f:
        contents = f.read()
        initial_state_str, transitions_str = contents.strip().split('\n\n')

    initial = initial_state_str[len('initial state: '):]

    transitions = transitions_str.split('\n')
    positive_states = [t[:5] for t in transitions if t.endswith('#')]
    print(initial)
    print(positive_states)

    print(iterate(initial, positive_states, 20))
    print(iterate_set(initial, positive_states, 50_000_000_000))


def iterate(initial: str, positive_states: list[str], generations: int) -> int:
    # This regex will match a zero-length string that is followed by any of the strings that will result in a new plant
    pattern = re.compile(f'(?={"|".join(re.escape(s) for s in positive_states)})')

    padding = '....'
    start_index = 0

    state = initial
    for i in range(generations):
        # print(state.ljust(250, '.'))
        if not state.endswith(padding):
            state += padding
        if not state.startswith(padding):
            state = padding + state
            start_index -= len(padding)
        new_state = ['.'] * len(state)
        for match in pattern.finditer(state):
            matching_index = match.start() + 2
            new_state[matching_index] = '#'
        state = ''.join(new_state)

    return sum(i + start_index for i, char in enumerate(state) if char == '#')


def iterate_set(initial: str, positive_states: list[str], generations: int) -> int:
    # sparse representation of the number line - set of all indices marked with '#'
    initial_state = {i for i, char in enumerate(initial) if char == '#'}
    boolean_patterns = {
        tuple(c == '#' for c in positive_state)
        for positive_state in positive_states
    }
    state = initial_state
    for g in range(generations):
        new_state = set()
        for i in range(min(state) - 4, max(state) + 1):
            current = tuple(((i + delta) in state) for delta in range(5))
            if current in boolean_patterns:
                new_state.add(i + 2)
        if new_state == {index + 1 for index in state}:
            # I'm not sure if this is guaranteed for all inputs, but for my input the plants eventually reached
            # a stable pattern where all plants would move one spot to the right between every generation. Once this is
            # reached, we can take a shortcut!
            print('Reached stable pattern at generation', g)
            return sum(generations - g - 1 + index for index in new_state)
        state = new_state

    return sum(state)


if __name__ == '__main__':
    main()