"""Everybody Codes - Quest 2, Year 2025
Solution Started: November 5, 2025
Puzzle Link: https://everybody.codes/event/20252/quests/2
Solution by: Abbas Moosajee
Brief: [From Complex to Clarity]"""

#!/usr/bin/env python3
from pathlib import Path
import numpy as np

# List of input file names
input_files = ["Day02_input_p1.txt", "Day02_input_p2.txt", "Day02_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class ComplexNumbers:
    def __init__(self, vec_str) -> None:
        self.inp_vec = self.parse_vector(vec_str)
        self.div_vec = [10, 10]


    def parse_vector(self, inp_str):
        stripped_vec = inp_str.split("=")[1].strip("[]")
        split_vec = stripped_vec.split(",")
        return [int(split_vec[0]), int(split_vec[1])]

    def run_cycle(self, vector, add_vec = [0, 0]):
        X, Y = vector
        AX, AY = add_vec
        DX, DY = self.div_vec

        # multiply
        new_x = X * X - Y * Y
        new_y = X * Y + Y * X

        # divide (integer truncation)
        new_x = int(new_x / DX)
        new_y = int(new_y / DY)

        # add
        new_x += AX
        new_y += AY
        return [new_x, new_y]

    def run_total_cycles(self, total_cycles = 3):
        init_vec = [0, 0]
        for cycle in range(total_cycles):
            new_vec = self.run_cycle(init_vec, self.inp_vec)
            init_vec = new_vec
        return init_vec

    def engrave_grid(self, size = 1000, precision = 10):
        base_grid = self.build_grid(self.inp_vec, size, precision)
        self.div_vec = [100000,100000]
        for coords in base_grid.keys():
            init_vec = [0, 0]
            base_grid[coords] = 1
            for cycle in range(100):
                new_vec = self.run_cycle(init_vec, coords)
                if new_vec[0] <= -1_000_000 or new_vec[0] >= 1_000_000 or new_vec[1] <= -1_000_000 or new_vec[1] >= 1_000_000:
                    base_grid[coords] = 0
                    break  # stops immediately when outside bounds
                init_vec = new_vec
        return base_grid

    def build_grid(self, origin, size, precision):
        grid = {}
        for row in range(origin[0], origin[0] + size + precision, precision):
            for col in range(origin[1], origin[1] + size + precision, precision):
                grid[row, col] = 0
        return grid

complex_p1 = ComplexNumbers(input_data_p1[0])
vec_ans_p1 = complex_p1.run_total_cycles()
print("Quest 2, P1:", f"[{vec_ans_p1[0]},{vec_ans_p1[1]}]")

complex_p2 = ComplexNumbers(input_data_p2[0])
grid_p2 = complex_p2.engrave_grid()
print("Quest 2, P2:", sum(grid_p2.values()))

# input_data_p3 = ["A=[35300,-64910]"]
complex_p3 = ComplexNumbers(input_data_p3[0])
grid_p3 = complex_p3.engrave_grid(size = 1000, precision = 1)
print("Quest 2, P3:", sum(grid_p3.values()))
