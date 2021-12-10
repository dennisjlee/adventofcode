import sys


def main():
    with open(sys.argv[1]) as f:
        depths = [int(line.strip()) for line in f.readlines()]

    increases = 0
    d_prev = None
    for d in depths:
        if d_prev is not None and d > d_prev:
            increases += 1
        d_prev = d

    print(increases)

    increases = 0
    w_prev = sum(depths[:3])
    for i in range(3, len(depths)):
        w = w_prev + depths[i] - depths[i-3]
        if w > w_prev:
            increases += 1
        w_prev = w
    print(increases)


if __name__ == '__main__':
    main()
