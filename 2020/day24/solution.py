from collections import defaultdict
import re
import sys


WHITE = True
BLACK = False

E = 'e'
SE = 'se'
SW = 'sw'
W = 'w'
NW = 'nw'
NE = 'ne'

DIRECTIONS = [
    E,
    W,
    SW,
    NE,
    SE,
    NW,
]

PARSER = re.compile(r'(se|sw|ne|nw|e|w)')


def main():
    with open(sys.argv[1]) as f:
        sequences = [PARSER.findall(line.strip()) for line in f.readlines()]

    tiles = part1(sequences)
    part2(tiles)


def part1(sequences):
    tiles = defaultdict(lambda: WHITE)
    root = 0 + 0j
    tiles[root] = WHITE
    for sequence in sequences:
        current = root
        for direction in sequence:
            current = neighbor(current, direction)
        tiles[current] = not tiles[current]

    print(sum(1 for color in tiles.values() if color == BLACK))
    return tiles


def neighbor(coordinate, direction):
    if direction == E:
        return coordinate + 1
    elif direction == W:
        return coordinate - 1
    elif direction == NE:
        return coordinate + 1j
    elif direction == SW:
        return coordinate - 1j
    elif direction == NW:
        return coordinate - 1 + 1j
    elif direction == SE:
        return coordinate + 1 - 1j


def part2(tiles):
    curr_tiles = tiles
    for i in range(100):
        new_tiles = iterate_tiles(curr_tiles)
        curr_tiles = new_tiles

    print(sum(1 for color in curr_tiles.values() if color == BLACK))


def iterate_tiles(tiles):
    new_tiles = defaultdict(lambda: WHITE)
    for coord in [c for c, color in tiles.items() if color == BLACK]:
        # execute the black tile rule first (zero or >2 black tile neighbors --> white)
        # this will ensure all white tile neighbors of black tiles are populated in the dictionary
        black_tile_neighbors = 0
        for direction in DIRECTIONS:
            if tiles[neighbor(coord, direction)] == BLACK:
                black_tile_neighbors += 1
        new_tiles[coord] = WHITE if (black_tile_neighbors == 0 or black_tile_neighbors > 2) else BLACK

    for coord in [c for c, color in tiles.items() if color == WHITE]:
        black_tile_neighbors = 0
        for direction in DIRECTIONS:
            if tiles[neighbor(coord, direction)] == BLACK:
                black_tile_neighbors += 1
        new_tiles[coord] = BLACK if (black_tile_neighbors == 2) else WHITE

    return new_tiles


if __name__ == '__main__':
    main()
