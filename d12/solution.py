from os import path
from typing import DefaultDict

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
diags = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


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
            for di, dj in moves:
                ni, nj = i + di, j + dj
                if (ni, nj) not in self.region_dict[region_id]:
                    result += 1
        return result

    def region_corners(self, region_id):
        # Calculates the number of corners for a given square within the shape.
        # A corner is identified based on the diagonals and neighboring squares:
        # - If the diagonal is not part of the shape, and both neighboring squares
        #   (one from the row and one from the column) are either inside or outside
        #   the shape, it is considered a corner.
        shape = self.region_dict[region_id]

        def cell_corners(r, c):
            corners = 0

            for dr, dc in diags:
                diagonal_row = r + dr
                diagonal_col = c + dc

                # To get the neightbouring squares of the current square and its diagonals
                # we swap the rows and the columns
                neighbour_one = (r, diagonal_col)
                neighbour_two = (diagonal_row, c)

                if (diagonal_row, diagonal_col) in shape:
                    # The diagonal is part of the shape. This can only be a corner piece if
                    # the neighbouring squares aren't part of the shape.
                    if (neighbour_one not in shape) and (neighbour_two not in shape):
                        corners += 1
                # XOR: True/True -> False | False/False -> False
                elif not ((neighbour_one in shape) ^ (neighbour_two in shape)):
                    corners += 1

            return corners

        return sum(cell_corners(r, c) for r, c in shape)

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

    @property
    def total_price2(self):
        result = 0
        for region_id in sorted(self.region_dict.keys()):
            region_price = self.region_area(region_id) * self.region_corners(region_id)
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
            for di, dj in moves:
                ni, nj = i + di, j + dj
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
    """Part 2
    with help from:
    https://github.com/jda5/advent-of-code-2024/blob/main/12/main.py
    """
    g = Grid(data)
    result = g.total_price2
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
