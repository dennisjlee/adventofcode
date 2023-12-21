import sys

FORWARD_DIRECTIONS = [
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]


class Seat:
    def __init__(self, occupied):
        self.occupied_now = occupied
        self.occupied_next = occupied
        self.neighbors = []

    def is_changed(self):
        return self.occupied_next == self.occupied_now


def main():
    with open(sys.argv[1]) as f:
        waiting_room = [list(l.strip()) for l in f]

    # part 1
    part1_seats = build_seat_graph(waiting_room, get_neighbor_part1)

    changed = True
    while changed:
        changed = iterate_seats(part1_seats, occupied_limit=4)
    print(count_occupied(part1_seats))

    # part 2
    part2_seats = build_seat_graph(waiting_room, get_neighbor_part2)
    changed = True
    while changed:
        changed = iterate_seats(part2_seats, occupied_limit=5)
    print(count_occupied(part2_seats))


def count_occupied(seats_by_coord):
    return sum(1 for seat in seats_by_coord.values() if seat.occupied_now)


def get_or_add_seat(room, seats_by_coord, y, x):
    coord = (y, x)
    seat = seats_by_coord.get(coord)
    if not seat:
        seat = Seat(occupied=(room[y][x] == '#'))
        seats_by_coord[coord] = seat
    return seat


def build_seat_graph(room, get_neighbor_for_direction):
    height = len(room)
    width = len(room[0])

    seats_by_coord = {}

    for y in range(height):
        for x in range(width):
            cur = room[y][x]
            if cur == '.':
                continue
            seat = get_or_add_seat(room, seats_by_coord, y, x)
            # Only look in half the directions, and trust that seats we iterated
            # over earlier would have established neighbor relationships in the
            # "backwards" directions by the time we get to any given seat
            for direction in FORWARD_DIRECTIONS:
                neighbor_coord = get_neighbor_for_direction(room, y, x, height, width, direction)
                if neighbor_coord:
                    ny, nx = neighbor_coord
                    neighbor_seat = get_or_add_seat(room, seats_by_coord, ny, nx)
                    seat.neighbors.append(neighbor_seat)
                    neighbor_seat.neighbors.append(seat)

    return seats_by_coord


def get_neighbor_part1(room, y, x, height, width, direction):
    dy, dx = direction
    ny = y + dy
    nx = x + dx
    if 0 <= ny < height and 0 <= nx < width and room[ny][nx] != '.':
        return ny, nx
    return None


def get_neighbor_part2(room, y, x, height, width, direction):
    dy, dx = direction
    ny = y
    nx = x

    while True:
        ny += dy
        nx += dx
        if 0 <= ny < height and 0 <= nx < width:
            if room[ny][nx] != '.':
                return ny, nx
        else:
            # out of bounds
            return None


def iterate_seats(seats_by_coord, occupied_limit):
    any_change = False
    for seat in seats_by_coord.values():
        if seat.occupied_now:
            count = 0
            seat.occupied_next = True
            for neighbor in seat.neighbors_bounded:
                if neighbor.occupied_now:
                    count += 1
                if count >= occupied_limit:
                    any_change = True
                    seat.occupied_next = False
                    break
        else:
            seat.occupied_next = True
            for neighbor in seat.neighbors_bounded:
                if neighbor.occupied_now:
                    seat.occupied_next = False
                    break
            if seat.occupied_next:
                any_change = True

    for seat in seats_by_coord.values():
        seat.occupied_now = seat.occupied_next

    return any_change


if __name__ == '__main__':
    main()
