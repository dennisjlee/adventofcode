import sys


def main():
    x = 0
    y = 0

    commands = []
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            direction, magnitude = line.strip().split()
            commands.append((direction, int(magnitude)))

    for direction, delta in commands:
        if direction == 'forward':
            x += delta
        elif direction == 'down':
            y += delta
        elif direction == 'up':
            y -= delta

    print(x * y)

    # part 2
    x = 0
    y = 0
    aim = 0

    for direction, delta in commands:
        if direction == 'forward':
            x += delta
            y += aim * delta
        elif direction == 'down':
            aim += delta
        elif direction == 'up':
            aim -= delta

    print(x * y)

if __name__ == '__main__':
    main()
