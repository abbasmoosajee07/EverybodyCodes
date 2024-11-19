# Everybody Codes - Day 5, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/5
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the input data from the specified file path
D5_file = "Day5_input.txt"
D5_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D5_file)

# Read and sort input data into a grid
with open(D5_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_data_p1 = input_data[0:5]
    input_data_p2 = input_data[6:104]
    input_data_p3 = input_data[106:]

def pseudo_clap_dance(input_data, iterations, part = 1):
    # Initialise Variables
    columns = []
    dance_result = []
    target_count = 0
    count = {}
    # Convert the input into columns
    for line in input_data:
        values = line.split(" ")
        for i in range(len(values)):
            if i >= len(columns):
                columns.append([])
            columns[i].append(int(values[i]))

    clap_idx = 0
    for r in range(1,iterations + 1):
        clapper = columns[clap_idx].pop(0)
        target_column = columns[(clap_idx + 1) % 4]

        # Calculate the moves (absolute value)
        moves = abs((clapper % (len(target_column) * 2)) - 1)
        if moves > len(target_column):
            moves = (len(target_column) * 2) - moves

        target_column.insert(moves, clapper)
        clap_idx = (clap_idx + 1) % len(columns)
        number_shouted = ''.join(str(col[0]) for col in columns)
        dance_result.append(int(number_shouted))
        if number_shouted == '12111010':
            target_count += 1
            # print(target_count,r,number_shouted)

        # Update count dictionary
        count[number_shouted] = count.get(number_shouted, 0) + 1

        # Check if the result has been reached 2024 times
        if count[number_shouted] == 2024:
            freq_2024 = r * int(number_shouted)
            return freq_2024

        r += 1

        # Join the first elements of each column into the result string
        number_shouted = ''.join(str(col[0]) for col in columns)

    if part == 1:
        return dance_result[-1]
    elif part == 3:
        return max(dance_result)

clapper_p1 = pseudo_clap_dance(input_data_p1, 10, 1)
print(f"Quest 1: {clapper_p1}")

clapper_p2 = pseudo_clap_dance(input_data_p2, 1800000, 2)
print(f"Quest 2: {clapper_p2}")

clapper_p3 = pseudo_clap_dance(input_data_p3, 1800000, 3)
print(f"Quest 3: {clapper_p3}")
