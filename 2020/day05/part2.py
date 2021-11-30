import re
import sys

def main():
    with open(sys.argv[1]) as f:
        boarding_passes = [l.strip() for l in f]
    all_seat_ids = [seat_id(bp) for bp in boarding_passes]
    all_seat_ids.sort()
    for i in range(len(all_seat_ids) - 1):
        if all_seat_ids[i+1] > all_seat_ids[i] + 1:
            print(all_seat_ids[i] + 1)
            return


def seat_id(boarding_pass):
    binary = re.sub('[BR]', '1', re.sub('[FL]', '0', boarding_pass))
    return int(binary, 2)


if __name__ == '__main__':
    main()
