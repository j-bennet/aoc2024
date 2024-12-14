from dataclasses import dataclass
from os import path
from typing import Counter

ROOT_DIR = path.dirname(__file__)


@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int

    def __init__(self, data):
        """p=0,4 v=3,-3"""
        self._data = data
        pos, vel = data.split()
        self.x, self.y = list(map(int, pos.split("=")[1].split(",")))
        self.dx, self.dy = list(map(int, vel.split("=")[1].split(",")))

    def move(self, n: int, w: int, h: int):
        self.x += n * self.dx
        self.y += n * self.dy
        self.x = self.x % w
        self.y = self.y % h
        if self.x < 0:
            self.x += w
        if self.y < 0:
            self.y += h


@dataclass
class Grid:
    w: int
    h: int
    robots: list[Robot]

    def __init__(self, w, h, robots):
        self.w = w
        self.h = h
        self.mw = w // 2
        self.mh = h // 2
        self.robots = robots
        self.robot_counts = Counter([(r.x, r.y) for r in robots])
        self.quadrants = self.make_quadrants()

    def make_quadrants(self):
        q1 = []
        q2 = []
        q3 = []
        q4 = []
        for r in self.robots:
            if r.x < self.mw and r.y < self.mh:
                q1.append((r.x, r.y))
            elif r.x > self.mw and r.y < self.mh:
                q2.append((r.x, r.y))
            elif r.x < self.mw and r.y > self.mh:
                q3.append((r.x, r.y))
            elif r.x > self.mw and r.y > self.mh:
                q4.append((r.x, r.y))
        return Counter(q1), Counter(q2), Counter(q3), Counter(q4)

    def christmas_tree(self):
        """q1 q2
        q3 q4"""
        q1_count = sum(self.quadrants[0].values())
        q2_count = sum(self.quadrants[1].values())
        q3_count = sum(self.quadrants[2].values())
        q4_count = sum(self.quadrants[3].values())
        return (
            (q3_count > q1_count)
            and (q3_count > q2_count)
            and (q4_count > q1_count)
            and (q4_count > q2_count)
            and (q4_count > q1_count)
        )

    def safety_factor(self):
        total = 1
        for q in self.quadrants:
            total *= sum(q.values())
        return total

    def __str__(self):
        lines = []
        for y in range(self.h):
            line = ""
            for x in range(self.w):
                if (x, y) in self.robot_counts:
                    # line += f"{self.robot_counts[(x, y)]}"
                    line += "#"
                else:
                    line += "."
            lines.append(line)
        robot_str = "\n".join(lines)
        return robot_str


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def part1(data):
    """Part 1"""
    robots = [Robot(d) for d in data]
    w = 101
    h = 103
    for r in robots:
        r.move(100, w=w, h=h)
    grid = Grid(w, h, robots)
    return grid.safety_factor()


def part2(data):
    """Part 2"""
    robots = [Robot(d) for d in data]
    w = 101
    h = 103
    for i in range(100):
        for r in robots:
            r.move(i, w=w, h=h)
        grid = Grid(w, h, robots)
        if grid.christmas_tree():
            print(f"Time: {i+1}")
            print(grid)
            print("---")


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
