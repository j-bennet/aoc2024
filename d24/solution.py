import copy
from os import path
from typing import NamedTuple

import networkx as nx
from networkx import DiGraph

ROOT_DIR = path.dirname(__file__)

"""
For part 2, credit to:
https://github.com/D3STNY27/advent-of-code-2024/blob/main/day-24/part-2.py#L20
"""


class Gate(NamedTuple):
    operand1: str
    operation: str
    operand2: str

    def __str__(self):
        return f"{self.operand1} {self.operation} {self.operand2}"

    def __repr__(self):
        return f"{self.operand1} {self.operation} {self.operand2}"


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
    outputs = {k: v for k, v in values.items() if k not in wires}
    return values, outputs


def calculate_output(values):
    z_values = sorted([(k, v) for k, v in values.items() if k.startswith("z")])
    out_value = 0
    for i, (k, v) in enumerate(z_values):
        out_value += v << i
    return out_value


def get_ith_bit(number, i):
    """Get the ith bit of a number."""
    return (number >> i) & 1


def find_gate(
    x_wire: str, y_wire: str, gate_type: str, configurations: dict[str, Gate]
) -> str | None:
    rev_config = {v: k for k, v in configurations.items()}
    if Gate(x_wire, gate_type, y_wire) in rev_config:
        return rev_config[Gate(x_wire, gate_type, y_wire)]
    if Gate(y_wire, gate_type, x_wire) in rev_config:
        return rev_config[Gate(y_wire, gate_type, x_wire)]
    return None


def swap_output_wires(
    wire_a: str, wire_b: str, configurations: dict[str, Gate]
) -> dict[str, Gate]:
    new_configurations = {}

    for k, gate in configurations.items():
        if k == wire_a:
            new_configurations[wire_b] = gate

        elif k == wire_b:
            new_configurations[wire_a] = gate

        else:
            new_configurations[k] = gate

    return new_configurations


def check_parallel_adders(configurations: dict[str, Gate]) -> list[str]:
    current_carry_wire = None
    swaps = []
    bit = 0

    while True:
        x_wire = f"x{bit:02d}"
        y_wire = f"y{bit:02d}"
        z_wire = f"z{bit:02d}"

        if bit == 0:
            current_carry_wire = find_gate(x_wire, y_wire, "AND", configurations)
        else:
            ab_xor_gate = find_gate(x_wire, y_wire, "XOR", configurations)
            ab_and_gate = find_gate(x_wire, y_wire, "AND", configurations)

            cin_ab_xor_gate = find_gate(
                ab_xor_gate, current_carry_wire, "XOR", configurations
            )
            if cin_ab_xor_gate is None:
                swaps.append(ab_xor_gate)
                swaps.append(ab_and_gate)
                configurations = swap_output_wires(
                    ab_xor_gate, ab_and_gate, configurations
                )
                bit = 0
                continue

            if cin_ab_xor_gate != z_wire:
                swaps.append(cin_ab_xor_gate)
                swaps.append(z_wire)
                configurations = swap_output_wires(
                    cin_ab_xor_gate, z_wire, configurations
                )
                bit = 0
                continue

            cin_ab_and_gate = find_gate(
                ab_xor_gate, current_carry_wire, "AND", configurations
            )

            carry_wire = find_gate(ab_and_gate, cin_ab_and_gate, "OR", configurations)
            current_carry_wire = carry_wire

        bit += 1
        if bit >= 45:
            break

    return swaps


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
            gates[output] = Gate(operand1, operation, operand2)
            g.add_edge(operand1, output)
            g.add_edge(operand2, output)
    return g, wires, gates


def part1(data):
    """Part 1"""
    result = 0
    g, wires, gates = parse_data(data)
    values, _ = simulate(g, wires, gates)
    result = calculate_output(values)
    return result


def part2(data):
    """Part 2"""
    _, _, gates = parse_data(data)
    swaps = check_parallel_adders(gates)
    return ",".join(sorted(swaps))


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
