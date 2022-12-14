from __future__ import annotations
from collections import Counter, deque
import sys
import timeit

def main():
    with open(sys.argv[1]) as f:
        buffer = f.read().strip()

    print('easy way', easy_way(buffer, 4), easy_way(buffer, 14))
    print('easy way time', timeit.timeit(lambda: easy_way(buffer, 14), number=1000))
    print('hard way', hard_way(buffer, 4), hard_way(buffer, 14))
    print('hard way time', timeit.timeit(lambda: hard_way(buffer, 14), number=1000))
    print('deque way', deque_way(buffer, 4), deque_way(buffer, 14))
    print('deque way time', timeit.timeit(lambda: deque_way(buffer, 14), number=1000))
    print('dedupe way', dedupe_way(buffer, 4), dedupe_way(buffer, 14))
    print('dedupe way time', timeit.timeit(lambda: dedupe_way(buffer, 14), number=1000))


def easy_way(buffer, n):
    for i in range(n, len(buffer)):
        test = set(buffer[i-n:i])
        if len(test) == n:
            return i


def hard_way(buffer, n):
    counter = Counter(buffer[:n])
    for i in range(n, len(buffer)):
        if len(counter) == n:
            return i
        left = buffer[i-n]
        counter[left] -= 1
        if counter[left] == 0:
            del counter[left]
        counter[buffer[i]] += 1


def deque_way(buffer, n):
    dq = deque(buffer[:n])
    for i in range(n, len(buffer)):
        if len(set(dq)) == n:
            return i
        dq.popleft()
        dq.append(buffer[i])


def dedupe_way(buffer, n):
    for i in range(n, len(buffer)):
        s = {buffer[i-n]}
        for j in range(i-n+1, i):
            if buffer[j] in s:
                break
            s.add(buffer[j])
        else:
            return i


if __name__ == '__main__':
    main()
