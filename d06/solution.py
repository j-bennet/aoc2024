from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


class Grid:
    moves = {
        "^": (0, -1),
        "v": (0, 1),
        "<": (-1, 0),
        ">": (1, 0),
    }

    turn_right = {
        "^": ">",
        "v": "<",
        "<": "^",
        ">": "v",
    }

    def __init__(self, data: list[str]) -> None:
        self.g = []
        self.w = len(data[0])
        self.h = len(data)
        self.direction = ""
        self.initial = (0, 0)
        for r, row in enumerate(data):
            cells = []
            for c, x in enumerate(row):
                if x in ("#", "."):
                    cells.append(x)
                elif x in self.moves:
                    self.direction = x
                    self.initial = c, r
                    cells.append(".")
                else:
                    raise ValueError(f"Unknown character {x} at {row}")
            self.g.append(cells)

    def is_obstruction(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h and self.g[y][x] == "#"

    def walk(self, x, y):
        visited = set()
        while 0 <= x < self.w and 0 <= y < self.h:
            visited.add((x, y))
            dx, dy = self.moves[self.direction]
            if self.is_obstruction(x + dx, y + dy):
                self.direction = self.turn_right[self.direction]
                continue
            else:
                x += dx
                y += dy
        return visited


def part1(data):
    """Part 1"""
    grid = Grid(data)
    visited = grid.walk(*grid.initial)
    return len(visited)


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
