import re
import sys

digits = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}


digit_re = re.compile(f'\\d|{"|".join(digits.keys())}')

def main():
    total1 = 0
    total2 = 0


    with open(sys.argv[1]) as f:
        for line in f.readlines():
            line = line.strip()
            first_digit = re.search(r'\d', line).group(0)
            last_digit = re.search(r'(\d)\D*$', line).group(1)
            total1 += 10 * int(first_digit) + int(last_digit)
            total2 += parse2(line)

    print(total1)
    print(total2)

    print(parse2('4nineeightseven2'))
    print(parse2('zoneight234'))
    print(parse2('zoneight'))


def parse2(line: str) -> int:
    match = digit_re.search(line)
    first_digit = clean_digit(match.group(0))
    while match:
        last_digit = clean_digit(match.group(0))
        match = digit_re.search(line, match.start() + 1)

    return 10 * first_digit + last_digit


def clean_digit(digit: str) -> int:
    return digits[digit] if digit in digits else int(digit)


if __name__ == '__main__':
    main()
