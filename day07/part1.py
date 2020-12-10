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
            content_color: number for number, content_color in content_tuples
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

    to_visit = get_bag('shiny gold').ancestors.copy()
    seen = set()
    while to_visit:
        color = to_visit.pop()
        seen.add(color)
        to_visit |= get_bag(color).ancestors - seen

    print(len(seen))




if __name__ == '__main__':
    main()
