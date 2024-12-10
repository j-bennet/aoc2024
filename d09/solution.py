from dataclasses import dataclass, field
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


@dataclass
class Block:
    free: int
    taken: int
    contents: list[int] = field(default_factory=list)

    def __str__(self):
        data = self.contents[:]
        if self.free > 0:
            data += ["."] * self.free
        return str(data)

    def can_take(self, other):
        return self.free >= other.taken

    @property
    def file_id(self):
        if self.contents:
            return self.contents[0]
        return "."

    @property
    def is_full(self):
        return self.free == 0

    def take(self, other):
        self.taken += other.taken
        self.free -= other.taken
        self.contents += other.contents
        other.taken, other.free, other.contents = other.free, other.taken, []


class Disk2:
    def __init__(self, data):
        self.data = data
        self.nums = [int(x) for x in data]
        self.blocks = []
        self.make_blocks()

    def make_blocks(self):
        file_index = 0
        for i, n in enumerate(self.nums):
            if i % 2 == 0:
                self.blocks.append(Block(0, n, [file_index] * n))
                file_index += 1
            else:
                if n > 0:
                    self.blocks.append(Block(n, 0, []))

    def maybe_move(self, source_index):
        for i, block in enumerate(self.blocks):
            if i >= source_index:
                break
            if block.can_take(self.blocks[source_index]):
                # print(
                #     f"Move {self.blocks[source_index]} at {source_index} to {block} at {i}"
                # )
                block.take(self.blocks[source_index])
                # print(self)
                return True
        return False

    def compress(self):
        moved_file_ids = set()
        for i in range(len(self.blocks) - 1, 0, -1):
            if self.blocks[i].file_id in moved_file_ids:
                continue
            if self.blocks[i].is_full:
                self.maybe_move(i)
                moved_file_ids.add(self.blocks[i].file_id)

    @property
    def checksum(self):
        result = 0
        i = 0
        for block in self.blocks:
            for file_id in block.contents:
                result += i * file_id
                i += 1
            i += block.free
        return result

    def __str__(self):
        return "".join(map(str, self.blocks))


def part1(data):
    """Part 1"""
    disk = Disk(data[0])
    # print(disk)
    # print("-" * 10)
    return disk.checksum


def part2(data):
    """Part 2"""
    disk = Disk2(data[0])
    disk.compress()
    # print(disk)
    # print("-" * 10)
    return disk.checksum


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
