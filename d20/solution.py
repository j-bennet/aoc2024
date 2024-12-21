from os import path

import networkx as nx

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def parse_data(
    data: list[str],
) -> tuple[nx.Graph, tuple[int, int], tuple[int, int], set[tuple[int, int]]]:
    walls = set()
    start = (-1, -1)
    finish = (-1, -1)
    g = nx.Graph()
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "#":
                walls.add((j, i))
            elif c == "S":
                start = (j, i)
                g.add_node((j, i))
            elif c == "E":
                g.add_node((j, i))
                finish = (j, i)
            else:
                g.add_node((j, i))

    for n in g.nodes:
        x, y = n
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            next_x = x + dx
            next_y = y + dy
            if (next_x, next_y) in g.nodes:
                g.add_edge((x, y), (next_x, next_y))
    return g, start, finish, walls


def connecting_walls(g: nx.Graph, walls: set[tuple[int, int]]) -> list[tuple]:
    connecting_walls = []
    for w in walls:
        x, y = w
        connects = False
        if (x + 1, y) in g.nodes and (x - 1, y) in g.nodes:
            connects = True
        if (x, y + 1) in g.nodes and (x, y - 1) in g.nodes:
            connects = True
        if connects:
            connecting_walls.append((x, y))
    return connecting_walls


def part1(data, target_savings: int = 1, cheat_length: int = 2):
    """Part 1"""
    g, start, finish, walls = parse_data(data)
    best_path = nx.shortest_path(g, start, finish)
    best_path_length = len(best_path) - 1
    connecting = connecting_walls(g, walls)
    counter = 0

    distance_to_start = {}
    distance_to_finish = {}

    for i, node in enumerate(best_path):
        distance_to_start[node] = i
        distance_to_finish[node] = best_path_length - i - 1

    for i, (x, y) in enumerate(connecting):
        distances = []
        if (x + 1, y) in g.nodes and (x - 1, y) in g.nodes:
            distances.append(
                distance_to_start[(x + 1, y)]
                + distance_to_finish[(x - 1, y)]
                + cheat_length
            )
            distances.append(
                distance_to_start[(x - 1, y)]
                + distance_to_finish[(x + 1, y)]
                + cheat_length
            )
        if (x, y + 1) in g.nodes and (x, y - 1) in g.nodes:
            distances.append(
                distance_to_start[(x, y + 1)]
                + distance_to_finish[(x, y - 1)]
                + cheat_length
            )
            distances.append(
                distance_to_start[(x, y - 1)]
                + distance_to_finish[(x, y + 1)]
                + cheat_length
            )
        savings = best_path_length - min(*distances)
        if savings >= target_savings:
            # print(f"{i}/{len(connecting)} saves {savings} steps: {distances}")
            counter += 1
    return counter


def part2(data):
    """Part 2"""
    return 0


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'), 100)}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
