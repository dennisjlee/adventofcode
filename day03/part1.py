import sys

def main():
    with open(sys.argv[1]) as f:
        tree_grid = [l.strip() for l in f.readlines()]

    width = len(tree_grid[0])
    height = len(tree_grid)
    trees_encountered = sum(
        1 if tree_grid[r][(r * 3) % width] == '#' else 0
        for r in range(1, height)
    )

    print(trees_encountered)


if __name__ == '__main__':
    main()
