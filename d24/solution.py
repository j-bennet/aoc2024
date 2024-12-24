import copy
from os import path

import networkx as nx
from networkx import DiGraph

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def simulate(g, wires, gates):
    """Calculate all z-gate values"""
    values = copy.deepcopy(wires)
    for node in nx.topological_sort(g):
        if node in wires:
            continue
        operand1, operation, operand2 = gates[node]
        if operation == "AND":
            values[node] = values[operand1] & values[operand2]
        elif operation == "OR":
            values[node] = values[operand1] | values[operand2]
        elif operation == "XOR":
            values[node] = values[operand1] ^ values[operand2]
        else:
            raise ValueError(f"Unknown operation: {operation}")
    return values


def calculate_output(values):
    z_values = sorted([(k, v) for k, v in values.items() if k.startswith("z")])
    out_value = 0
    for i, (k, v) in enumerate(z_values):
        out_value += v << i
    return out_value


def parse_data(data):
    wires = {}
    gates = {}
    g = DiGraph()
    for line in data:
        if not line:
            continue
        if ":" in line:
            name, value = line.split(": ")
            wires[name] = int(value)
            g.add_node(name, value=int(value))
        elif "->" in line:
            gate, output = line.split(" -> ")
            operand1, operation, operand2 = gate.split(" ")
            gates[output] = (operand1, operation, operand2)
            g.add_edge(operand1, output)
            g.add_edge(operand2, output)
    return g, wires, gates


def part1(data):
    """Part 1"""
    result = 0
    g, wires, gates = parse_data(data)
    values = simulate(g, wires, gates)
    result = calculate_output(values)
    return result


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
