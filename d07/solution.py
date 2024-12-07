from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def check_equation(target, components, acc):
    if len(components) == 0:
        return target == acc
    return check_equation(
        target, components[1:], (0 if acc is None else acc) + components[0]
    ) or check_equation(
        target, components[1:], (1 if acc is None else acc) * components[0]
    )


def part1(data):
    """Part 1"""
    result = 0
    for line in data:
        target, components = line.strip().split(": ")
        target = int(target)
        components = list(map(int, components.split(" ")))
        if check_equation(target, components, None):
            result += target
    return result


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
