from os import path

import networkx as nx
from networkx import Graph

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def parse_data(data) -> Graph:
    G = nx.Graph()
    for line in data:
        comp1, comp2 = line.split("-")
        G.add_edge(comp1, comp2)
    return G


def find_triangles(graph: Graph):
    triangles = []
    for node in graph:
        neighbors = set(graph[node])
        for neighbor in neighbors:
            common_neighbors = neighbors.intersection(graph[neighbor])
            for common_neighbor in common_neighbors:
                if node < neighbor < common_neighbor:  # to avoid duplicates
                    if any(
                        x.startswith("t") for x in [node, neighbor, common_neighbor]
                    ):
                        triangles.append((node, neighbor, common_neighbor))
    return triangles


def part1(data):
    """Part 1"""
    g = parse_data(data)
    triangles = find_triangles(g)
    return len(triangles)


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    # print(f"Part 2: {part2(get_data('example.txt'))}")
