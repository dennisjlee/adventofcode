from __future__ import annotations

import itertools
import re
import sys

# represent points as complex numbers - real component is x, imaginary component is y
Point = complex

TURN_LEFT = 0
STRAIGHT = 1
TURN_RIGHT = 2

ROTATE_LEFT = -1j
ROTATE_RIGHT = 1j

VECTOR_LEFT = -1
VECTOR_RIGHT = 1
VECTOR_UP = -1j
VECTOR_DOWN = 1j

DIRECTION_TO_VECTOR = {
    '<': VECTOR_LEFT,
    '>': VECTOR_RIGHT,
    '^': VECTOR_UP,
    'v': VECTOR_DOWN
}


class Cart:
    def __init__(self, x: int, y: int, direction: str):
        self.position = x + y * 1j
        self.vector = DIRECTION_TO_VECTOR[direction]
        self.next_turn = TURN_LEFT

    def current_track(self, tracks: list[str]):
        return tracks[int(self.position.imag)][int(self.position.real)]

    def step(self, tracks: list[str], carts: dict[Point, Cart]):
        if self.position not in carts:
            # This cart has already crashed and been removed from the tracks
            return None

        del carts[self.position]
        self.position += self.vector
        track = self.current_track(tracks)
        if track == '+':
            if self.next_turn == TURN_LEFT:
                self.vector *= ROTATE_LEFT
            elif self.next_turn == TURN_RIGHT:
                self.vector *= ROTATE_RIGHT
            self.next_turn = (self.next_turn + 1) % 3
        elif track == '/':
            if self.vector == VECTOR_DOWN or self.vector == VECTOR_UP:
                self.vector *= ROTATE_RIGHT
            else:
                self.vector *= ROTATE_LEFT
        elif track == '\\':
            if self.vector == VECTOR_DOWN or self.vector == VECTOR_UP:
                self.vector *= ROTATE_LEFT
            else:
                self.vector *= ROTATE_RIGHT

        if self.position in carts:
            # Collision!
            return self.position

        # No collision
        carts[self.position] = self
        return None


def main():
    with open(sys.argv[1]) as f:
        grid = [line.strip('\n') for line in f.readlines()]

    cart_pattern = re.compile(r'[<>v^]')
    horizontal_cart_pattern = re.compile(r'[<>]')
    vertical_cart_pattern = re.compile(r'[v^]')
    carts: dict[Point, Cart] = {}
    tracks = []
    for y in range(len(grid)):
        row = grid[y]
        for match in cart_pattern.finditer(row):
            x = match.start()
            cart = Cart(x, y, match[0])
            carts[cart.position] = cart
        tracks.append(vertical_cart_pattern.sub('|', horizontal_cart_pattern.sub('-', row)))

    run_simulation(tracks, carts)


def run_simulation(tracks: list[str], carts: dict[Point, Cart]):
    first_collision = True
    for tick in itertools.count():
        for pos, cart in sorted(carts.items(), key=lambda item: (item[0].imag, item[0].real)):
            if collision_position := cart.step(tracks, carts):
                if first_collision:
                    print(f'{int(collision_position.real)},{int(collision_position.imag)}')
                    first_collision = False
                del carts[collision_position]
        if len(carts) == 1:
            last_position = next(iter(carts.keys()))
            print(f'{int(last_position.real)},{int(last_position.imag)}')
            break


if __name__ == '__main__':
    main()
