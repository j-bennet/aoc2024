from collections import defaultdict
from functools import cache
from os import path

import networkx as nx
from networkx import DiGraph

"""
Credit to:
https://github.com/marcodelmastro/AdventOfCode2024/blob/main/Day21.ipynb
"""


def build_graph(data: list[str]) -> tuple[DiGraph, dict]:
    graph = DiGraph()
    pos_nodes = {}
    node_pos = {}
    moves_between_keys = {}
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == " ":
                continue
            graph.add_node(c, pos=(x, y))
            pos_nodes[(x, y)] = c
            node_pos[c] = (x, y)
    for unode in graph.nodes:
        x, y = node_pos[unode]
        if (x + 1, y) in pos_nodes:
            vnode = pos_nodes[(x + 1, y)]
            graph.add_edge(unode, vnode, dir=">")
            graph.add_edge(vnode, unode, dir="<")
            moves_between_keys[(unode, vnode)] = ">"
            moves_between_keys[(vnode, unode)] = "<"
        if (x, y + 1) in pos_nodes:
            vnode = pos_nodes[(x, y + 1)]
            graph.add_edge(unode, vnode, dir="v")
            graph.add_edge(vnode, unode, dir="^")
            moves_between_keys[(unode, vnode)] = "v"
            moves_between_keys[(vnode, unode)] = "^"
    return graph, moves_between_keys


def build_numeric_keypad() -> tuple[DiGraph, dict]:
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


def build_directional_keypad() -> tuple[DiGraph, dict]:
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


num_pad, num_pad_moves = build_numeric_keypad()
dir_pad, dir_pad_moves = build_directional_keypad()


def find_shortest_paths(g: DiGraph, moves: dict) -> dict:
    paths = defaultdict(list)
    for start in g.nodes():
        for end in g.nodes():
            if start != end:
                for p in list(nx.all_shortest_paths(g, start, end)):
                    m = "".join([moves[(p[i], p[i + 1])] for i in range(len(p) - 1)])
                    paths[start + end].append(m)
    return paths


# cache all possible shortest paths between two keys on a given keypath

paths_on_num_pad = find_shortest_paths(num_pad, num_pad_moves)
paths_on_dir_pad = find_shortest_paths(dir_pad, dir_pad_moves)


def num_paths(A, B):
    paths = []
    for p in nx.all_shortest_paths(num_pad, A, B):
        seq = []
        for i in range(len(p) - 1):
            move = (p[i], p[i + 1])
            seq += [num_pad_moves[move]]
        seq += ["A"]  # press A
        paths.append("".join(seq))
    return paths


def dir_paths(A, B):
    paths = []
    for p in nx.all_shortest_paths(dir_pad, A, B):
        seq = ""
        for i in range(len(p) - 1):
            move = (p[i], p[i + 1])
            seq += dir_pad_moves[move]
        seq += "A"  # press A
        paths.append(seq)
    return paths

def num_to_dir_options(target: str) -> list[str]:
    """
    What should be typed on the directional keypad
    to produce the output on the numeric keypad.
    """
    paths = []
    _target = "A" + target
    for i in range(len(_target) - 1):
        paths.append(num_paths(_target[i], _target[i + 1]))
    sequences = [""]
    i = 0
    while i < len(paths):
        sequences_new = []
        for s in sequences:
            for p in paths[i]:
                sequences_new.append(s + p)
        sequences = sequences_new
        i += 1
    return sequences


def dir_to_dir_options(target: str) -> list[str]:
    """
    What should be typed on the directional keypad
    to produce the output on another directional keypad.
    """
    paths = []
    _target = "A" + target
    for i in range(len(_target) - 1):
        paths.append(dir_paths(_target[i], _target[i + 1]))
    sequences = [""]
    i = 0
    while i < len(paths):
        sequences_new = []
        for s in sequences:
            for p in paths[i]:
                sequences_new.append(s + p)
        sequences = sequences_new
        i += 1
    return sequences


@cache
def minimum_sequence(level: int, target: str, nrobots: int) -> int:
    # end of keypad sequence reached, return lenght of current sequence
    if level == nrobots + 1:
        return len(target)

    # select dictionary of shortest paths according to level and corresponding keypad
    if level == 0:
        pair_paths = paths_on_num_pad
    else:
        pair_paths = paths_on_dir_pad

    # recursively cumulate sequence lenght, only considering shortest one
    total = 0
    for start, end in zip("A" + target, target):
        # adding "A" command at end of current step to press the button!
        min_seq = [
            minimum_sequence(level + 1, p + "A", nrobots)
            for p in pair_paths[start + end]
        ]
        if min_seq:
            total += min(min_seq)
        else:
            # When the same button is pressed twice in a row account for 1 step in sequence,
            # since  min_seq would be empty (no entry in the shortest path dictionaries), but
            # operation is happening anyway
            total += 1

    return total

def find_shortest_option_length(target: str) -> int:
    """Find the shortest option to type on the human keypad."""
    min_length = -1
    for robot1 in num_to_dir_options(target):
        for robot2 in dir_to_dir_options(robot1):
            for human in dir_to_dir_options(robot2):
                if min_length == -1 or len(human) < min_length:
                    min_length = len(human)
    return min_length


def part1(data):
    """Part 1"""
    result = 0
    for line in data:
        shortest_len = find_shortest_option_length(line)
        numeric_part = int(line[:-1])
        # print(
        #     f"{line}: {numeric_part} * {shortest_len} = {numeric_part * shortest_len}"
        # )
        result += numeric_part * shortest_len
    return result


def part2(data, nrobots=25):
    """Part 2"""
    result = 0
    for line in data:
        shortest_len = minimum_sequence(0, line, nrobots)
        numeric_part = int(line[:-1])
        print(
            f"{line}: {numeric_part} * {shortest_len} = {numeric_part * shortest_len}"
        )
        result += numeric_part * shortest_len
    return result


if __name__ == "__main__":
    # print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
