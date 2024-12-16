import copy
from dataclasses import dataclass
from os import path

ROOT_DIR = path.dirname(__file__)


clockwise = {">": "v", "v": "<", "<": "^", "^": ">"}

counterclock = {">": "^", "v": ">", "<": "v", "^": "<"}

moves = {"^": (0, -1), "v": (0, 1), ">": (1, 0), "<": (-1, 0)}


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


@dataclass
class Maze:
    w: int
    h: int
    maze: list[str]
    reindeer: tuple[int, int, str]

    def __str__(self):
        maze = copy.deepcopy(self.maze)
        reindeer_line = list(maze[self.reindeer[1]])
        reindeer_line[self.reindeer[0]] = self.reindeer[2]
        maze[self.reindeer[1]] = "".join(reindeer_line)
        return "\n".join(maze)

    def cheapest_from(self, x, y, facing, cost, visited):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return float("inf")
        if self.maze[y][x] == "#":
            return float("inf")
        if self.maze[y][x] == "E":
            return cost
        if (x, y, facing) in visited and visited[(x, y, facing)] <= cost:
            return float("inf")
        visited[(x, y, facing)] = cost
        return min(
            self.cheapest_from(
                x + moves[facing][0],
                y + moves[facing][1],
                facing,
                cost + 1,
                visited,
            ),
            self.cheapest_from(
                x + moves[clockwise[facing]][0],
                y + moves[clockwise[facing]][1],
                clockwise[facing],
                cost + 1001,
                visited,
            ),
            self.cheapest_from(
                x + moves[counterclock[facing]][0],
                y + moves[counterclock[facing]][1],
                counterclock[facing],
                cost + 1001,
                visited,
            ),
        )

    def cheapest_path(self):
        visited = {}
        return self.cheapest_from(*self.reindeer, 0, visited)


def parse_data(data):
    maze = []
    reindeer = (None, None, None)
    for y, d in enumerate(data):
        line = ""
        for x, char in enumerate(d):
            if char == "S":
                reindeer = (x, y, ">")
                line += "."
            else:
                line += char
        maze.append(line)
    return Maze(len(maze[0]), len(maze), maze, reindeer)


def part1(data):
    """Part 1"""
    m = parse_data(data)
    print(m)
    cost, steps, turns = m.cheapest_path()
    print(f"Cost: {cost}, Steps: {steps}, Turns: {turns}")
    return cost


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
