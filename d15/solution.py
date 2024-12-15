from dataclasses import dataclass, field
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


@dataclass
class Robot:
    x: int
    y: int


@dataclass
class Grid:
    w: int
    h: int
    robot: Robot | None = None
    boxes: set = field(default_factory=set)
    walls: set = field(default_factory=set)

    def __str__(self):
        result = ""
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in self.boxes:
                    result += "O"
                elif (x, y) in self.walls:
                    result += "#"
                elif self.robot and self.robot.x == x and self.robot.y == y:
                    result += "@"
                else:
                    result += "."
            result += "\n"
        return result


def parse_data(data) -> Grid:
    boxes = set()
    walls = set()
    robot = None
    for y, line in enumerate(data):
        if not line:
            break
        for x, char in enumerate(line):
            if char == "@":
                robot = Robot(x, y)
            elif char == "O":
                boxes.add((x, y))
            elif char == "#":
                walls.add((x, y))
    w = len(data[0])
    h = len(data) - 2
    return Grid(w, h, robot, boxes, walls)


def part1(data):
    """Part 1"""
    g = parse_data(data)
    print(g)
    return 0


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('example.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
