from collections import deque
import itertools
import sys


def main():
    with open(sys.argv[1]) as f:
        sections = f.read().strip().split('\n\n')

    part1(sections)
    part2(sections)


def part1(sections):
    deck1 = parse_deck(sections[0])
    deck2 = parse_deck(sections[1])

    while deck1 and deck2:
        iterate_decks_basic(deck1, deck2)
    print(count_score(deck1) if deck1 else count_score(deck2))


def iterate_decks_basic(deck1, deck2):
    card1 = deck1[0]
    card2 = deck2[0]
    if card1 > card2:
        deck1.rotate(-1)
        deck1.append(deck2.popleft())
    elif card2 > card1:
        deck2.rotate(-1)
        deck2.append(deck1.popleft())
    else:
        assert False, "Rules don't allow for ties!"


def part2(sections):
    deck1 = parse_deck(sections[0])
    deck2 = parse_deck(sections[1])

    winner = recursive_combat(deck1, deck2)
    print(count_score(deck1) if winner == 1 else count_score(deck2))


def recursive_combat(deck1, deck2):
    previous_configs = set()
    while deck1 and deck2:
        key = (tuple(deck1), tuple(deck2))
        if key in previous_configs:
            # short circuit, player 1 wins
            return 1
        previous_configs.add(key)
        iterate_decks_recursive(deck1, deck2)
    return 1 if deck1 else 2


def iterate_decks_recursive(deck1, deck2):
    card1 = deck1[0]
    card2 = deck2[0]
    if len(deck1) > card1 and len(deck2) > card2:
        winner = recursive_combat(deque(itertools.islice(deck1, 1, card1+1)),
                                  deque(itertools.islice(deck2, 1, card2+1)))
    elif card1 > card2:
        winner = 1
    elif card2 > card1:
        winner = 2
    else:
        assert False, "Rules don't allow for ties!"

    if winner == 1:
        deck1.rotate(-1)
        deck1.append(deck2.popleft())
    else:
        deck2.rotate(-1)
        deck2.append(deck1.popleft())


def parse_deck(section: str):
    lines = section.strip().split('\n')
    return deque(int(line) for line in lines[1:])  # skip player N line


def count_score(deck):
    score = 0
    for i, card in enumerate(reversed(deck)):
        score += (i + 1) * card
    return score


if __name__ == '__main__':
    main()
