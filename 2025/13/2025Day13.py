"""Everybody Codes - Quest 13, Year 2025
Solution Started: November 19, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/13
Solution by: Abbas Moosajee
Brief: [Unlocking the Mountain]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import deque
from itertools import cycle
import time
start_time = time.time()
# List of input file names
input_files = ["Day13_input_p1.txt", "Day13_input_p2.txt", "Day13_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class LockDials:
    def __init__(self, dial_vals):
        self.dial_nums = dial_vals

    def build_basic_dial(self, init_num = 1):
        full_dial = deque([init_num])
        for idx, val in enumerate(self.dial_nums[:], start=1):
            if idx % 2 == 0: # place left
                full_dial.appendleft(val)
            else: # place_right
                full_dial.append(val)
        return full_dial

    def build_expanded_dial(self, init_num = 1):
        full_dial = deque([init_num])
        for idx, data in enumerate(self.dial_nums[:], start=1):
            val_1, val_2 = list(map(int, data.split("-")))
            num_list = list(range(val_1, val_2 + 1))
            print(idx, val_1, val_2, len(num_list), len(full_dial))
            if idx % 2 == 0: # place left
                full_dial.extendleft(num_list)
            else: # place_right
                full_dial.extend(num_list)
        return full_dial

    def turn_dial(self, turns, expansion = False):
        start_num = 1
        if expansion:
            dial_built = self.build_expanded_dial(start_num)
        else:
            dial_built = self.build_basic_dial(start_num)
        start_idx = dial_built.index(start_num)
        final_idx = (start_idx + turns) % len(dial_built)
        # print(start_idx, final_idx, dial_built[final_idx])
        return dial_built[final_idx]

    def turn_dial_express(self, turns):
        clock = deque([range(1, 1+1)])
        left = []
        for idx, data in enumerate(self.dial_nums):
            val_1, val_2 = map(int, data.split("-"))
            if idx % 2 == 0:
                clock.append(range(val_1, val_2+1))
            else:
                left.append(range(val_2, val_1-1, -1))
        clock.extend(reversed(left))

        left = turns % sum(map(len, clock))
        for r in cycle(clock):
            if left < (length := len(r)):
                return r[left]
            left -= length
        return None

dials_p1 = LockDials(input_data_p1)
turn_dials_p1 = dials_p1.turn_dial(2025)
print("Quest 13, P1:", turn_dials_p1)

dials_p2 = LockDials(input_data_p2)
turn_dials_p2 = dials_p2.turn_dial_express(20252025)
print("Quest 13, P2:", turn_dials_p2)

dials_p3 = LockDials(input_data_p3)
turn_dials_p3 = dials_p3.turn_dial_express(202520252025)
print("Quest 13, P2:", turn_dials_p3)


# print(f"Execution Time: {time.time() - start_time:5f}s")