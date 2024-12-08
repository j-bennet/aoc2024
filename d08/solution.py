from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


class Graph:
    def __init__(self, data):
        self.data = data
        self.h = len(data)
        self.w = len(data[0])
        self.antennas = {}
        self.antenodes = set()
        self.parse()
        self.find_antenodes()

    def parse(self):
        for i, row in enumerate(self.data):
            for j, x in enumerate(row):
                if x != ".":
                    if x not in self.antennas:
                        self.antennas[x] = []
                    self.antennas[x].append((i, j))

    def find_antenode(self, p1, p2):
        i1, j1 = p1
        i2, j2 = p2
        di = i2 - i1
        dj = j2 - j1
        i = i2 + di
        j = j2 + dj
        if 0 <= i < self.h and 0 <= j < self.w:
            return (i, j)

    def find_antenodes(self):
        for atype in self.antennas:
            for p1 in self.antennas[atype]:
                for p2 in self.antennas[atype]:
                    if p1 != p2:
                        if antenode := self.find_antenode(p1, p2):
                            self.antenodes.add(antenode)

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
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
