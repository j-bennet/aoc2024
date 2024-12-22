from os import path

import networkx as nx
from networkx import DiGraph


def build_graph(data: list[str]) -> DiGraph:
    graph = DiGraph()
    pos_nodes = {}
    node_pos = {}
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == " ":
                continue
            graph.add_node(c, pos=(x, y))
            pos_nodes[(x, y)] = c
            node_pos[c] = (x, y)
    for node in graph.nodes:
        x, y = node_pos[node]
        if (x + 1, y) in pos_nodes:
            graph.add_edge(node, pos_nodes[(x + 1, y)], dir=">")
            graph.add_edge(pos_nodes[(x + 1, y)], node, dir="<")
        if (x, y + 1) in pos_nodes:
            graph.add_edge(node, pos_nodes[(x, y + 1)], dir="v")
            graph.add_edge(pos_nodes[(x, y + 1)], node, dir="^")
    return graph


def build_numeric_keypad() -> DiGraph:
    """
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+
    """
    data = ["789", "456", "123", " 0A"]
    return build_graph(data)


def build_directional_keypad() -> DiGraph:
    """
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """
    data = [" ^A", "<v>"]
    return build_graph(data)


ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


num_pad = build_numeric_keypad()
num_pad_paths = dict(nx.all_pairs_all_shortest_paths(num_pad))

dir_pad = build_directional_keypad()
dir_pad_paths = dict(nx.all_pairs_all_shortest_paths(dir_pad))


def edges_for_numeric_path(path: list) -> str:
    result = ""
    for u, v in zip(path, path[1:]):
        edge = num_pad.edges[u, v]
        result += edge["dir"]
    return result


def edges_for_directional_path(path: list) -> str:
    result = ""
    for u, v in zip(path, path[1:]):
        edge = dir_pad.edges[u, v]
        result += edge["dir"]
    return result


def steps_for_target(start_sym: str, target: str):
    target_symbols = list(target)
    steps = [(start_sym, target_symbols[0])]
    if len(target_symbols) >= 1:
        steps.extend([(u, v) for u, v in zip(target_symbols, target_symbols[1:])])
    return steps


def numeric_to_directional_options(start_sym: str, target: str) -> list[str]:
    """
    What should be typed on the directional keypad
    to produce the output on the numeric keypad.
    """
    results = []
    steps = steps_for_target(start_sym, target)
    for sym1, sym2 in steps:
        step_results = []
        for possible_path in num_pad_paths[sym1][sym2]:
            res = edges_for_numeric_path(possible_path)
            step_results.append(res + "A")
        if len(results) == 0:
            results = step_results
        else:
            results = [r1 + r2 for r1 in results for r2 in step_results]
    return results


def directional_to_directional_options(start_sym: str, target: str) -> list[str]:
    """
    What should be typed on the directional keypad
    to produce the output on another directional keypad.
    """
    results = []
    steps = steps_for_target(start_sym, target)
    for sym1, sym2 in steps:
        step_results = []
        for possible_path in dir_pad_paths[sym1][sym2]:
            res = edges_for_directional_path(possible_path)
            step_results.append(res + "A")
        if len(results) == 0:
            results = step_results
        else:
            results = [r1 + r2 for r1 in results for r2 in step_results]
    return results


def find_shortest_option_length(start_sym: str, target: str) -> int:
    """Find the shortest option to type on the human keypad."""
    min_length = -1
    for robot1 in numeric_to_directional_options(start_sym, target):
        for robot2 in directional_to_directional_options(start_sym, robot1):
            for human in directional_to_directional_options(start_sym, robot2):
                if min_length == -1 or len(human) < min_length:
                    min_length = len(human)
    return min_length


def part1(data):
    """Part 1"""
    result = 0
    for line in data:
        shortest_len = find_shortest_option_length("A", line)
        numeric_part = int(line[:-1])
        print(
            f"{line}: {numeric_part} * {shortest_len} = {numeric_part * shortest_len}"
        )
        result += numeric_part * shortest_len
    return result


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
