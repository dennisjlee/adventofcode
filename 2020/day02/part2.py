import re
import sys

def main():
    line_regex = re.compile(r'^(\d+)-(\d+) ([a-z]): ([a-z]+)$')

    valid_password_count = 0

    with open(sys.argv[1]) as f:
        for line in f:
            match = line_regex.match(line)
            if match:
                position1, position2, letter, password = match.groups()
                index1 = int(position1) - 1
                index2 = int(position2) - 1
                if (password[index1] == letter) != (password[index2] == letter):
                    valid_password_count += 1

    print(valid_password_count)


if __name__ == '__main__':
    main()
