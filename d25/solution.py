from functools import cache
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        res = f.read().split("\n\n")
        return [x.split("\n") for x in res]


def parse_data(data):
    locks = set()
    keys = set()
    h = len(data[0]) - 1
    for chunk in data:
        if all(x == "#" for x in chunk[0]):
            # lock
            cols = [0] * len(chunk[0])
            for row in chunk[1:]:
                for i, c in enumerate(row):
                    if c == "#":
                        cols[i] += 1
            locks.add(tuple(cols))
        else:
            cols = [0] * len(chunk[0])
            for row in chunk[:-1]:
                for i, c in enumerate(row):
                    if c == "#":
                        cols[i] += 1
            keys.add(tuple(cols))
    return locks, keys, h


@cache
def is_match(lock, key, h):
    return all((x + y) < h for x, y in zip(lock, key))


def part1(data):
    """Part 1"""
    result = 0
    locks, keys, h = parse_data(data)
    for lock in sorted(locks):
        for key in reversed(sorted(keys)):
            if is_match(lock, key, h):
                # print(f"Lock {lock}: no overlap with key {key}")
                result += 1
            # else:
            # print(f"Lock {lock}: overlap with key {key}")
    return result


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
