from collections import deque
from dataclasses import dataclass, field
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


@dataclass
class Computer:
    """_summary_
    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs.
    """

    A: int
    B: int
    C: int
    program: list[int]
    pointer: int = 0
    output: list[int] = field(default_factory=list)

    def combo(self, operand: int) -> int:
        if operand in (0, 1, 2, 3):
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        elif operand == 7:
            raise ValueError(
                "Combo operand 7 is reserved and will not appear in valid programs."
            )
        else:
            raise ValueError(f"Unknown combo operand {operand}")

    def adv(self, operand):
        """
        The adv instruction (opcode 0) performs division. The numerator is the value in
        the A register. The denominator is found by raising 2 to the power of the instruction's
        combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5
        would divide A by 2^B.) The result of the division operation is truncated
        to an integer and then written to the A register.
        """
        self.A = self.A // (2 ** self.combo(operand))
        self.pointer += 2

    def bxl(self, operand):
        """
        The bxl instruction (opcode 1) calculates the bitwise XOR of register B and
        the instruction's literal operand, then stores the result in register B.
        """
        self.B = self.B ^ operand
        self.pointer += 2

    def bst(self, operand):
        """
        The bst instruction (opcode 2) calculates the value of its combo operand
        modulo 8 (thereby keeping only its lowest 3 bits), then writes that value
        to the B register.
        """
        self.B = self.combo(operand) % 8
        self.pointer += 2

    def jnz(self, operand):
        """
        The jnz instruction (opcode 3) does nothing if the A register is 0.
        However, if the A register is not zero, it jumps by setting the instruction
        pointer to the value of its literal operand; if this instruction jumps,
        the instruction pointer is not increased by 2 after this instruction.
        """
        if self.A != 0:
            self.pointer = operand
        else:
            self.pointer += 2

    def bxc(self, operand):
        """
        The bxc instruction (opcode 4) calculates the bitwise XOR of register B
        and register C, then stores the result in register B. (For legacy reasons,
        this instruction reads an operand but ignores it.)
        """
        self.B = self.B ^ self.C
        self.pointer += 2

    def out(self, operand):
        """
        The out instruction (opcode 5) calculates the value of its combo operand
        modulo 8, then outputs that value. (If a program outputs multiple values,
        they are separated by commas.)
        """
        self.output.append(self.combo(operand) % 8)
        self.pointer += 2

    def bdv(self, operand):
        """
        The bdv instruction (opcode 6) works exactly like the adv instruction except
        that the result is stored in the B register. (The numerator is still read
        from the A register.)
        """
        self.B = self.A // (2 ** self.combo(operand))
        self.pointer += 2

    def cdv(self, operand):
        """
        The cdv instruction (opcode 7) works exactly like the adv instruction except
        that the result is stored in the C register. (The numerator is still read
        from the A register.)
        """
        self.C = self.A // (2 ** self.combo(operand))
        self.pointer += 2

    def run_program(self, early_exit=False):
        self.pointer = 0
        self.output = []
        while self.pointer < (len(self.program) - 1):
            opcode, operand = self.program[self.pointer], self.program[self.pointer + 1]
            if opcode == 0:
                self.adv(operand)
            elif opcode == 1:
                self.bxl(operand)
            elif opcode == 2:
                self.bst(operand)
            elif opcode == 3:
                self.jnz(operand)
            elif opcode == 4:
                self.bxc(operand)
            elif opcode == 5:
                self.out(operand)
            elif opcode == 6:
                self.bdv(operand)
            elif opcode == 7:
                self.cdv(operand)
            else:
                raise ValueError(f"Unknown opcode {opcode}")

            if early_exit and len(self.output) > 0:
                if len(self.output) >= len(self.program):
                    break
                last_index = len(self.output) - 1
                if self.output[last_index] != self.program[last_index]:
                    break


def parse_data(data) -> Computer:
    a, b, c = 0, 0, 0
    program = []
    for line in data:
        if line.startswith("Register A: "):
            a = int(line.split(": ")[1])
        elif line.startswith("Register B: "):
            b = int(line.split(": ")[1])
        elif line.startswith("Register C: "):
            c = int(line.split(": ")[1])
        elif line.startswith("Program: "):
            instructions = line.split(": ")[1]
            program = [int(x) for x in instructions.split(",")]
    return Computer(a, b, c, program)


def part1(data):
    """Part 1"""
    computer = parse_data(data)
    computer.run_program()
    result = ",".join(str(x) for x in computer.output)
    return result


def part2(data):
    """Part 2

    Credit to Dustin Bowers for the solution.
    https://github.com/dustinbowers/advent-of-code/blob/main/2024/day17_chronospatial_computer/main.py
    """
    computer = parse_data(data)
    b = computer.B
    c = computer.C
    target_output = computer.program.copy()
    queue = deque()
    queue.append((0, 1))

    while queue:
        a, n = queue.popleft()
        if n > len(target_output):  # Base
            return a

        for i in range(8):
            a2 = (a << 3) | i
            computer = Computer(a2, b, c, target_output)
            computer.run_program()

            # save correct partial solutions
            if computer.output == target_output[-n:]:
                queue.append((a2, n + 1))
    return False


if __name__ == "__main__":
    print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
