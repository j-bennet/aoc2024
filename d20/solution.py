from collections import deque
from dataclasses import dataclass
from os import path
from typing import NamedTuple

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


@dataclass
class Racetrack:
    w: int
    h: int
    walls: set[tuple[int, int]]
    start: tuple[int, int]
    finish: tuple[int, int]

    def __str__(self) -> str:
        result = ""
        for i in range(self.h):
            for j in range(self.w):
                if (j, i) in self.walls:
                    result += "#"
                elif (j, i) == self.start:
                    result += "S"
                elif (j, i) == self.finish:
                    result += "E"
                else:
                    result += "."
            result += "\n"
        return result


class Program(NamedTuple):
    x: int = 0
    y: int = 0
    steps: int = 0
    cheat_count: int = 0
    cheat_move: int = 0


def parse_data(data: list[str]) -> Racetrack:
    walls = set()
    w = len(data[0])
    h = len(data)
    start = None
    finish = None
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "#":
                walls.add((j, i))
            elif c == "S":
                start = (j, i)
            elif c == "E":
                finish = (j, i)
    return Racetrack(w, h, walls, start, finish)


def shortest_path(racetrack: Racetrack) -> int:
    queue = deque()
    queue.append(Program(*racetrack.start))
    costs = {}
    while queue:
        prog = queue.popleft()
        if (prog.x, prog.y) in costs and costs[(prog.x, prog.y)] <= prog.steps:
            continue
        if (prog.x, prog.y) in racetrack.walls:
            continue
        if prog.x < 0 or prog.y < 0 or prog.x >= racetrack.w or prog.y >= racetrack.h:
            continue
        costs[(prog.x, prog.y)] = prog.steps
        if (prog.x, prog.y) == racetrack.finish:
            return prog.steps
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            x = prog.x + dx
            y = prog.y + dy
            queue.append(Program(x, y, prog.steps + 1))
    return -1


def part1(data):
    """Part 1"""
    racetrack = parse_data(data)
    print(racetrack)
    result = shortest_path(racetrack)
    return result


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('example.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
