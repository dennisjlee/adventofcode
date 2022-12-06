from __future__ import annotations
import sys


def main():
    with open(sys.argv[1]) as f:
        buffer = f.read().strip()

    for i in range(3, len(buffer)):
        test = set(buffer[i-3:i+1])
        if len(test) == 4:
            print(i + 1)
            break

    for i in range(13, len(buffer)):
        test = set(buffer[i-13:i+1])
        if len(test) == 14:
            print(i + 1)
            break


if __name__ == '__main__':
    main()
