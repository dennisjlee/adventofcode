import re
import sys
from typing import NamedTuple


CONFIG_REGEX = re.compile(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)")


class ClawMachine(NamedTuple):
    a_dx: int
    a_dy: int
    b_dx: int
    b_dy: int
    prize_x: int
    prize_y: int

    def solve1(self) -> int | None:
        x = 0
        y = 0
        i = 1
        while x <= self.prize_x and y <= self.prize_y and i <= 100:
            x += self.a_dx
            y += self.a_dy

            coeff_x, rem_x = divmod(self.prize_x - x, self.b_dx)
            if rem_x == 0:
                coeff_y, rem_y = divmod(self.prize_y - y, self.b_dy)
                if rem_y == 0 and coeff_x == coeff_y:
                    return i * 3 + coeff_x
            i += 1
        return None


def main():
    machines: list[ClawMachine] = []
    with open(sys.argv[1]) as f:
        raw = f.read()
        for match in CONFIG_REGEX.finditer(raw):
            machines.append(ClawMachine(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4)),
                int(match.group(5)),
                int(match.group(6)),
            ))

    tokens_spent = 0
    for machine in machines:
        if (tokens := machine.solve()) is not None:
            tokens_spent += tokens
    print(tokens_spent)



if __name__ == '__main__':
    main()
