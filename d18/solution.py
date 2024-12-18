from collections import deque
from dataclasses import dataclass
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


@dataclass
class Grid:
    w: int
    h: int
    bytes: list[tuple[int, int]]

    def bfs(self, initial: tuple[int, int], target: tuple[int, int]):
        """
        Find the shortest path to the exit using a breadth-first search.
        """
        queue = deque()
        queue.append((*initial, 0))
        costs = {}
        while queue:
            x, y, cost = queue.popleft()
            if x < 0 or x >= self.w or y < 0 or y >= self.h:
                continue
            if (x, y) in self.bytes:
                continue
            if (x, y) in costs and costs[(x, y)] <= cost:
                continue
            costs[(x, y)] = cost
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                queue.append((x + dx, y + dy, cost + 1))
        return costs.get(target)

    def __str__(self) -> str:
        result = ""
        for y in range(self.h):
            for x in range(self.w):
                result += "#" if (x, y) in self.bytes else "."
            result += "\n"
        return result


def parse_data(data):
    bytes = []
    for line in data:
        x, y = line.split(",")
        bytes.append((int(x), int(y)))
    return bytes


def part1(data):
    """Part 1"""
    # bytes = parse_data(data)
    # grid = Grid(7, 7, bytes[:12])
    # print(grid)
    # return grid.bfs((0, 0), (6, 6))
    bytes = parse_data(data)
    grid = Grid(71, 71, bytes[:1024])
    print(grid)
    return grid.bfs((0, 0), (70, 70))


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
