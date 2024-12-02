from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def is_safe(report):
    prev_diff_sign = None
    for cur, nxt in zip(report, report[1:]):
        abs_diff = abs(cur - nxt)
        diff_sign = (cur - nxt) < 0
        if abs_diff > 3 or abs_diff < 1:
            return 0
        if prev_diff_sign is not None and prev_diff_sign != diff_sign:
            return 0
        prev_diff_sign = diff_sign
    return 1


def is_safe2(report):
    if is_safe(report):
        return 1
    for i in range(len(report)):
        subreport = report[:i] + report[i + 1 :]
        if is_safe(subreport):
            return 1
    return 0


def part1(data):
    """Part 1"""
    result = 0
    for line in data:
        report = list(map(int, line.strip().split()))
        result += is_safe(report)
    return result


def part2(data):
    """Part 2"""
    result = 0
    for line in data:
        report = list(map(int, line.strip().split()))
        result += is_safe2(report)
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
