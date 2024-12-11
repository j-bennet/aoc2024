from dataclasses import dataclass
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


@dataclass
class Stone:
    n: int

    def __repr__(self):
        return str(self.n)

    def __str__(self):
        return self.__repr__()

    def split(self):
        digits = list(str(self.n))
        m = len(digits) // 2
        left_digits = digits[:m]
        right_digits = digits[m:]
        left = int("".join(left_digits))
        right = int("".join(right_digits))
        return [Stone(left), Stone(right)]


def blink(stones: list[Stone]) -> list[Stone]:
    result = []
    for stone in stones:
        if stone.n == 0:
            result.append(Stone(1))
        elif len(str(stone.n)) % 2 == 0:
            result.extend(stone.split())
        else:
            result.append(Stone(stone.n * 2024))
    return result


def part1(data):
    """Part 1"""
    stones = [Stone(int(x)) for x in data[0].split()]
    for i in range(25):
        stones = blink(stones)
    return len(stones)


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
