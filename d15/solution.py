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
class Box:
    def __init__(self, x, y, w=1):
        self.x = x
        self.y = y
        self.w = w

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.w))


@dataclass
class Grid:
    w: int
    h: int
    robot: Robot
    boxes: set = field(default_factory=set)
    walls: set = field(default_factory=set)
    directions: str = ""

    def sum_gps(self):
        result = 0
        for x, y in self.boxes:
            result += x + 100 * y
        return result

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
            # print(f"Move {direction}:")
            result = self.move_robot(direction)
            # print(f"Moved: {result}")
            # print(self)

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


@dataclass
class Grid2:
    w: int
    h: int
    robot: Robot
    boxes_l: set = field(default_factory=set)
    boxes_r: set = field(default_factory=set)
    walls: set = field(default_factory=set)
    directions: str = ""

    def sum_gps(self):
        result = 0
        for x, y in self.boxes_l:
            result += x + 100 * y
        return result

    def move_robot(self, direction: str):
        dx, dy = MOVES[direction]
        new_x = self.robot.x + dx
        new_y = self.robot.y + dy
        if (new_x, new_y) in self.walls:
            return False

        def explore_direction(x: int, y: int, boxes_l: set, boxes_r: set):
            if (x, y) in self.boxes_l:
                boxes_l.add((x, y))
                boxes_r.add((x + 1, y))
                return explore_direction(
                    x + 1, y, boxes_l, boxes_r
                ) and explore_direction(x + dx, y + dy, boxes_l, boxes_r)
            elif (x, y) in self.boxes_r:
                boxes_r.add((x, y))
                boxes_l.add((x - 1, y))
                return explore_direction(
                    x - 1, y, boxes_l, boxes_r
                ) and explore_direction(x + dx, y + dy, boxes_l, boxes_r)
            elif 1 < x < (self.w - 2) and 0 < y < (self.h - 1):
                if (x, y) not in self.walls:
                    return True

        boxes_l = set()
        boxes_r = set()
        can_move = explore_direction(new_x, new_y, boxes_l, boxes_r)
        if not can_move:
            return False

        # move the boxes, left halves
        for box in boxes_l:
            self.boxes_l.remove(box)
        for box in boxes_l:
            self.boxes_l.add((box[0] + dx, box[1] + dy))

        # right halves
        for box in boxes_r:
            self.boxes_r.remove(box)
        for box in boxes_r:
            self.boxes_r.add((box[0] + dx, box[1] + dy))

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
                if (x, y) in self.boxes_l:
                    result += "["
                elif (x, y) in self.boxes_r:
                    result += "]"
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
    h = 0
    for y, line in enumerate(data):
        if not line:
            break
        h += 1
        for x, char in enumerate(line):
            if char == "@":
                robot = Robot(x, y)
            elif char == "O":
                boxes.add((x, y))
            elif char == "#":
                walls.add((x, y))
    w = len(data[0])
    directions = "".join(data[h + 1 :])
    g = Grid(w, h, robot, boxes, walls, directions)
    return g


def parse_data2(data) -> Grid2:
    boxes_l = set()
    boxes_r = set()
    walls = set()
    robot = Robot(0, 0)
    h = 0
    for y, line in enumerate(data):
        if not line:
            break
        h += 1
        for x, char in enumerate(line):
            if char == "@":
                robot = Robot(x * 2, y)
            elif char == "O":
                boxes_l.add((x * 2, y))
                boxes_r.add((x * 2 + 1, y))
            elif char == "#":
                walls.add((x * 2, y))
                walls.add((x * 2 + 1, y))
    w = len(data[0])
    directions = "".join(data[h + 1 :])
    g = Grid2(w * 2, h, robot, boxes_l, boxes_r, walls, directions)
    return g


def part1(data):
    """Part 1"""
    g = parse_data(data)
    # print("Initial:")
    # print(g)
    g.walk()
    return g.sum_gps()


def part2(data):
    """Part 2"""
    g = parse_data2(data)
    print("Initial:")
    print(g)
    g.walk()
    return g.sum_gps()


if __name__ == "__main__":
    # print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example3.txt'))}")
