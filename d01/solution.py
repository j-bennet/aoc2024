from collections import Counter
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def parse_data(data):
    l1 = []
    l2 = []
    for line in data:
        x, y = line.strip().split()
        x = int(x)
        y = int(y)
        l1.append(x)
        l2.append(y)
    return l1, l2


def part1(data):
    """Part 1"""
    l1, l2 = parse_data(data)
    l1 = sorted(l1)
    l2 = sorted(l2)
    result = 0
    for x, y in zip(l1, l2):
        result += abs(x - y)
    return result


def part2(data):
    """Part 2"""
    l1, l2 = parse_data(data)
    cnt = Counter(l2)
    result = 0
    for x in l1:
        if x in cnt:
            result += x * cnt[x]
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
