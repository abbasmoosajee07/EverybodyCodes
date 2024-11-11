# Everybody Codes - Day 4, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/4
# Solution by: [abbasmoosajee07]
# Brief: [Number list and loops]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D4_file = "Day4_input.txt"
D4_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D4_file)

# Read and sort input data into a grid
with open(D4_file_path) as file:
    input_data = file.read().strip().split('\n')

    input_list_p1 = input_data[0:11]
    input_list_p2 = input_data[12:212]
    input_list_p3 = input_data[213:]

def find_median(numbers):
    # Sort the list
    numbers.sort()

    # Get the length of the list
    n = len(numbers)

    # If the length is odd, return the middle element
    if n % 2 != 0:
        return numbers[n // 2]
    else:
        # If the length is even, return the average of the two middle elements
        mid1, mid2 = numbers[n // 2 - 1], numbers[n // 2]
        return (mid1 + mid2) / 2

def count_hammer_strikes(nail_str, level = False):
    hammer_count = 0
    nail_list = [int(num) for num in nail_str]
    smallest_nail = min(nail_list)
    
    if level is False:
        for nail in nail_list:
            hammer_strikes = nail - smallest_nail
            hammer_count += hammer_strikes
    else:
        smallest_nail = int(find_median(nail_list))
        for nail in nail_list:
            hammer_strikes = abs(nail - smallest_nail)
            hammer_count += hammer_strikes

    return hammer_count

hammer_p1 = count_hammer_strikes(input_list_p1)
print(f"Part 1: {hammer_p1}")

hammer_p2 = count_hammer_strikes(input_list_p2)
print(f"Part 2: {hammer_p2}")

hammer_p3 = count_hammer_strikes(input_list_p3, level=True)
print(f"Part 3: {hammer_p3}")