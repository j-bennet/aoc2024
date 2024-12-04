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

    def _iterate():
        for line in data:
            line = re.sub(r"do\(\)", r"\n\g<0>\n", line)
            line = re.sub(r"don't\(\)", r"\n\g<0>\n", line)
            for sub_line in line.splitlines():
                yield sub_line

    result = 0
    current_mode = True
    for line in _iterate():
        if line == "do()":
            current_mode = True
        elif line == "don't()":
            current_mode = False
        elif current_mode:
            instrs = re.findall(r"mul\((\d{1,3},\d{1,3})\)", line)
            for instr in instrs:
                x, y = instr.split(",")
                result += int(x) * int(y)
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
