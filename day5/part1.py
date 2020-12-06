import re
import sys

def main():
    with open(sys.argv[1]) as f:
        boarding_passes = [l.strip() for l in f]
        print(max(seat_id(bp) for bp in boarding_passes))

def seat_id(boarding_pass):
    binary = re.sub('[BR]', '1', re.sub('[FL]', '0', boarding_pass))
    return int(binary, 2)


if __name__ == '__main__':
    main()
