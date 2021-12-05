from __future__ import annotations
import re
import sys


class Marble:
    value: int = 0
    # clockwise
    next: Marble = None

    # counterclockwise
    prev: Marble = None

    def __init__(self, value: int):
        self.value = value
        self.next = self
        self.prev = self

    def insert_after(self, new_marble: Marble):
        old_next = self.next
        self.next = new_marble
        new_marble.prev = self
        new_marble.next = old_next
        old_next.prev = new_marble

    def remove(self):
        self.next.prev = self.prev
        self.prev.next = self.next


def main():
    with open(sys.argv[1]) as f:
        line = f.readline()
        match = re.match(r'(\d+) players; last marble is worth (\d+) points', line.strip())
        num_players = int(match.group(1))
        last_marble_value = int(match.group(2))

    print(get_high_score(num_players, last_marble_value))
    print(get_high_score(num_players, last_marble_value * 100))


def get_high_score(num_players, last_marble_value):
    scores = [0 for _ in range(num_players)]
    current_marble = Marble(0)
    player_index = 0
    for marble_value in range(1, last_marble_value + 1):
        player_index = (player_index + 1) % num_players
        if marble_value % 23 == 0:
            to_remove = current_marble.prev.prev.prev.prev.prev.prev.prev
            scores[player_index] += marble_value + to_remove.value
            to_remove.remove()
            current_marble = to_remove.next
        else:
            new_marble = Marble(marble_value)
            current_marble.next.insert_after(new_marble)
            current_marble = new_marble

    return max(scores)


if __name__ == '__main__':
    main()
