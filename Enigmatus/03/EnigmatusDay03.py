"""# Everybody Codes - Day 3, Story Enigmatus
# Solved in Jun, 2025
# Puzzle Link: https://everybody.codes/story/1/quests/3
# Solution by: [abbasmoosajee07]
# Brief: [The Conical Snail Clock]
"""

#!/usr/bin/env python3

import os, re, copy, time
from math import gcd
import numpy as np
start_time = time.time()

# List of input file names
input_files = ["Day03_p1_input.txt", "Day03_p2_input.txt", "Day03_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

class SnailClock:
    def __init__(self, init_pos):
        self.snail_dict = self.build_clock(init_pos)

    def build_clock(self, init_pos):
        snail_dict = {}
        self.clock_size = {}
        for snail_no, snail_pos in enumerate(init_pos, start=1):
            x_pos, y_pos = snail_pos.split()
            x_int = int(x_pos.strip('x='))
            y_int = int(y_pos.strip('y='))
            snail_dict[snail_no] = (x_int, y_int)
            x_min, y_max = x_int, y_int
            while x_min > 1:
                x_min -= 1
                y_max += 1
            self.clock_size[snail_no] = y_max
        return snail_dict

    def move_snail(self, no, pos):
        xi, yi = pos
        max_y = self.clock_size[no]

        if yi > 1:
            return (xi + 1, yi - 1)
        else:
            return (1, max_y)

    def run_clock(self, total_days):
        final_status = {}
        for snail_id, pos in self.snail_dict.items():
            for day in range(total_days):
                pos = self.move_snail(snail_id, pos)
            final_status[snail_id] = pos
        return self.calculate_snail_sum(final_status)

    @staticmethod
    def calculate_snail_sum(final_status):
        snail_sum = [
            (x + (100 * y))
            for x, y in final_status.values()
        ]
        return snail_sum

    def reqd_days(self):
        days_to_1 = []
        for snail_id, pos in self.snail_dict.items():
            shift = pos[1]  # how many days until y=1 initially
            cycle = self.clock_size[snail_id]  # repeat cycle length
            days_to_1.append((shift % cycle, cycle))

        def lcm(a, b):
            return a * b // gcd(a, b)

        # Combine congruences: x ≡ r_i mod m_i
        def combine(a1, m1, a2, m2):
            # Find x ≡ a1 mod m1 and x ≡ a2 mod m2
            # Brute-force alignment since cycles may not be coprime
            x = a1
            while x % m2 != a2:
                x += m1
            return x, lcm(m1, m2)

        result, modulus = days_to_1[0]
        for shift, cycle in days_to_1[:]:
            result, modulus = combine(result, modulus, shift, cycle)

        return result - 1

snails_p1 = SnailClock(input_data_p1).run_clock(100)
print("Quest 1:", sum(snails_p1))


snails_p2 = SnailClock(input_data_p2).reqd_days()
print("Quest 2:", snails_p2)

snails_p3 = SnailClock(input_data_p3).reqd_days()
print("Quest 3:", snails_p3)


print(f"Execution Time = {time.time() - start_time:.5f}s")
