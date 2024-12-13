from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def parse_data(data):
    machines = []

    machine = {}
    for line in data:
        line = line.strip()
        if not line:
            if machine:
                machines.append(machine)
            machine = {}
        if line.startswith("Button A:"):
            ax, ay = line.split(": ")[1].split(", ")
            machine["a1"] = int(ax.split("+")[1])
            machine["a2"] = int(ay.split("+")[1])
        elif line.startswith("Button B:"):
            bx, by = line.split(": ")[1].split(", ")
            machine["b1"] = int(bx.split("+")[1])
            machine["b2"] = int(by.split("+")[1])
        elif line.startswith("Prize:"):
            px, py = line.split(": ")[1].split(", ")
            machine["c1"] = int(px.split("=")[1])
            machine["c2"] = int(py.split("=")[1])
    if machine:
        machines.append(machine)
    return machines


def solve(coefficients: dict):
    # # Coefficients of the equations
    a1, b1, c1 = coefficients["a1"], coefficients["b1"], coefficients["c1"]
    a2, b2, c2 = coefficients["a2"], coefficients["b2"], coefficients["c2"]

    # Calculate the determinant
    determinant = a1 * b2 - a2 * b1

    # Solve for a and b using Cramer's rule
    if determinant != 0:
        a = (c1 * b2 - c2 * b1) / determinant
        b = (a1 * c2 - a2 * c1) / determinant
        if int(a) == a and int(b) == b:
            return int(a), int(b)
    return None, None


def part1(data):
    """Part 1"""
    machines = parse_data(data)
    costs = []
    for machine in machines:
        a, b = solve(machine)
        if a is not None and b is not None:
            costs.append(a * 3 + b)
    return sum(costs)


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
