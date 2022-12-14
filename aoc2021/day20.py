import sys
import typing
from collections import defaultdict


DEBUG = False


class Point(typing.NamedTuple):
    x: int
    y: int


def main():
    with open(sys.argv[1]) as f:
        image_enhancement, input_section = f.read().strip().split('\n\n')

        pixel_mapping = [int(char == '#') for char in image_enhancement]

        default_value = 0
        image = defaultdict(lambda: default_value)
        lines = input_section.strip().split('\n')
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                val = int(char == '#')
                image[Point(x, y)] = val

        BUFFER = 2

        y_start = -BUFFER
        y_end = len(lines) + BUFFER
        x_start = -BUFFER
        x_end = len(lines[0]) + BUFFER
        if DEBUG:
            print_image(image, x_start, x_end, y_start, y_end)
        for i in range(50):
            print(i)
            new_default = pixel_mapping[int(str(default_value) * 9, 2)]
            next_image = defaultdict(constant_factory(new_default))
            for y in range(y_start, y_end):
                for x in range(x_start, x_end):
                    p = Point(x, y)
                    next_image[p] = process_pixel(p, image, pixel_mapping)

            default_value = new_default
            image = next_image
            y_start -= BUFFER
            x_start -= BUFFER
            y_end += BUFFER
            x_end += BUFFER
            if DEBUG:
                print_image(image, x_start, x_end, y_start, y_end)

            if i == 1:
                # part 1
                print(sum(image.values()))

        # part 2
        print(sum(image.values()))


def constant_factory(value):
    return lambda: value


def print_image(image: dict[Point, int], x_start: int, x_end: int, y_start: int, y_end: int):
    for y in range(y_start, y_end):
        print(''.join('*' if x == 0 and y == 0 else '#' if image[Point(x, y)] else '.' for x in range(x_start, x_end)))
    print()


def process_pixel(p: Point, image: dict[Point, int], pixel_mapping: list[int]) -> int:
    digits = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            digits.append(str(image[Point(p.x + dx, p.y + dy)]))

    return pixel_mapping[int(''.join(digits), 2)]


if __name__ == '__main__':
    main()
