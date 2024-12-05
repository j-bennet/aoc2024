from os import path
from pprint import pformat

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    rules = []
    updates = []
    with open(full_name) as f:
        for line in f.read().splitlines():
            line = line.strip()
            if not line:
                continue
            if "|" in line:
                parts = list(map(int, line.split("|")))
                rules.append(parts)
            else:
                parts = list(map(int, line.split(",")))
                updates.append(parts)
    return rules, updates


class RuleGraph:
    def __init__(self, rules):
        self.rules = rules
        self.g = {}
        self.build_graph()
        self.correct_order = self.traverse()
        self.positions = {node: i for i, node in enumerate(self.correct_order)}

    def build_graph(self):
        for parent, child in self.rules:
            if parent not in self.g:
                self.g[parent] = set()
            if child not in self.g:
                self.g[child] = set()
            self.g[parent].add(child)

    def check_topo(self, topo: list[int]) -> bool:
        """Positions should be in increasing order"""
        max_seen_position = -1
        for node in topo:
            if self.positions[node] < max_seen_position:
                return False
            max_seen_position = self.positions[node]
        return True

    def middle_sum(self, updates: list[list[int]]) -> int:
        result = 0
        for update in updates:
            if self.check_topo(update):
                m = len(update) // 2
                # print(f"{update=}, {m=}, {update[m]=}")
                result += update[m]
        return result

    def traverse(self):
        path = []
        visited = set()
        for node in self.g:
            self.dfs(node, path, visited)
        return list(reversed(path))

    def dfs(self, node, path, visited):
        if node in visited:
            return
        visited.add(node)
        for child in self.g[node]:
            self.dfs(child, path, visited)
        path.append(node)

    def __str__(self) -> str:
        return pformat(self.g)


def part1(data):
    """Part 1"""
    rules, updates = data
    g = RuleGraph(rules)
    # print(g)
    # print(g.correct_order)
    result = g.middle_sum(updates)
    return result


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
