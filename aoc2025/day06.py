from __future__ import annotations

import sys
from math import prod
from pathlib import Path
from typing import cast, Literal, NamedTuple


class MathProblem(NamedTuple):
    operands: list[int]
    operator: Literal["*", "+"]

    def result(self) -> int:
        op = sum if self.operator == "+" else prod
        return op(self.operands)

def main():
    with Path(sys.argv[1]).open() as f:
        lines = f.readlines()
    operands_lines = [line.split() for line in lines[:-1]]
    operators = lines[-1].split()
    problems1 = [
        MathProblem(
            [int(operands[i]) for operands in operands_lines],
            cast(Literal["+", "*"], operator)
        )
        for i, operator in enumerate(operators)
    ]
    print(sum(problem.result() for problem in problems1))

    problems2: list[MathProblem] = []
    curr_operands: list[int] = []
    for col in range(len(lines[0]) - 2, -1, -1):  # -2 to skip newline
        curr_operand: str = ""
        for line in lines[:-1]:
            char = line[col]
            if char != " ":
                curr_operand += char
        if len(curr_operand):
            curr_operands.append(int(curr_operand))
        op = lines[-1][col]
        if op == "+" or op == "*":
            problems2.append(MathProblem(curr_operands, op))
            curr_operands = []
    print(sum(problem.result() for problem in problems2))






if __name__ == "__main__":
    main()