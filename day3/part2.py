import sys

def main():
    with open(sys.argv[1]) as f:
        tree_grid = [l.strip() for l in f.readlines()]

    result = (trees_encountered(tree_grid, 1, 1) *
        trees_encountered(tree_grid, 1, 3) *
        trees_encountered(tree_grid, 1, 5) *
        trees_encountered(tree_grid, 1, 7) *
        trees_encountered(tree_grid, 2, 1))

    print(result)


def trees_encountered(tree_grid, down_increment, right_increment):
    width = len(tree_grid[0])
    height = len(tree_grid)
    return sum(
        1 if tree_grid[r][(r * right_increment) % width] == '#' else 0
        for r in range(1, height, down_increment)
    )


if __name__ == '__main__':
    main()
