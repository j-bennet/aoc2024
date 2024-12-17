import copy
from dataclasses import dataclass
from os import path
from typing import Counter, DefaultDict

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
    target: tuple[int, int]

    def __str__(self):
        maze = copy.deepcopy(self.maze)
        reindeer_line = list(maze[self.reindeer[1]])
        reindeer_line[self.reindeer[0]] = self.reindeer[2]
        maze[self.reindeer[1]] = "".join(reindeer_line)
        return "\n".join(maze)

    def bfs(self):
        """
        Finds all shortest paths to the exit using a breadth-first search.

        Keeps track of all paths and their costs
        """
        queue = [(*self.reindeer, 0, set())]
        costs = {}
        while queue:
            x, y, facing, cost, acc = queue.pop(0)
            if x < 0 or x >= self.w or y < 0 or y >= self.h:
                continue
            if self.maze[y][x] == "#":
                continue
            if (x, y, facing) in costs and costs[(x, y, facing)][0] < cost:
                continue
            if (x, y, facing) not in costs or costs[(x, y, facing)][0] > cost:
                costs[(x, y, facing)] = (cost, acc | {(x, y)})
            else:
                costs[(x, y, facing)][1].update(acc | {(x, y)})
            queue.append(
                (
                    x + moves[facing][0],
                    y + moves[facing][1],
                    facing,
                    cost + 1,
                    acc | {(x, y)},
                )
            )
            for new_facing in [clockwise[facing], counterclock[facing]]:
                queue.append(
                    (
                        x + moves[new_facing][0],
                        y + moves[new_facing][1],
                        new_facing,
                        cost + 1001,
                        acc | {(x, y)},
                    )
                )
        target_costs = []
        cost_paths = DefaultDict(set)
        cost_counter = Counter()
        for direction in ["^", "v", ">", "<"]:
            if (*self.target, direction) in costs:
                cost, acc = costs[(*self.target, direction)]
                target_costs.append(cost)
                cost_paths[cost] |= acc
                cost_counter[cost] += 1
        min_cost = min(target_costs)
        best_spots = len(cost_paths[min_cost])
        return min_cost, best_spots


def parse_data(data):
    maze = []
    reindeer = (None, None, None)
    target = (None, None)
    for y, d in enumerate(data):
        line = ""
        for x, char in enumerate(d):
            if char == "S":
                reindeer = (x, y, ">")
                line += "."
            elif char == "E":
                target = (x, y)
                line += char
            else:
                line += char
        maze.append(line)
    return Maze(len(maze[0]), len(maze), maze, reindeer, target)


def part1(data):
    """Part 1"""
    m = parse_data(data)
    cost, _ = m.bfs()
    return cost


def part2(data):
    """Part 2"""
    m = parse_data(data)
    _, seats = m.bfs()
    return seats


if __name__ == "__main__":
    # print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
