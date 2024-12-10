from os import path
from typing import DefaultDict

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


class Map:
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, data):
        self.data = data
        self.w = len(data[0])
        self.h = len(data)
        self.heights = {}
        self.trails = DefaultDict(set)
        self.parse_heights()
        self.find_trails()

    def parse_heights(self):
        for y, line in enumerate(self.data):
            for x, num in enumerate(line):
                self.heights[(x, y)] = int(num)

    def walk_up(self, acc):
        x, y, h = acc[-1]
        if h == 9:
            self.trails[acc[0]].add(acc[-1])
            return

        # if (x, y) in self.walked:
        #     return
        # self.walked.add((x, y))

        for dx, dy in self.moves:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.w
                and 0 <= ny < self.h
                and self.heights[(nx, ny)] == h + 1
            ):
                self.walk_up(acc + [(nx, ny, h + 1)])

    def find_trails(self):
        # self.walked = set()
        for y in range(self.h):
            for x in range(self.w):
                if self.heights[(x, y)] == 0:
                    self.walk_up([(x, y, 0)])

    @property
    def score(self):
        return sum(len(v) for v in self.trails.values())


def part1(data):
    """Part 1"""
    m = Map(data)
    result = m.score
    return result


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
