from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


class Graph:
    def __init__(self, data, part=1):
        self.data = data
        self.h = len(data)
        self.w = len(data[0])
        self.antennas = {}
        self.antennas_by_point = {}
        self.antenodes = set()
        self.parse()
        if part == 1:
            self.find_antenodes()
        else:
            self.find_antenodes2()

    def parse(self):
        for i, row in enumerate(self.data):
            for j, x in enumerate(row):
                if x != ".":
                    if x not in self.antennas:
                        self.antennas[x] = []
                    self.antennas_by_point[(i, j)] = x
                    self.antennas[x].append((i, j))

    def find_antenode_for_pair(self, p1, p2):
        i1, j1 = p1
        i2, j2 = p2
        di, dj = i2 - i1, j2 - j1
        i, j = i2 + di, j2 + dj
        if 0 <= i < self.h and 0 <= j < self.w:
            return (i, j)

    def find_antenodes_for_pair(self, p1, p2):
        i1, j1 = p1
        i2, j2 = p2
        di, dj = i2 - i1, j2 - j1
        i, j = i2 + di, j2 + dj
        nodes = set()
        while 0 <= i < self.h and 0 <= j < self.w:
            nodes.add((i, j))
            i, j = i + di, j + dj
        return nodes

    def find_ante_antenodes_for_pair(self, p1, p2):
        i1, j1 = p1
        i2, j2 = p2
        di, dj = i2 - i1, j2 - j1
        i, j = i2 + di, j2 + dj
        nodes = set()
        while 0 <= i < self.h and 0 <= j < self.w:
            if (i, j) in self.antennas_by_point:
                nodes.add((i, j))
            i, j = i + di, j + dj
        return nodes

    def find_antenodes(self):
        for points in self.antennas.values():
            for p1 in points:
                for p2 in points:
                    if p1 != p2:
                        if antenode := self.find_antenode_for_pair(p1, p2):
                            self.antenodes.add(antenode)

    def find_antenodes2(self):
        for points in self.antennas.values():
            for p1 in points:
                for p2 in points:
                    if p1 != p2:
                        if antenodes := self.find_antenodes_for_pair(p1, p2):
                            self.antenodes.update(antenodes)
        antenna_antenodes = set()
        for p1 in self.antenodes:
            for p2 in self.antenodes:
                if p1 != p2:
                    if antenodes := self.find_ante_antenodes_for_pair(p1, p2):
                        antenna_antenodes.update(antenodes)
        self.antenodes.update(antenna_antenodes)

    def __str__(self):
        result = []
        for i in range(self.h):
            row = []
            for j in range(self.w):
                if (i, j) in self.antenodes:
                    row.append("#")
                else:
                    row.append(self.data[i][j])
            result.append("".join(row))
        return "\n".join(result)


def part1(data):
    """Part 1"""
    graph = Graph(data)
    # print(graph)
    # print("---")
    return len(graph.antenodes)


def part2(data):
    """Part 2"""
    graph = Graph(data, part=2)
    # print(graph)
    # print("---")
    return len(graph.antenodes)


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
