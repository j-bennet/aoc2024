from functools import lru_cache
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


@lru_cache(maxsize=None)
def split(n):
    if n == 0:
        return [1]
    elif len(str(n)) % 2 == 0:
        digits = str(n)
        m = len(digits) // 2
        left_digits = digits[:m]
        right_digits = digits[m:]
        left = int(left_digits)
        right = int(right_digits)
        return [left, right]
    else:
        return [n * 2024]


@lru_cache(maxsize=None)
def blink_for(stone, i):
    if i == 0:
        return 1
    result = 0
    for n in split(stone):
        result += blink_for(n, i - 1)
    return result


def blink(stones: list[int]) -> list[int]:
    result = []
    for stone in stones:
        if stone == 0:
            result.append(1)
        elif len(str(stone)) % 2 == 0:
            result.extend(split(stone))
        else:
            result.append(stone * 2024)
    return result


def part1(data):
    """Part 1"""
    stones = [int(x) for x in data[0].split()]
    result = 0
    for stone in stones:
        result += blink_for(stone, 25)
    return result
    # for i in range(25):
    #     stones = blink(stones)
    # return len(stones)


def part2(data):
    """Part 2"""
    stones = [int(x) for x in data[0].split()]
    result = 0
    for stone in stones:
        result += blink_for(stone, 75)
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
