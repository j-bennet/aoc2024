import re
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def part1(data):
    """Part 1"""
    result = 0
    for line in data:
        instrs = re.findall(r"mul\((\d{1,3},\d{1,3})\)", line)
        for instr in instrs:
            x, y = instr.split(",")
            result += int(x) * int(y)
    return result


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
