import functools


@functools.cache
def alu0(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu1(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu2(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu3(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu4(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu5(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu6(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu7(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu8(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu9(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu10(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu11(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu12(d, w, x, y, z):
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
    return w, x, y, z


@functools.cache
def alu13(d, w, x, y, z):
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
    return w, x, y, z


def main():
    digits = [9] * 14

    alus = [alu0, alu1, alu2, alu3, alu4, alu5, alu6, alu7, alu8, alu9, alu10, alu11, alu12, alu13]

    register_snapshots: list[tuple[int, int, int, int]] = [(0, 0, 0, 0)]
    for i, alu in enumerate(alus):
        register_snapshots.append(alu(digits[i], *register_snapshots[i]))
    if register_snapshots[-1][-1] == 0:
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
                    register_snapshots[i + 1] = alus[i](digits[i], *register_snapshots[i])

                if register_snapshots[-1][-1] == 0:
                    print(''.join(str(d) for d in digits))
                    return
                break


if __name__ == '__main__':
    main()
