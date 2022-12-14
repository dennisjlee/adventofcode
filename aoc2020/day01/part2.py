import sys

def main():
    expenses = set()
    partially_computed = {}
    with open(sys.argv[1]) as f:
        for line in f:
            expense = int(line.strip())
            complement = 2020 - expense
            if complement in partially_computed:
                print(expense * partially_computed[complement])
                return
            for other in expenses:
                partially_computed[expense + other] = expense * other
            expenses.add(expense)


if __name__ == '__main__':
    main()
