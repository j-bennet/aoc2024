from dataclasses import dataclass, field
from os import path

ROOT_DIR = path.dirname(__file__)


MOVES = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}


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
    robot: Robot
    boxes: set = field(default_factory=set)
    walls: set = field(default_factory=set)
    directions: str = ""

    def move_robot(self, direction: str):
        dx, dy = MOVES[direction]
        new_x = self.robot.x + dx
        new_y = self.robot.y + dy
        if (new_x, new_y) in self.walls:
            return False

        def explore_direction(x: int, y: int, boxes_to_move: set):
            if (x, y) in self.boxes:
                boxes_to_move.add((x, y))
                return explore_direction(x + dx, y + dy, boxes_to_move)
            elif 0 < x < (self.w - 1) and 0 < y < (self.h - 1):
                if (x, y) not in self.walls:
                    return (x, y)

        boxes_to_move = set()
        can_move = explore_direction(new_x, new_y, boxes_to_move)
        if not can_move:
            return False

        # move the boxes
        for box in boxes_to_move:
            self.boxes.remove(box)
        for box in boxes_to_move:
            self.boxes.add((box[0] + dx, box[1] + dy))

        # then the robot
        self.robot = Robot(new_x, new_y)
        return True

    def walk(self):
        for direction in self.directions:
            print(f"Move {direction}:")
            result = self.move_robot(direction)
            print(f"Moved: {result}")
            print(self)

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
    robot = Robot(0, 0)
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
    directions = data[-1]
    g = Grid(w, h, robot, boxes, walls, directions)
    return g


def part1(data):
    """Part 1"""
    g = parse_data(data)
    print("Initial:")
    print(g)
    g.walk()
    return 0


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('example.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
