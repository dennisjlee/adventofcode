import sys

def main():
    expenses = set()
    with open(sys.argv[1]) as f:
        for line in f:
            expense = int(line.strip())
            complement = 2020 - expense
            if complement in expenses:
                print(complement * expense)
                return
            expenses.add(expense)


if __name__ == '__main__':
    main()
