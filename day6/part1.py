import re
import sys

def main():
    with open(sys.argv[1]) as f:
        batch = f.read()

    total_yes_count = 0
    groups = batch.split('\n\n')
    for group in groups:
        distinct = set(group.replace('\n', ''))
        total_yes_count += len(distinct)

    print(total_yes_count)



if __name__ == '__main__':
    main()
