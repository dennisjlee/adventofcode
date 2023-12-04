import re
import sys


class Card:
    id: int
    overlap_count: int
    count: int
    winning_numbers: set[int]
    actual_numbers: set[int]

    def __init__(self, id: int, winning_numbers: set[int], actual_numbers: set[int]):
        self.id = id
        self.count = 1
        self.winning_numbers = winning_numbers
        self.actual_numbers = actual_numbers
        self.overlap_count = len(winning_numbers & actual_numbers)


def main():
    card_regex = re.compile(r'Card\s+(\d+):\s+(.*)\s+\|\s+(.*)')
    whitespace = re.compile(r'\s+')
    cards: list[Card] = []
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            match = card_regex.search(line)
            id = int(match.group(1))
            winning_numbers = set(int(s) for s in whitespace.split(match.group(2)))
            numbers = [int(s) for s in whitespace.split(match.group(3))]
            actual_numbers = set(numbers)
            assert len(numbers) == len(actual_numbers)
            cards.append(Card(id, winning_numbers, actual_numbers))

    points = 0
    for card in cards:
        if card.overlap_count:
            points += 2 ** (card.overlap_count - 1)
    print(points)

    for i, card in enumerate(cards):
        if card.overlap_count:
            for j in range(i + 1, min(len(cards), i + card.overlap_count + 1)):
                other_card = cards[j]
                other_card.count += card.count

    print(sum(card.count for card in cards))


if __name__ == '__main__':
    main()
