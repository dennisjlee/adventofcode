import re
import sys
import bisect
import math
from typing import NamedTuple
import math


class Race(NamedTuple):
    time: int
    distance: int

    def ways_to_win(self) -> int:
        for i in range(1, self.time):
            if i * (self.time - i) > self.distance:
                return int(((self.time / 2) - i) * 2) + 1
        return 0


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    times = [int(s) for s in lines[0].split(':')[1].strip().split()]
    distances = [int(s) for s in lines[1].split(':')[1].strip().split()]

    races = [Race(time, distance) for (time, distance) in zip(times, distances)]

    # part 1
    print(math.prod(race.ways_to_win() for race in races))

    # part 2
    whitespace = re.compile(r'\s+')
    time = int(whitespace.sub('', lines[0].split(':')[1]))
    distance = int(whitespace.sub('', lines[1].split(':')[1]))
    print(Race(time, distance).ways_to_win())


if __name__ == '__main__':
    main()
