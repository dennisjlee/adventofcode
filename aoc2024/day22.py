import sys
from collections import deque, defaultdict


def evolve_secret(secret: int) -> int:
    secret = (secret ^ (secret * 64)) % 16777216
    secret = (secret ^ (secret // 32)) % 16777216
    return (secret ^ (secret * 2048)) % 16777216


MASK = (1 << 24) - 1


def evolve_secret_bitwise(secret: int) -> int:
    secret = (secret ^ (secret << 6)) & MASK
    secret = (secret ^ (secret >> 5)) & MASK
    return (secret ^ (secret << 11)) & MASK


def main():
    with open(sys.argv[1]) as f:
        seeds = [int(l.strip()) for l in f.readlines()]

    result1 = 0
    total_selling_prices: dict[tuple[int, ...], int] = defaultdict(int)
    for seed in seeds:
        selling_prices: set[tuple[int, ...]] = set()
        price_window: deque[int] = deque([seed % 10], maxlen=5)
        delta_window: deque[int] = deque(maxlen=4)
        for _ in range(2000):
            seed = evolve_secret_bitwise(seed)
            price = seed % 10
            delta_window.append(price - price_window[-1])
            price_window.append(price)
            if len(delta_window) == 4:
                price_key = tuple(delta_window)
                if price_key not in selling_prices:
                    selling_prices.add(price_key)
                    total_selling_prices[price_key] += price
        result1 += seed

    print(result1)

    print(max(total_selling_prices.values()))


if __name__ == "__main__":
    main()
