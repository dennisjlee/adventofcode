from collections import defaultdict
from functools import reduce
from operator import mul
import math
import re
import sys
from typing import Dict, Optional, Set, Tuple, List

TILE_NAME_PARSER = re.compile(r'Tile (\d+):')

N = 1j
E = 1
S = -1j
W = -1


class Tile:
    def __init__(self, id, pixels, edges=None, neighbors=None):
        self.id = id
        self.pixels = pixels
        self.edges = edges if edges else self._compute_edges()
        self.neighbors: Dict[int, Optional[Tuple[int, int]]] = neighbors if neighbors else {}

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
        new_edges = self.edges
        new_neighbors = self.neighbors
        for i in range(quarter_turns_ccw):
            new_pixels = list(reversed(list(zip(*new_pixels))))
            new_edges = {k * 1j: v for k, v in new_edges.items()}
            new_neighbors = {k * 1j: v for k, v in new_neighbors.items()}
        return Tile(self.id, new_pixels, new_edges, new_neighbors)


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

    edge_map: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
    for tile in tiles.values():
        for edge_id, edge in tile.edges.items():
            normalized_edge = min(edge, reverse_str(edge))
            edge_map[normalized_edge].append((tile.id, edge_id))

    corner_ids = part1(edge_map)
    part2(tiles, edge_map, corner_ids)


def part1(edge_map):
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


def part2(tiles: Dict[int, Tile], edge_map: Dict[str, List[Tuple[int, int]]], corner_ids: List[int]):
    length = int(math.sqrt(len(tiles)))
    tile_arrangement: List[List[Optional[Tile]]] = [
        [None for x in range(length)]
        for y in range(length)
    ]

    edge_tiles = []
    corner_tiles = [tiles[tile_id] for tile_id in corner_ids]
    for matches in edge_map.values():
        if len(matches) == 1:
            tile_id, edge_id = matches[0]
            tile = tiles[tile_id]
            tile.neighbors[edge_id] = None
            if tile_id not in corner_ids:
                edge_tiles.append(tile)
        else:
            assert len(matches) == 2, "Unexpected situation with more than 2 matches!"
            tile_id1, edge_id1 = matches[0]
            tile_id2, edge_id2 = matches[1]
            tiles[tile_id1].neighbors[edge_id1] = (tile_id2, edge_id2)
            tiles[tile_id2].neighbors[edge_id2] = (tile_id1, edge_id1)

    print(corner_tiles[0])
    print('\n'.join(''.join(c for c in row) for row in corner_tiles[0].pixels))
    print()
    rotated_corner0 = corner_tiles[0].rotated(1)
    print('\n'.join(''.join(c for c in row) for row in rotated_corner0.pixels))


if __name__ == '__main__':
    main()
