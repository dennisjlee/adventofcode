import sys


def main():
    with open(sys.argv[1]) as f:
        instructions = [l.strip() for l in f]

    part1(instructions)
    part2(instructions)


def part1(instructions):
    # model position as a complex number - x coordinates are the real component,
    # y coordinates are the imaginary component
    position = 0
    direction = 1
    for instruction in instructions:
        operation = instruction[0]
        magnitude = int(instruction[1:])
        if operation == 'N':
            position += magnitude * 1j
        elif operation == 'E':
            position += magnitude
        elif operation == 'S':
            position -= magnitude * 1j
        elif operation == 'W':
            position -= magnitude
        elif operation == 'F':
            position += direction * magnitude
        elif operation == 'R':
            direction = rotate(direction, 360 - magnitude)
        elif operation == 'L':
            direction = rotate(direction, magnitude)

    print(int(abs(position.real) + abs(position.imag)))


def part2(instructions):
    position = 0
    waypoint = 10 + 1j
    for instruction in instructions:
        operation = instruction[0]
        magnitude = int(instruction[1:])
        if operation == 'N':
            waypoint += magnitude * 1j
        elif operation == 'E':
            waypoint += magnitude
        elif operation == 'S':
            waypoint -= magnitude * 1j
        elif operation == 'W':
            waypoint -= magnitude
        elif operation == 'F':
            position += waypoint * magnitude
        elif operation == 'R':
            waypoint = rotate(waypoint, 360 - magnitude)
        elif operation == 'L':
            waypoint = rotate(waypoint, magnitude)

    print(int(abs(position.real) + abs(position.imag)))


def rotate(coord, angle):
    quarter_turns = angle / 90
    return coord * (1j ** quarter_turns)


if __name__ == '__main__':
    main()
