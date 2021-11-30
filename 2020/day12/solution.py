import re
import sys

def main():
    with open(sys.argv[1]) as f:
        instructions = [l.strip() for l in f]

    part1(instructions)
    part2(instructions)


def part1(instructions):
    x = 0
    y = 0
    direction = (1, 0)
    for instruction in instructions:
        operation = instruction[0]
        magnitude = int(instruction[1:])
        if operation == 'N':
            y += magnitude
        elif operation == 'E':
            x += magnitude
        elif operation == 'S':
            y -= magnitude
        elif operation == 'W':
            x -= magnitude
        elif operation == 'F':
            x += direction[0] * magnitude
            y += direction[1] * magnitude
        elif operation == 'R':
            direction = rotate(direction, 360 - magnitude)
        elif operation == 'L':
            direction = rotate(direction, magnitude)

    print(abs(x) + abs(y))


def part2(instructions):
    x = 0
    y = 0
    wx = 10
    wy = 1
    for instruction in instructions:
        operation = instruction[0]
        magnitude = int(instruction[1:])
        if operation == 'N':
            wy += magnitude
        elif operation == 'E':
            wx += magnitude
        elif operation == 'S':
            wy -= magnitude
        elif operation == 'W':
            wx -= magnitude
        elif operation == 'F':
            x += wx * magnitude
            y += wy * magnitude
        elif operation == 'R':
            wx, wy = rotate((wx, wy), 360 - magnitude)
        elif operation == 'L':
            wx, wy = rotate((wx, wy), magnitude)

    print(abs(x) + abs(y))


def rotate(coord, angle, origin=(0, 0)):
    x, y = coord
    ox, oy = origin
    dx = x - ox
    dy = y - oy
    if angle == 90:
        return ox - dy, oy + dx
    elif angle == 180:
        return ox - dx, oy - dy
    elif angle == 270:
        return ox + dy, oy - dx


if __name__ == '__main__':
    main()
