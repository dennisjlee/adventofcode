import sys


def main():
    gamma = 0
    epsilon = 0

    with open(sys.argv[1]) as f:
        numbers = [line.strip() for line in f.readlines()]

    n = len(numbers)
    num_bits = len(numbers[0])
    for i in range(num_bits):
        ones_count = count_one_bits(i, numbers)
        if ones_count > n/2:
            gamma |= 1 << (num_bits - i - 1)
        else:
            epsilon |= 1 << (num_bits - i - 1)

    print(f'{gamma:08b}', f'{epsilon:08b}')
    print(gamma * epsilon)

    # part 2
    oxygen_numbers = numbers[:]
    co2_numbers = numbers[:]
    for i in range(num_bits):
        ones_count = count_one_bits(i, oxygen_numbers)
        if ones_count >= len(oxygen_numbers) / 2:
            oxygen_numbers = [num for num in oxygen_numbers if num[i] == '1']
        else:
            oxygen_numbers = [num for num in oxygen_numbers if num[i] == '0']
        if len(oxygen_numbers) == 1:
            break

    for i in range(num_bits):
        ones_count = count_one_bits(i, co2_numbers)
        if ones_count >= len(co2_numbers) / 2:
            co2_numbers = [num for num in co2_numbers if num[i] == '0']
        else:
            co2_numbers = [num for num in co2_numbers if num[i] == '1']
        if len(co2_numbers) == 1:
            break

    oxygen_rating = int(oxygen_numbers[0], 2)
    co2_rating = int(co2_numbers[0], 2)
    print(f'{oxygen_rating:08b}', f'{co2_rating:08b}')
    print(oxygen_rating * co2_rating)


def count_one_bits(i, binary_strings):
    return sum(1 for num in binary_strings if num[i] == '1')


if __name__ == '__main__':
    main()
