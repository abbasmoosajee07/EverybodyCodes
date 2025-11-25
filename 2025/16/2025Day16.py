"""Everybody Codes - Quest 16, Year 2025
Solution Started: November 24, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/16
Solution by: Abbas Moosajee
Brief: [Harmonics of Stone]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
import numpy as np
import time
start_time = time.time()

# List of input file names
input_files = ["Day16_input_p1.txt", "Day16_input_p2.txt", "Day16_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class Stones:
    def __init__(self, inp_data):
        self.input_notes = list(map(int, inp_data.split(",")))

    def build_wall(self, columns):
        total_columns = list(range(1, columns + 1))
        wall = defaultdict(list)
        for spell in self.input_notes:
            for wall_idx in total_columns:
                if wall_idx % spell == 0:
                    wall[wall_idx].append(1)
        return sum(len(col) for col in wall.values())

    def identify_spell(self):
        wall = defaultdict(int)
        for idx, col_size in enumerate(self.input_notes, 1):
            wall[idx] = col_size

        spells = []
        columns = len(wall)

        # process small → large
        for s in range(1, columns + 1):
            if wall[s] > 0:
                spells.append(s)
                for m in range(2 * s, columns + 1, s):
                    wall[m] -= 1
        return spells

    def identify_wall_len(self, avail_blocks):
        def blocks_used(length, all_spells):
            return sum(len(range(spell-1, length, spell)) for spell in all_spells)

        charms = self.identify_spell()
        upper = 1_000_000_000_000_000
        lower = len(self.input_notes)
        while lower < upper:
            mid = (lower + upper) // 2
            if blocks_used(mid, charms) < avail_blocks:
                lower = mid
            else:
                upper = mid - 1
        return lower

stones_p1 = Stones(input_data_p1[0])
blocks_p1 = stones_p1.build_wall(90)
print("Quest 16, P1:", blocks_p1)

stones_p2 = Stones(input_data_p2[0])
spell = stones_p2.identify_spell()
print("Quest 16, P2:", np.prod(spell))

stones_p3 = Stones(input_data_p3[0])
blocks_p3 = stones_p3.identify_wall_len(202520252025000)
print("Quest 16, P3:", blocks_p3)

# print(f"Execution Time: {time.time() - start_time:5f}s")