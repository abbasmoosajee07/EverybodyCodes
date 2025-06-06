"""# Everybody Codes - Day 1, Year Enigmatus
# Solved in Jun, 2025
# Puzzle Link: https://everybody.codes/story/1/quests/1
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# List of input file names
input_files = ["Day01_p1_input.txt", "Day01_p2_input.txt", "Day01_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
print(input_data_p1), print(input_data_p2), print(input_data_p3)
print(f"Execution Time = {time.time() - start_time:.5f}s")
