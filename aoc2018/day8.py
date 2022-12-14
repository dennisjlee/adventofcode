import sys


class Node:
    child_count = 0
    metadata_count = 0
    children = None
    metadata = None

    def __init__(self, child_count, metadata_count):
        self.child_count = child_count
        self.metadata_count = metadata_count
        self.children = []

    def sum_metadata(self):
        own_sum = sum(self.metadata)
        return own_sum + sum(child.sum_metadata() for child in self.children)

    def value(self):
        if self.child_count == 0:
            return self.sum_metadata()

        value = 0
        for child_number in self.metadata:
            if 0 < child_number <= self.child_count:
                value += self.children[child_number - 1].value()
        return value


def main():
    with open(sys.argv[1]) as f:
        line = f.readline()
        numbers = [int(w) for w in line.split()]

    root, i = parse_tree(numbers, 0)

    # part 1
    print(root.sum_metadata())

    # part 2
    print(root.value())



def sum_metadata(node: Node):
    own_sum = sum(node.metadata)


def parse_tree(numbers: list[int], i: int) -> tuple[Node, int]:
    node = Node(numbers[i], numbers[i + 1])
    i += 2
    for _ in range(node.child_count):
        child, i = parse_tree(numbers, i)
        node.children.append(child)
    node.metadata = numbers[i:i + node.metadata_count]
    i += node.metadata_count
    return node, i


if __name__ == '__main__':
    main()
