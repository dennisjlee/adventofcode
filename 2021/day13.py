import re
import sys
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


def main():
    coordinates = set()
    folds = []
    fold_pattern = re.compile(r'fold along ([xy])=(\d+)')

    with open(sys.argv[1]) as f:
        contents = f.read()
        coordinate_content, fold_content = contents.split('\n\n')
        for coordinate_line in coordinate_content.strip().split('\n'):
            xs, ys = coordinate_line.strip().split(',')
            coordinates.add(Point(int(xs), int(ys)))

        for fold_line in fold_content.strip().split('\n'):
            match = fold_pattern.match(fold_line)
            x_or_y = match.group(1)
            position = int(match.group(2))
            folds.append((x_or_y, position))

    new_points = execute_fold(coordinates, folds[0])
    print(len(new_points))

    for fold in folds[1:]:
        new_points = execute_fold(new_points, fold)

    height = max(p.y for p in new_points)
    width = max(p.x for p in new_points)
    grid = [
        ['.' for x in range(width + 1)]
        for y in range(height + 1)
    ]
    for p in new_points:
        grid[p.y][p.x] = '#'

    print('\n'.join(''.join(row) for row in grid))


def execute_fold(points, fold):
    new_points = set()
    line_position = fold[1]
    if fold[0] == 'x':
        for point in points:
            if point.x > line_position:
                new_points.add(Point(point.x - 2 * (point.x - line_position), point.y))
            else:
                new_points.add(point)
    else:
        for point in points:
            if point.y > line_position:
                new_points.add(Point(point.x, point.y - 2 * (point.y - line_position)))
            else:
                new_points.add(point)

    return new_points


if __name__ == '__main__':
    main()
