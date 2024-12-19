from functools import lru_cache
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


@lru_cache(None)
def is_possible(search_string: str, patterns: frozenset[str]) -> bool:
    if len(search_string) == 0:
        return True
    for pattern in patterns:
        if search_string.startswith(pattern):
            if is_possible(search_string[len(pattern) :], patterns):
                return True
    return False


@lru_cache(None)
def count_ways(search_string: str, patterns: frozenset[str]) -> int:
    if len(search_string) == 0:
        return 1
    total_ways = 0
    for pattern in patterns:
        if search_string.startswith(pattern):
            total_ways += count_ways(search_string[len(pattern) :], patterns)
    return total_ways


def parse_data(data):
    patterns = data[0].split(", ")
    designs = [line for line in data[1:] if line]
    return patterns, designs


def part1(data):
    """Part 1"""
    patterns, designs = parse_data(data)
    patterns = frozenset(patterns)
    count = 0
    for design in designs:
        if is_possible(design, patterns):
            count += 1
        #     print(f"+: {design}")
        # else:
        #     print(f"-: {design}")
    return count


def part2(data):
    """Part 2"""
    patterns, designs = parse_data(data)
    patterns = set(patterns)
    count = 0
    for design in designs:
        # print(f"Design: {design}")
        ways = count_ways(design, frozenset(patterns))
        # print(f"    Ways: {ways}")
        count += ways
    return count


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
