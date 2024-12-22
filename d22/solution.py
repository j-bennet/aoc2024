from functools import lru_cache
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def parse_data(data):
    return [int(x) for x in data]


@lru_cache(maxsize=None)
def mix(secret: int, val: int) -> int:
    """
    To mix a value into the secret number, calculate the bitwise XOR of the given value and
    the secret number. Then, the secret number becomes the result of that operation.
    """
    return secret ^ val


@lru_cache(maxsize=None)
def prune(secret: int) -> int:
    """
    To prune the secret number, calculate the value of the secret number modulo 16777216.
    Then, the secret number becomes the result of that operation.
    """
    return secret % 16777216


@lru_cache(maxsize=None)
def calculate_secret(secret):
    """
    In particular, each buyer's secret number evolves into the next secret number in the sequence via the
    following process:

    Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret
    number. Finally, prune the secret number.

    Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer.
    Then, mix this result into the secret number. Finally, prune the secret number.

    Calculate the result of multiplying the secret number by 2048. Then, mix this result into the
    secret number. Finally, prune the secret number.
    """
    val = secret * 64
    secret = prune(mix(secret, val))
    val = secret // 32
    secret = prune(mix(secret, val))
    val = secret * 2048
    secret = prune(mix(secret, val))
    return secret


def calculate_secret_n(secret, n):
    """
    Calculate the secret number after n iterations
    """
    for _ in range(n):
        secret = calculate_secret(secret)
    return secret


def part1(data):
    """Part 1"""
    initials = parse_data(data)
    total = 0
    for x in initials:
        result = calculate_secret_n(x, 2000)
        # print(f"{x}: {result}")
        total += result
    return total


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
