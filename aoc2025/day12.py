from __future__ import annotations

import sys
import numpy as np
from pathlib import Path
from typing import NamedTuple


class Shape(NamedTuple):
    label: int
    array: np.ndarray

    @staticmethod
    def parse(block: str) -> Shape:
        lines = block.strip().split("\n")
        label = int(lines[0][:-1])
        array = np.array(
            [
                [1 if c == "#" else 0 for c in line]
                for line in lines[1:]
            ]
        )
        return Shape(label, array)


def main():
    contents = Path(sys.argv[1]).read_text()
    blocks = contents.split("\n\n")
    shapes = [Shape.parse(block) for block in blocks[:-1]]
    print(shapes)
        

if __name__ == "__main__":
    main()