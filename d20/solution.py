from collections import defaultdict
from enum import Enum
from functools import cache, cached_property
from math import inf
from os import path

ROOT_DIR = path.dirname(__file__)
"""
credit to Alexandra Jay:
https://www.reddit.com/r/adventofcode/comments/1hicdtb/comment/m31nmc9/
I was able to solve part 1, but had to use reddit for part 2.
"""

def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


class Direction(Enum):
    """A cardinal direction."""

    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    @property
    def horisontal(self):
        return self in (Direction.LEFT, Direction.RIGHT)

    @cached_property
    def delta(self):
        return ((0, -1), (1, 0), (0, 1), (-1, 0))[self.value]

    def move(self, x, y):
        """Translate the coordinates a distance of 1 in this direction."""
        dx, dy = self.delta
        return x + dx, y + dy


@cache
def taxicab_circle(x, y, r):
    for offset in range(r):
        inv_offset = r - offset
        yield x + offset, y + inv_offset
        yield x + inv_offset, y - offset
        yield x - offset, y - inv_offset
        yield x - inv_offset, y + offset


def find_tile(grid, tile):
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == tile:
                return x, y

    raise ValueError(f'Could not find "{tile}" in grid')


def ScoreMap(mapping):
    return defaultdict(lambda: inf, mapping)


def on_grid(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def at(grid, x, y):
    return grid[y][x]


def open_space(grid):
    def check(coord):
        return on_grid(*coord, grid) and at(grid, *coord) != "#"

    return check


def get_cheats(x, y, grid, cheat_time):
    for radius in range(2, cheat_time + 1):
        valid_cheats = filter(open_space(grid), taxicab_circle(x, y, radius))
        yield from ((cheat, radius) for cheat in valid_cheats)


def make_graph(grid, cheat_time):
    valid_neighbour = open_space(grid)

    start = find_tile(grid, "S")
    end = find_tile(grid, "E")

    seen = {
        start,
    }
    edges = defaultdict(set)
    cheats = dict()  # a cheat is effectively a bonus edge

    todo = {
        start,
    }
    while len(todo) > 0:
        node = todo.pop()

        # find this node's neighbours
        for direction in Direction:
            neighbour = direction.move(*node)
            if valid_neighbour(neighbour):
                # valid neighbour
                edges[node].add(neighbour)

                if neighbour not in seen:
                    todo.add(neighbour)
                    seen.add(neighbour)

        # find the cheats for this node
        cheats[node] = set(get_cheats(*node, grid, cheat_time))

    return start, end, edges, cheats


def dijkstra(start, edges):
    discovered = {
        start,
    }
    distance = ScoreMap({start: 0})

    while len(discovered) > 0:
        current_node = min(discovered, key=lambda x: distance[x])
        discovered.remove(current_node)

        for neighbour in edges[current_node]:
            candidate_score = distance[current_node] + 1
            if candidate_score < distance[neighbour]:
                distance[neighbour] = candidate_score
                discovered.add(neighbour)

    return distance


def multi_items(mapping):
    for key, items in mapping.items():
        for item in items:
            yield key, *item


def part1(data, target_savings: int = 1, cheat_length: int = 2):
    """Part 1"""
    start, end, edges, cheats = make_graph(data, cheat_length)
    distance_from_start = dijkstra(start, edges)
    distance_from_end = dijkstra(end, edges)
    target_distance = distance_from_start[end] - target_savings

    cheat_count = defaultdict(int)
    total = 0
    for cheat_start, cheat_end, _ in multi_items(cheats):
        dist = (
            distance_from_start[cheat_start]
            + cheat_length
            + distance_from_end[cheat_end]
        )
        if dist <= target_distance:
            cheat_count[distance_from_start[end] - dist] += 1
            total += 1

    # for save, number in sorted(cheat_count.items(), key=lambda x: x[0]):
    #     if number == 1:
    #         print(f"There is one cheat that saves {save} picoseconds")
    #     else:
    #         print(f"There are {number} cheats that save {save} picoseconds")

    return total

def part2(data, target_savings: int = 100, cheat_length: int = 20):
    """Part 2"""
    start, end, edges, cheats = make_graph(data, cheat_length)
    distance_from_start = dijkstra(start, edges)
    distance_from_end = dijkstra(end, edges)
    target_distance = distance_from_start[end] - target_savings

    cheat_count = defaultdict(int)
    total = 0
    for cheat_start, cheat_end, cheat_cost in multi_items(cheats):
        dist = (
            distance_from_start[cheat_start] + cheat_cost + distance_from_end[cheat_end]
        )
        if dist <= target_distance:
            cheat_count[distance_from_start[end] - dist] += 1
            total += 1

    # for save, number in sorted(cheat_count.items(), key=lambda x: x[0]):
    #     if number == 1:
    #         print(f"There is one cheat that saves {save} picoseconds")
    #     else:
    #         print(f"There are {number} cheats that save {save} picoseconds")

    return total

if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'), 100)}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
