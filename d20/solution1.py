from collections import deque
from dataclasses import dataclass
from os import path

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
    queue.append((*racetrack.start, 0))
    costs = {}
    while queue:
        (x, y, steps) = queue.popleft()
        if (x, y) in costs and costs[(x, y)] <= steps:
            continue
        if (x, y) in racetrack.walls:
            continue
        if x < 0 or y < 0 or x >= racetrack.w or y >= racetrack.h:
            continue
        costs[(x, y)] = steps
        if (x, y) == racetrack.finish:
            return steps
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            next_x = x + dx
            next_y = y + dy
            queue.append((next_x, next_y, steps + 1))
    return -1


def find_all_paths(racetrack: Racetrack, max_steps: int | None = None) -> set[tuple]:
    queue = deque()
    queue.append(((*racetrack.start, 0), [racetrack.start]))
    all_paths = set()
    while queue:
        (x, y, steps), acc = queue.popleft()
        if max_steps is not None and steps >= max_steps:
            continue
        if (x, y) in racetrack.walls:
            continue
        if x < 0 or y < 0 or x >= racetrack.w or y >= racetrack.h:
            continue
        if (x, y) == racetrack.finish:
            all_paths.add(tuple(acc))
            continue
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            next_x = x + dx
            next_y = y + dy
            if (next_x, next_y) not in acc:
                queue.append(((next_x, next_y, steps + 1), acc + [(next_x, next_y)]))
    return all_paths


def part1(data, target_savings: int = 1):
    """Part 1"""
    racetrack = parse_data(data)
    best_path = shortest_path(racetrack)

    all_paths = set()
    for wall in racetrack.walls:
        walls = racetrack.walls - {wall}
        cheat = Racetrack(
            racetrack.w, racetrack.h, walls, racetrack.start, racetrack.finish
        )
        cheat_paths = find_all_paths(cheat, best_path)
        all_paths |= cheat_paths

    print(len(all_paths))
    result = 0
    for path in all_paths:
        savings = best_path - len(path) - 1
        if savings >= target_savings:
            result += 1
    return best_path


def part2(data):
    """Part 2"""
    return 0


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'), 100)}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
