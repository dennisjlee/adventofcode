import functools
from collections import defaultdict
from typing import Callable, Optional

@functools.cache
def alu0(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 1)
    x += 12
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    return z


@functools.cache
def alu1(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 1)
    x += 14
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 12
    y *= x
    z += y
    return z


@functools.cache
def alu2(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 1)
    x += 11
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    return z


@functools.cache
def alu3(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 26)
    x += -9
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 12
    y *= x
    z += y
    return z


@functools.cache
def alu4(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 26)
    x += -7
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    return z


@functools.cache
def alu5(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 1)
    x += 11
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 2
    y *= x
    z += y
    return z


@functools.cache
def alu6(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 26)
    x += -1
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 11
    y *= x
    z += y
    return z


@functools.cache
def alu7(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 26)
    x += -16
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    return z


@functools.cache
def alu8(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 1)
    x += 11
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 10
    y *= x
    z += y
    return z


@functools.cache
def alu9(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 26)
    x += -15
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 2
    y *= x
    z += y
    return z


@functools.cache
def alu10(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 1)
    x += 10
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 0
    y *= x
    z += y
    return z


@functools.cache
def alu11(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 1)
    x += 12
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 0
    y *= x
    z += y
    return z


@functools.cache
def alu12(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 26)
    x += -4
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    return z


@functools.cache
def alu13(d, z):
    x = y = 0
    w = d
    x *= 0
    x += z
    x = x % 26
    z = int(z / 26)
    x += 0
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    return z

@functools.cache
def s_alu12(d, z):
    x = z % 26
    z = int(z / 26)
    x1 = int(x - 4 != d)  # 0 or 1
    y = 25 * x1 + 1  # 26 or 1
    z *= y
    y1 = (d + 15) * x1
    z += y1
    return z


@functools.cache
def s_alu13(d, z):
    x = z % 26
    z = int(z / 26)
    x1 = int(x != d)  # 0 or 1
    y = 25 * x1 + 1  # 26 or 1
    z *= y
    y1 = (d + 15) * x1  # (d + 15) or 0
    z += y1
    return z


def main():
    alus = [alu0, alu1, alu2, alu3, alu4, alu5, alu6, alu7, alu8, alu9, alu10, alu11, alu12, alu13]

    work_backwards(alus)


def work_backwards(alus: list[Callable[[int, int], int]]):
    possible_inputs = [set() for _ in range(14)]
    possible_inputs[0].add(0)
    possible_outputs = [defaultdict(set) for _ in range(14)]

    for d in range(1, 10):
        # alu13 can only produce 0 using z inputs in this range
        for z_in in range(-26, 27):
            z_out = alus[13](d, z_in)
            # later d values will overwrite, so we'll be left with the highest
            if z_out == 0:
                possible_outputs[13][z_in].add((d, z_out))
                possible_inputs[13].add(z_in)

    for i in range(12, -1, -1):
        next_inputs = possible_inputs[i + 1]
        outputs = possible_outputs[i]
        for d in range(1, 10):
            for z_in in range(20000):
                z_out = alus[i](d, z_in)
                if z_out in next_inputs:
                    outputs[z_in].add((d, z_out))
        possible_inputs[i] = set(outputs.keys())

    # print([len(i) for i in possible_inputs])
    # print([len(o) for o in possible_outputs])
    # print(possible_inputs[0])
    # print(possible_outputs[0])

    model_number = find_highest_model_number(possible_outputs, 0, 0)
    print(''.join(str(d) for d in model_number))
    # print(execute(alus, model_number))

    # part 2
    model_number = find_lowest_model_number(possible_outputs, 0, 0)
    print(''.join(str(d) for d in model_number))
    # print(execute(alus, model_number))


def find_highest_model_number(possible_outputs: list[dict[int, set[tuple[int, int]]]], i: int, z_in: int) \
    -> Optional[list[int]]:

    if z_in not in possible_outputs[i]:
        return None

    for d, z_out in sorted(possible_outputs[i][z_in], reverse=True):
        if i == len(possible_outputs) - 1:
            return [d]
        subsolution = find_highest_model_number(possible_outputs, i + 1, z_out)
        if subsolution:
            return [d] + subsolution


def find_lowest_model_number(possible_outputs: list[dict[int, set[tuple[int, int]]]], i: int, z_in: int) \
        -> Optional[list[int]]:

    if z_in not in possible_outputs[i]:
        return None

    for d, z_out in sorted(possible_outputs[i][z_in]):
        if i == len(possible_outputs) - 1:
            return [d]
        subsolution = find_lowest_model_number(possible_outputs, i + 1, z_out)
        if subsolution:
            return [d] + subsolution


def execute(alus: list[Callable[[int, int], int]], digits: list[int]) -> list[int]:
    register_snapshots: list[int] = [0]
    for i, alu in enumerate(alus):
        register_snapshots.append(alu(digits[i], register_snapshots[i]))
    return register_snapshots


def brute_force(alus: list[Callable[[int, int], int]]):
    digits = [9] * 14
    register_snapshots: list[int] = [0]
    result = execute(alus, digits)[-1]
    if result == 0:
        print(''.join(str(d) for d in digits))
        return

    counter = 0
    while True:
        counter += 1
        if counter % 100000 == 0:
            print('currently trying number', ''.join(str(d) for d in digits))

        # if counter % 5_000_000 == 0:
        #     return

        for j in range(13, -1, -1):
            digits[j] = (digits[j] - 2) % 9 + 1
            if digits[j] < 9:
                for i in range(j, 14):
                    register_snapshots[i + 1] = alus[i](digits[i], register_snapshots[i])

                if register_snapshots[-1] == 0:
                    return int(''.join(str(d) for d in digits))
                break


if __name__ == '__main__':
    main()
