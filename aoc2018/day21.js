function f() {
  let [r1, r2, r3, r5] = [0, 0, 0, 0];
  r1 = 123
  do {
    r1 &= 456
    r1 = (r1 === 72) ? 1 : 0
  } while (r1 === 0)
  r1 = 0

  const r1Values = [];

  while (true) {
    r5 = r1 | 65536          // 1 followed by 16x 0
    r1 = 8586263

    while (true) {
      r2 = r5 & 255            // 0 the first time
      r1 += r2

      // 16777215 is 24 bits of 1s
      r1 &= 16777215           // 8586263 the first time.
      r1 *= 65899
      r1 &= 16777215           // 14535837 the first time

      if (r5 < 256) {
        break;
      }
      r2 = Math.floor(r5 / 256);
      r5 = r2;
    }
    if (r1Values.includes(r1)) {
      console.log('part2:', r1Values[r1Values.length - 1]);
      return;
    } else {
      r1Values.push(r1);
    }
    if (r1Values.length === 1) {
      console.log('part1:', r1Values[0]);
    }
  }
}

f();