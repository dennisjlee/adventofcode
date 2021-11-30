import re
import sys

def main():
    line_regex = re.compile(r'^(\d+)-(\d+) ([a-z]): ([a-z]+)$')

    valid_password_count = 0

    with open(sys.argv[1]) as f:
        for line in f:
            match = line_regex.match(line)
            if match:
                min_count, max_count, letter, password = match.groups()
                count = sum(1 for c in password if c == letter)
                if int(min_count) <= count <= int(max_count):
                    valid_password_count += 1

    print(valid_password_count)


if __name__ == '__main__':
    main()
