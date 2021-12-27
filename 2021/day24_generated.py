import functools
from collections import defaultdict
from typing import Callable


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
    y += 16
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
def alu13_simplified(d, z):
    x = z % 26
    z = int(z / 26)
    x1 = int(x != d)  # 0 or 1
    y = 25 * x1 + 1   # 26 or 1
    z *= y
    y1 = (d + 15) * x1 # (d + 15) or 0
    z += y1
    return z


def main():
    alus = [alu0, alu1, alu2, alu3, alu4, alu5, alu6, alu7, alu8, alu9, alu10, alu11, alu12, alu13]

    work_backwards(alus)


def work_backwards(alus: list[Callable[[int, int], int]]):
    possible_inputs = [{0}]
    possible_outputs = []
    for i in range(14):
        outputs = {}
        possible_outputs.append(outputs)
        for d in range(1, 10):
            for z_in in possible_inputs[i]:
                z_out = alus[i](d, z_in)

                key = (z_in, z_out)
                # later d values will overwrite, so we'll be left with the highest
                outputs[(z_in, z_out)] = d

        possible_inputs.append({output_key[1] for output_key in outputs.keys()})

        print('possible inputs:', i, len(possible_inputs[i]))
        print('possible outputs:', i, len(possible_outputs[i]))


def brute_force(alus: list[Callable[[int, int], int]]):
    digits = [9] * 14
    register_snapshots: list[int] = [0]
    for i, alu in enumerate(alus):
        register_snapshots.append(alu(digits[i], register_snapshots[i]))
    if register_snapshots[-1] == 0:
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
