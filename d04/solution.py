import re
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


class Grid:
    PAT = re.compile(r"^(MAS|SAM)$")

    def __init__(self, data):
        self.g = data
        self.w = len(data[0])
        self.h = len(data)

    def has_pattern(self, pattern, limit, x, y, dx, dy):
        target = ""
        while 0 <= x < self.w and 0 <= y < self.h:
            target += self.g[y][x]
            if len(target) > limit:
                return False
            if len(target) == limit:
                return re.match(pattern, target)
            x += dx
            y += dy
        return False

    def count_mas(self, x, y):
        if self.has_pattern(self.PAT, 3, x, y, 1, 1) and self.has_pattern(
            self.PAT, 3, x, y + 2, 1, -1
        ):
            return 1
        return 0

    def has_xmas(self, x, y, dx, dy):
        target = ""
        while 0 <= x < self.w and 0 <= y < self.h:
            target += self.g[y][x]
            if len(target) > 4:
                return False
            if target == "XMAS":
                return True
            x += dx
            y += dy
        return False

    def count_xmas(self, x, y):
        cnt = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                cnt += self.has_xmas(x, y, dx, dy)
        return cnt

    def count_all_mas(self):
        cnt = 0
        for y in range(self.h):
            for x in range(self.w):
                res = self.count_mas(x, y)
                cnt += res
        return cnt

    def count_all_xmas(self):
        cnt = 0
        for y in range(self.h):
            for x in range(self.w):
                cnt += self.count_xmas(x, y)
        return cnt


def part1(data):
    """Part 1"""
    grid = Grid(data)
    result = grid.count_all_xmas()
    return result


def part2(data):
    """Part 2"""
    grid = Grid(data)
    result = grid.count_all_mas()
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
