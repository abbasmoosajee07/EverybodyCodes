
# Everybody Codes - Day 8, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/8
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
# List of input file names
input_files = ["Day08_p1_input.txt", "Day08_p2_input.txt", "Day08_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1),print(input_data_p2), print(input_data_p3)

def odd_numbers():
    n = 1
    while True:
        yield n
        n += 2

def count_special_blocks(input):
    blocks_remaining = int(input[0])

    for n in odd_numbers():
        if blocks_remaining > n:
            blocks_remaining -= n
        else:
            would_need = n - blocks_remaining
            return n * would_need
    
    raise RuntimeError("Unreachable code reached")

ans_p1 = count_special_blocks(input_data_p1)
print(f"Quest 1: {ans_p1}")

def build_shrine(input):
    priests = int(input[0])
    blocks = 20240000
    acolytes = 1111
    thick = 1

    for n in odd_numbers():
        n = n * thick
        if blocks > n:
            blocks -= n
        else:
            would_need = n - blocks
            ans = (n * would_need) / thick
            return int(ans)
        thick = (thick * priests) % acolytes

    raise RuntimeError("Unreachable code reached")

ans_p2 = build_shrine(input_data_p2)
print(f"Quest 2: {ans_p2}")

def complete_shrine(input):
    input_value = int(input[0])
    target = 202400000
    high_priest_acolytes = 10
    thickness = 1
    shape = [1]  # Start with a list containing the initial shape value

    while True:
        # Update thickness with modular multiplication
        thickness = (thickness * input_value) % high_priest_acolytes + high_priest_acolytes
        
        # Update shape by adding values to the start, middle, and end
        shape = [thickness] + [s + thickness for s in shape] + [thickness]
        
        # Calculate width, full, and remove
        width = len(shape)
        full = sum(shape)
        remove = sum((input_value * width * np.array(shape[1:-1])) % high_priest_acolytes)
        
        # Calculate total and check against target
        total = full - remove
        if total > target:
            out = total - target
            break

    return out

ans_p3 = complete_shrine(input_data_p3)
print(f"Quest 3: {ans_p3}")
