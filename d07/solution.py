from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def combine(acc, x, op):
    if op == "+":
        acc = acc if acc is not None else 0
        return acc + x
    elif op == "*":
        acc = acc if acc is not None else 1
        return acc * x
    elif op == "||":
        acc = acc if acc is not None else 0
        remainder = x
        while remainder > 0:
            acc = acc * 10
            remainder = remainder // 10
        return acc + x


def check_equation(target, components, acc):
    if len(components) == 0:
        return target == acc
    return check_equation(
        target, components[1:], combine(acc, components[0], "+")
    ) or check_equation(target, components[1:], combine(acc, components[0], "*"))


def check_equation2(target, components, acc):
    if len(components) == 0:
        return target == acc
    return (
        check_equation2(target, components[1:], combine(acc, components[0], "+"))
        or check_equation2(target, components[1:], combine(acc, components[0], "*"))
        or check_equation2(target, components[1:], combine(acc, components[0], "||"))
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
    for line in data:
        target, components = line.strip().split(": ")
        target = int(target)
        components = list(map(int, components.split(" ")))
        if check_equation2(target, components, None):
            result += target
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
