import sys
from collections import namedtuple, Counter
import math


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.small = name.islower()
        self.neighbors = []
        self.max_visits = 1 if self.small else math.inf


State = namedtuple('State', ['cave', 'visited', 'path'])


def main():
    caves_by_name = {}

    with open(sys.argv[1]) as f:
        for line in f.readlines():
            cave1_name, cave2_name = line.strip().split('-')
            cave1 = caves_by_name.setdefault(cave1_name, Cave(cave1_name))
            cave2 = caves_by_name.setdefault(cave2_name, Cave(cave2_name))
            cave1.neighbors.append(cave2)
            cave2.neighbors.append(cave1)

    start = caves_by_name['start']
    end = caves_by_name['end']

    valid_paths = set()

    def bfs():
        queue = [State(start, Counter(['start']), ['start'])]
        while queue:
            current = queue.pop()
            for neighbor in current.cave.neighbors:
                if neighbor == end:
                    valid_paths.add(tuple(current.path))
                    continue
                if current.visited[neighbor.name] >= neighbor.max_visits:
                    continue
                new_visited = Counter(current.visited)
                new_visited[neighbor.name] += 1
                new_path = list(current.path)
                new_path.append(neighbor.name)
                queue.append(State(neighbor, new_visited, new_path))

    bfs()
    # part 1 answer
    print(len(valid_paths))

    # for each small cave, try the BFS with 2 visits allowed to that cave (we'll hit a lot of duplicate paths but we're
    # deduping)
    for cave in caves_by_name.values():
        if cave.small and cave is not start:
            cave.max_visits = 2
            bfs()
            cave.max_visits = 1

    # part 2 answer
    print(len(valid_paths))


if __name__ == '__main__':
    main()
