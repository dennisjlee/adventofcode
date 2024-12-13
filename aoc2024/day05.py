import math
import sys
from collections import defaultdict, deque


def main():
    with open(sys.argv[1]) as f:
        rules_str, updates_str = f.read().split("\n\n")

    ordering_rules: dict[int, set[int]] = defaultdict(set)
    for line in rules_str.strip().split("\n"):
        s1, s2 = line.split("|")
        ordering_rules[int(s1)].add(int(s2))

    updates: list[list[int]] = []
    for line in updates_str.strip().split("\n"):
        words = line.split(",")
        updates.append([int(w) for w in words])

    result1 = 0
    result2 = 0
    for update in updates:
        if is_correctly_ordered(update, ordering_rules):
            result1 += update[len(update) // 2]
        else:
            fixed = topological_sort(update, ordering_rules)
            result2 += fixed[len(fixed) // 2]
    print(result1)
    print(result2)


def is_correctly_ordered(
    update: list[int], ordering_rules: dict[int, set[int]]
) -> bool:
    indexed = {n: i for i, n in enumerate(update)}
    for n, n_i in indexed.items():
        for m in ordering_rules[n]:
            m_i = indexed.get(m, math.inf)
            if m_i < n_i:
                return False
    return True


def topological_sort(
    update: list[int], ordering_rules: dict[int, set[int]]
) -> list[int]:
    members = set(update)
    filtered_rules = {
        n: dependents & members
        for n, dependents in ordering_rules.items()
        if n in members
    }

    visited: dict[int, bool] = {}
    result: deque[int] = deque([])

    def visit(n: int):
        if visited.get(n):
            return
        # assume there are no cycles
        for m in filtered_rules.get(n, ()):
            visit(m)
        visited[n] = True
        result.appendleft(n)

    for n in update:
        visit(n)

    return list(result)


if __name__ == "__main__":
    main()
