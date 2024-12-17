from solution import Computer

# If register C contains 9, the program 2,6 would set register B to 1.
computer = Computer(0, 0, 9, [2, 6])
computer.run_program()
assert computer.B == 1


# If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
computer = Computer(10, 0, 0, [5, 0, 5, 1, 5, 4])
computer.run_program()
assert computer.output == [0, 1, 2]


# If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0
# and leave 0 in register A.
computer = Computer(2024, 0, 0, [0, 1, 5, 4, 3, 0])
computer.run_program()
assert computer.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
assert computer.A == 0


# If register B contains 29, the program 1,7 would set register B to 26.
computer = Computer(0, 29, 0, [1, 7])
computer.run_program()
assert computer.B == 26

# If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
computer = Computer(0, 2024, 43690, [4, 0])
computer.run_program()
assert computer.B == 44354
