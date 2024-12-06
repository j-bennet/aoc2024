import copy
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
        return 0 <= x < self.w and 0 <= y < self.h and self.g[y][x] in ("#", "0")

    def walk(self, x, y):
        visited = set()
        direction = self.direction
        while 0 <= x < self.w and 0 <= y < self.h:
            visited.add((x, y))
            dx, dy = self.moves[direction]
            if self.is_obstruction(x + dx, y + dy):
                direction = self.turn_right[direction]
                continue
            else:
                x += dx
                y += dy
        return visited

    def in_a_loop(self, corners):
        if len(corners) < 5:
            return False
        # print(corners[-1], corners[-5], corners[-1] == corners[-5])
        # print(corners)
        for j in range(len(corners) - 5, -1, -4):
            if corners[-1] == corners[j]:
                return True
        return False

    def will_loop(self, x, y):
        corners = []
        direction = self.direction
        while 0 <= x < self.w and 0 <= y < self.h:
            dx, dy = self.moves[direction]
            if self.in_a_loop(corners):
                return True
            if self.is_obstruction(x + dx, y + dy):
                corners.append((x, y))
                # corners = corners[-100:]
                direction = self.turn_right[direction]
                continue
            else:
                x += dx
                y += dy
        return False

    def __str__(self):
        data = copy.deepcopy(self.g)
        data[self.initial[1]][self.initial[0]] = self.direction
        return "\n".join("".join(row) for row in data)


def part1(data):
    """Part 1"""
    grid = Grid(data)
    visited = grid.walk(*grid.initial)
    return len(visited)


def part2(data):
    """Part 2"""
    grid = Grid(data)
    loops = set()
    for r in range(grid.h):
        for c in range(grid.w):
            # if r != 8:
            #     continue
            # try adding an obstacle
            if grid.g[r][c] == ".":
                grid.g[r][c] = "0"
                if grid.will_loop(*grid.initial):
                    # print(f"Loop at {r=}, {c=}")
                    # print(grid)
                    # print("----")
                    loops.add((c, r))
                # else:
                #     print(f"No loop at {r=}, {c=}")
                #     print(grid)
                #     print("----")
                # revert the change
                grid.g[r][c] = "."
    return len(loops)


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
