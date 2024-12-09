from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


class Disk:
    def __init__(self, data):
        self.data = data
        self.nums = [int(x) for x in data]
        self.sparse = []
        self.make_sparse()
        self.compress()

    def make_sparse(self):
        file_index = 0
        for i, n in enumerate(self.nums):
            if i % 2 == 0:
                self.sparse.extend([file_index] * n)
                file_index += 1
            else:
                self.sparse.extend(["."] * n)

    def compress(self):
        left_index = 0
        right_index = len(self.sparse) - 1
        while left_index < right_index:
            while self.sparse[left_index] != ".":
                left_index += 1
            while self.sparse[right_index] == ".":
                right_index -= 1
            if left_index >= right_index:
                break
            self.sparse[left_index], self.sparse[right_index] = (
                self.sparse[right_index],
                self.sparse[left_index],
            )

    @property
    def checksum(self):
        return sum(i * num for i, num in enumerate(self.sparse) if num != ".")

    def __str__(self):
        return "".join(map(str, self.sparse))


def part1(data):
    """Part 1"""
    disk = Disk(data[0])
    # print(disk)
    # print("-" * 10)
    return disk.checksum


def part2(data):
    """Part 2"""
    result = 0
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('example.txt'))}")
