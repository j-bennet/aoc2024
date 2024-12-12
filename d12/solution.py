from os import path
from typing import DefaultDict

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Grid:
    def __init__(self, data) -> None:
        self.data = data
        self.h = len(data)
        self.w = len(data[0])
        self.region_map = self.map_regions()
        self.region_dict = DefaultDict(set)
        for k, v in self.region_map.items():
            self.region_dict[v].add(k)

    def region_area(self, region_id):
        return len(self.region_dict[region_id])

    def region_perimeter(self, region_id):
        result = 0
        for i, j in self.region_dict[region_id]:
            for dx, dy in moves:
                ni, nj = i + dx, j + dy
                if (ni, nj) not in self.region_dict[region_id]:
                    result += 1
        return result

    @property
    def total_price(self):
        result = 0
        for region_id in sorted(self.region_dict.keys()):
            region_price = self.region_area(region_id) * self.region_perimeter(
                region_id
            )
            # print(f"Region {region_id}: {region_price}")
            result += region_price
        # print(f"Total price: {result}")
        return result

    def __str__(self) -> str:
        result = []
        for i in range(self.h):
            line = "".join(f"{self.region_map[(i, j)]: 2}" for j in range(self.w))
            result.append(line)
        return "\n".join(result)

    def map_regions(self):
        seen = {}

        def map_region(i, j, seen, region_id, letter):
            for dx, dy in moves:
                ni, nj = i + dx, j + dy
                if (
                    0 <= ni < self.h
                    and 0 <= nj < self.w
                    and (ni, nj) not in seen
                    and self.data[ni][nj] == letter
                ):
                    seen[(ni, nj)] = region_id
                    map_region(ni, nj, seen, region_id, letter)

        region_id = 0
        for i in range(self.h):
            for j in range(self.w):
                if (i, j) not in seen:
                    region_id += 1
                    map_region(i, j, seen, region_id, self.data[i][j])
                    seen[(i, j)] = region_id
        return seen


def part1(data):
    """Part 1"""
    g = Grid(data)
    result = g.total_price
    return result


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
