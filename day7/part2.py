from collections import namedtuple
import re
import sys

toplevel_regex = re.compile(r'(.*?) bags contain (.*)')
contents_regex = re.compile(r'(\d+) (.*?) bags?[,\.]')

class BagNode():
    def __init__(self, color):
        self.color = color
        self.contents = {}
        self.ancestors = set()

    def set_contents(self, content_tuples):
        self.contents = {
            content_color: int(number) for number, content_color in content_tuples
        }

nodes = {}

def get_bag(color):
    return nodes.setdefault(color, BagNode(color))

def main():
    with open(sys.argv[1]) as f:
        for line in f:
            toplevel_match = toplevel_regex.match(line.strip())
            color, contents = toplevel_match.groups()
            content_tuples = contents_regex.findall(contents)

            get_bag(color).set_contents(content_tuples)

            for _, content_bag in content_tuples:
                get_bag(content_bag).ancestors.add(color)

    print(get_total_count(get_bag('shiny gold')))


def get_total_count(bag):
    total = 1  # the bag itself
    for content_color, number in bag.contents.items():
        subtotal = get_total_count(get_bag(content_color))
        total += number * subtotal
    return total


if __name__ == '__main__':
    main()
