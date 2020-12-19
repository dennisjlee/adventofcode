import re
from operator import add, mul
import sys
from typing import List, Union, Optional


OPERATORS = {
    '+': add,
    '*': mul
}
TOKENIZER = re.compile(r'(\(*)(\d+)(\)*)')
PAREN_GROUP = re.compile(r'\(([^()]*)\)')


def main():
    with open(sys.argv[1]) as f:
        expressions = [l.strip() for l in f]

    part1_orig(expressions)
    part1(expressions)
    part2(expressions)


def part1_orig(expressions):
    print(sum(eval_part1(expression) for expression in expressions))


def part1(expressions):
    print(sum(parse_to_tree2(expression) for expression in expressions))


def part2(expressions):
    print(sum(parse_to_tree2(expression, True) for expression in expressions))


class Node:
    def __init__(self, plus_takes_precedence: bool):
        self.parent: Optional[Node] = None
        self.left: Union[int, Node, None] = None
        self.operator: Optional[str] = None
        self.right: Union[int, Node, None] = None
        self.closed = False
        self.plus_takes_precedence = plus_takes_precedence

    def __repr__(self):
        open = '[' if self.closed else '('
        close = ']' if self.closed else ')'
        return f'{open}{repr(self.left)} {self.operator} {repr(self.right)}{close}'

    def evaluate(self) -> int:
        assert self.left is not None
        left = self.left if type(self.left) is int else self.left.evaluate()
        if self.right is None:
            return left
        assert self.operator is not None
        right = self.right if type(self.right) is int else self.right.evaluate()
        return OPERATORS[self.operator](left, right)

    def set_operator(self, operator: str):
        if self.operator is None:
            self.operator = operator
            return self
        new_node = Node(self.plus_takes_precedence)
        new_node.operator = operator
        if self.plus_takes_precedence and self.operator == '*' and operator == '+' and not self.closed:
            # new operator is + which takes precedence over *, so new node becomes right child of current node
            new_node.parent = self
            new_node.left = self.right
            self.right = new_node
        else:
            # just left-to-right precedence; current node becomes left child of new node
            new_node.parent = self.parent
            if self.parent:
                self.parent.swap_children(self, new_node)
            self.parent = new_node
            new_node.left = self
        return new_node

    def add_child_node(self):
        child = Node(self.plus_takes_precedence)
        child.parent = self
        if self.operator is None:
            self.left = child
        else:
            self.right = child
        return child

    def add_number(self, number: int):
        if self.operator is None:
            self.left = number
        else:
            self.right = number
        return self

    def create_parent(self):
        old_parent = self.parent
        self.parent = Node(self.plus_takes_precedence)
        self.parent.left = self
        if old_parent:
            old_parent.swap_children(self, self.parent)
        self.parent.parent = old_parent
        return self.parent

    def get_or_create_parent(self):
        if self.parent is None:
            return self.create_parent()
        return self.parent

    def swap_children(self, old_child, new_child):
        if self.left == old_child:
            self.left = new_child
        elif self.right == old_child:
            self.right = new_child
        else:
            assert False, "Couldn't find old child"


def parse_to_tree1(expression, plus_takes_precedence=False):
    root = Node(plus_takes_precedence)
    curr = root
    for token in expression.split(' '):
        if token in OPERATORS:
            new_node = curr.set_operator(token)
            if new_node.parent is None:
                root = new_node
            curr = new_node
        else:
            match = TOKENIZER.match(token)
            left_parens = match.group(1)
            number = int(match.group(2))
            right_parens = match.group(3)
            for _ in left_parens:
                curr = curr.add_child_node()

            new_node = curr.add_number(number)
            if new_node.parent is None:
                root = new_node
            curr = new_node

            for _ in right_parens:
                did_close = False
                if not did_close and curr.right is not None:
                    did_close = True
                    curr.closed = True
                curr = curr.get_or_create_parent()
                if not did_close and curr.right is not None:
                    curr.closed = True

    return root.evaluate()


def evaluate_tree(expression, plus_takes_precedence=False):
    root = Node(plus_takes_precedence)
    curr = root
    for token in expression.split(' '):
        if token in OPERATORS:
            new_node = curr.set_operator(token)
            if new_node.parent is None:
                root = new_node
            curr = new_node
        else:
            number = int(token)

            new_node = curr.add_number(number)
            if new_node.parent is None:
                root = new_node
            curr = new_node

    return root.evaluate()


def parse_to_tree2(expression, plus_takes_precedence=False):
    match = PAREN_GROUP.search(expression)
    while match:
        inner_expression = match.group(1)
        inner_value = evaluate_tree(inner_expression, plus_takes_precedence)
        expression = f'{expression[:match.start()]}{inner_value}{expression[match.end():]}'
        match = PAREN_GROUP.search(expression)

    return evaluate_tree(expression, plus_takes_precedence)


def eval_part1(expression):
    """Evaluate part1 by parsing the expression in a linear fashion .. a bit overly complex"""
    stacks: List[List[Union[int, str]]] = [[]]
    for token in expression.split(' '):
        if token in OPERATORS:
            stacks[-1].append(token)
        else:
            match = TOKENIZER.match(token)
            left_parens = match.group(1)
            number = int(match.group(2))
            right_parens = match.group(3)
            for _ in left_parens:
                stacks.append([])
            cur_stack = stacks[-1]
            cur_stack.append(number)
            eval_one_operation1(cur_stack)
            for _ in right_parens:
                assert len(cur_stack) == 1
                stacks.pop()
                if len(stacks) == 0:
                    stacks.append([])
                stacks[-1].append(cur_stack[0])
                cur_stack = stacks[-1]
                eval_one_operation1(cur_stack)
    assert len(stacks) == 1
    assert len(stacks[0]) == 1
    return stacks[0][0]


def eval_one_operation1(stack):
    if len(stack) >= 3 and stack[-2] in OPERATORS:
        operand2 = stack.pop()
        fn = OPERATORS[stack.pop()]
        operand1 = stack.pop()
        stack.append(fn(operand1, operand2))


if __name__ == '__main__':
    main()
