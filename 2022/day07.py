from __future__ import annotations

import math
from typing import NamedTuple, Optional
import re
import sys


class File(NamedTuple):
    name: str
    size: int


class Directory(NamedTuple):
    name: str
    files: list[File]
    directories: list[Directory]
    parent: Optional[Directory]

    @property
    def size(self):
        return sum(f.size for f in self.files) + sum(d.size for d in self.directories)

    def part1(self):
        total = 0
        self_size = self.size
        if self_size < 100000:
            total += self_size

        for d in self.directories:
            total += d.part1()

        return total

    def part2(self, needed_space):
        self_size = self.size
        if self_size >= needed_space:
            return min(self_size, *[d.part2(needed_space) for d in self.directories])
        else:
            return math.inf


CMD_REGEX = re.compile(r'\$ (\w\w)(?: (.+))?$')


TOTAL_SPACE = 70_000_000
TARGET_SPACE = 30_000_000


def main():
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    root = Directory('/', [], [], None)
    cwd = root

    for line in lines:
        if line[0] == '$':
            match = CMD_REGEX.match(line)
            cmd = match.group(1)
            arg = match.group(2)
            if cmd == 'cd':
                if arg == '..':
                    cwd = cwd.parent
                elif arg == '/':
                    cwd = root
                else:
                    cwd = next(child for child in cwd.directories if child.name == arg)
            elif cmd == 'ls':
                # nothing to do - we'll parse the ls results in the next lines
                pass
        else:
            desc, name = line.split(' ')
            if desc == 'dir':
                cwd.directories.append(Directory(name, [], [], cwd))
            else:
                cwd.files.append(File(name, int(desc)))

    print(root.part1())

    needed_space = TARGET_SPACE - (TOTAL_SPACE - root.size)
    print(root.part2(needed_space))


if __name__ == '__main__':
    main()
