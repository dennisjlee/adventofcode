from collections import defaultdict
from functools import reduce
from itertools import chain
from operator import mul
import math
import re
import sys
from typing import Dict, Optional, Tuple, List

TILE_NAME_PARSER = re.compile(r'Tile (\d+):')

N = 1j
E = 1
S = -1j
W = -1

EdgeMap = Dict[str, List[Tuple[int, complex]]]

SEA_MONSTER_REGEXES = [
    re.compile(r'..................#.'),
    re.compile(r'#....##....##....###'),
    re.compile(r'.#..#..#..#..#..#...'),
]
SEA_MONSTER_SIZE = 15


class Tile:
    def __init__(self, id: int, pixels: List[List[str]], neighbors=None):
        self.id = id
        self.pixels = pixels
        self.neighbors: Dict[complex, Optional[Tuple[int, complex]]] = neighbors if neighbors else {}
        self.edges: Dict[complex, str] = self._compute_edges()

    def __repr__(self):
        return f'Tile(id={self.id}, neighbors={repr(self.neighbors)}'

    def _compute_edges(self):
        top = ''.join(self.pixels[0])
        bottom = ''.join(self.pixels[-1])
        left = ''.join(row[0] for row in self.pixels)
        right = ''.join(row[-1] for row in self.pixels)
        edges = {
            N: top,
            S: bottom,
            W: left,
            E: right,
        }
        return edges

    def rotated(self, quarter_turns_ccw):
        new_pixels = self.pixels
        new_neighbors = self.neighbors
        for i in range(quarter_turns_ccw):
            new_pixels = list(reversed(list(zip(*new_pixels))))
        new_neighbors = {k * (1j ** quarter_turns_ccw): v for k, v in new_neighbors.items()}
        return Tile(self.id, new_pixels, new_neighbors)

    def flipped_vertically(self):
        new_pixels = list(reversed(self.pixels))
        new_neighbors = {
            N: self.neighbors.get(S),
            E: self.neighbors.get(E),
            S: self.neighbors.get(N),
            W: self.neighbors.get(W),
        }
        return Tile(self.id, new_pixels, new_neighbors)

    def flipped_horizontally(self):
        new_pixels = [list(reversed(row)) for row in self.pixels]
        new_neighbors = {
            N: self.neighbors.get(N),
            E: self.neighbors.get(W),
            S: self.neighbors.get(S),
            W: self.neighbors.get(E),
        }
        return Tile(self.id, new_pixels, new_neighbors)

    def hashtag_count(self):
        return sum(1 for c in chain(*self.pixels) if c == '#')


def reverse_str(s):
    return ''.join(reversed(s))


def main():
    with open(sys.argv[1]) as f:
        tile_sections = f.read().strip().split('\n\n')

    tiles = {}

    for section in tile_sections:
        lines = section.strip().split('\n')
        match = TILE_NAME_PARSER.match(lines[0])
        tile_id = int(match.group(1))
        tile_pixels = [list(line) for line in lines[1:]]
        tiles[tile_id] = Tile(tile_id, tile_pixels)

    edge_map: EdgeMap = defaultdict(list)
    for tile in tiles.values():
        for edge_id, edge in tile.edges.items():
            normalized_edge = min(edge, reverse_str(edge))
            edge_map[normalized_edge].append((tile.id, edge_id))

    corner_ids = part1(edge_map)
    part2(tiles, edge_map, corner_ids)


def part1(edge_map: EdgeMap):
    # Don't try to reconstruct the entire grid - just look
    # for 4 tiles that don't match anything on corners

    candidates = defaultdict(int)
    for matches in edge_map.values():
        if len(matches) == 1:
            candidates[matches[0][0]] += 1

    corner_ids = [candidate for candidate, count_non_matching in candidates.items()
                  if count_non_matching == 2]
    print(reduce(mul, corner_ids))
    return corner_ids


def part2(tiles: Dict[int, Tile], edge_map: EdgeMap, corner_ids: List[int]):
    tile_arrangement = construct_tile_arrangement(corner_ids, edge_map, tiles)
    rows_per_tile = len(tile_arrangement[0][0].pixels) - 2
    final_row_count = len(tile_arrangement) * rows_per_tile
    final_image = []
    for r in range(final_row_count):
        tile_row_index = r // rows_per_tile
        pixel_row_index = (r % rows_per_tile) + 1

        final_image.append(list(chain(*(
            tile.pixels[pixel_row_index][1:-1]
            for tile in tile_arrangement[tile_row_index]
        ))))

    full_tile = Tile(0, final_image)  # TODO: use a different class from Tile to avoid computing edges unnecessarily
    # there is only one rotation / flip that will produce any sea monsters
    monster_indexes = 0
    for i in range(4):
        monster_indexes = count_sea_monsters(full_tile)
        if monster_indexes:
            break
        monster_indexes = count_sea_monsters(full_tile.flipped_vertically())
        if monster_indexes:
            break
        full_tile = full_tile.rotated(1)
    print(full_tile.hashtag_count() - (len(monster_indexes) * SEA_MONSTER_SIZE))


def count_sea_monsters(tile):
    monster_indexes = []
    strings = [''.join(row) for row in tile.pixels]
    for i in range(1, len(strings) - 1):
        search_index = 0
        while True:
            # match the middle regex first because it's the most constrained
            match = SEA_MONSTER_REGEXES[1].search(strings[i], search_index)
            if not match:
                break
            if (SEA_MONSTER_REGEXES[0].match(strings[i-1], match.start()) and
                    SEA_MONSTER_REGEXES[2].match(strings[i+1], match.start())):
                monster_indexes.append((match.start(), i-1))
                search_index = match.end() + 1
            else:
                # Allow overlapping matches for the middle regex
                search_index = match.start() + 1
    return monster_indexes


def construct_tile_arrangement(corner_ids, edge_map, tiles):
    length = int(math.sqrt(len(tiles)))
    tile_arrangement: List[List[Optional[Tile]]] = [
        [None for x in range(length)]
        for y in range(length)
    ]
    corner_tiles = [tiles[tile_id] for tile_id in corner_ids]
    for matches in edge_map.values():
        if len(matches) == 1:
            tile_id, edge_id = matches[0]
            tile = tiles[tile_id]
            tile.neighbors_bounded[edge_id] = None
        else:
            assert len(matches) == 2, "Unexpected situation with more than 2 matches!"
            tile_id1, edge_id1 = matches[0]
            tile_id2, edge_id2 = matches[1]
            tiles[tile_id1].neighbors_bounded[edge_id1] = matches[1]
            tiles[tile_id2].neighbors_bounded[edge_id2] = matches[0]
    nw_corner = corner_tiles[0]
    while not (nw_corner.neighbors_bounded[N] is None and nw_corner.neighbors_bounded[W] is None):
        nw_corner = nw_corner.rotated(1)
    tile_arrangement[0][0] = nw_corner
    prev_tile = nw_corner
    for c in range(1, length):
        next_tile = get_east_neighbor(prev_tile, tiles)
        prev_tile = next_tile
        tile_arrangement[0][c] = next_tile
    for r in range(1, length):
        for c in range(length):
            tile_arrangement[r][c] = get_south_neighbor(tile_arrangement[r - 1][c], tiles)
    # print('\n'.join(' '.join(str(tile.id) for tile in row) for row in tile_arrangement))
    return tile_arrangement


def get_east_neighbor(prev_tile, tiles):
    next_tile_id, next_edge_id = prev_tile.neighbors_bounded[E]
    next_tile = tiles[next_tile_id]
    # rotate
    if next_edge_id != W:
        next_tile = next_tile.rotated(rotations_needed(next_edge_id, W))

    # flip if needed
    if prev_tile.edges[E] != next_tile.edges[W]:
        next_tile = next_tile.flipped_vertically()
        assert prev_tile.edges[E] == next_tile.edges[W], "Edges should now match!"
    return next_tile


def get_south_neighbor(prev_tile, tiles):
    next_tile_id, next_edge_id = prev_tile.neighbors_bounded[S]
    next_tile = tiles[next_tile_id]
    # rotate
    if next_edge_id != N:
        next_tile = next_tile.rotated(rotations_needed(next_edge_id, N))

    # flip if needed
    if prev_tile.edges[S] != next_tile.edges[N]:
        next_tile = next_tile.flipped_horizontally()
        assert prev_tile.edges[S] == next_tile.edges[N], "Edges should now match!"
    return next_tile


def rotations_needed(start_direction: complex, end_direction: complex) -> int:
    if start_direction == end_direction:
        return 0
    total_rotation = end_direction / start_direction
    if total_rotation == -1:
        return 2
    elif total_rotation == 1j:
        return 1
    else:
        return 3


if __name__ == '__main__':
    main()