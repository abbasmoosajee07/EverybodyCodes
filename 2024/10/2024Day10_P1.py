
# Everybody Codes - Day 10, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/10
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# List of input file names
input_files = ["Day10_p1_input.txt", "Day10_p2_input.txt", "Day10_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def create_letter_grid(input_data):
    grid = []
    for line in input_data:
        split_line = list(line)
        grid.append(split_line)
    return np.array(grid)

def complete_grid(grid):
    updated_grid = copy.deepcopy(grid)
    # Initialize variables
    letter_string = []
    ignore = {".", "?"}  # Use a set for efficient lookups

    index_list = [(row, col) for row, subarray in enumerate(grid) for col, value in enumerate(subarray) if value in ignore]

    for index in index_list:

        row_letters = grid[index[0]]
        col_letters = grid[:,index[1]]
        common_letter = [letter for letter in row_letters if letter in col_letters and letter not in ignore]
        if common_letter == []:
            pass
        else:
            updated_grid[index] = common_letter[0]
            letter_string.append(str(common_letter[0]))
    return ''.join(letter_string), letter_string, updated_grid

grid_p1 = create_letter_grid(input_data_p1)
ans_p1, _, new = complete_grid(grid_p1)
print(f"Part 1: {ans_p1}")

def divide_grid(input_data, grid_size = 8):

    # Filter out empty lines
    filtered_grid = [line for line in input_data if line != ""]

    split_grid = []
    for row, line in enumerate(filtered_grid):
        # print(row, line)
        split_line = line.split(' ')
        split_grid.append(split_line)

    # Split the filtered grid into smaller grids
    smaller_grids = []

    for i in range(0, len(split_grid), grid_size):
        grid_chunk = split_grid[i:i + grid_size]  # Get 5 rows at a time
        smaller_grids.append(grid_chunk)

    grid_list = []
    for grid_row in smaller_grids:
        for grid_no in range(len(grid_row[0])):
            small_grid = []
            for row in range(grid_size):
                string = grid_row[row][grid_no]
                small_grid.append(string)
            grid_list.append(small_grid)

    return grid_list # Return the list of divide grid list

def calc_rune_power(rune_string):
    base_power = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
    'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15,
    'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22,
    'W': 23, 'X': 24, 'Y': 25, 'Z': 26
    }
    rune_power = 0
    for pos, letter in enumerate(rune_string):
        score = (pos + 1) * base_power.get(letter, 0)  # Handle cases where letter is not found
        rune_power += score
    return rune_power

def total_power(grid_list):
    power_list = []
    total_power = 0
    for small_grid in grid_list:
        grid_array = create_letter_grid(small_grid)
        runic_word, letter_string, new_grid = complete_grid(grid_array)
        rune_score = calc_rune_power(letter_string)
        total_power += rune_score
        power_list.append([runic_word,int(rune_score)])
    return total_power, np.array(power_list)

grid_list_p2 = divide_grid(input_data_p2)
ans_p2, runes_p2 = total_power(grid_list_p2)
print(f"Part 2: {ans_p2}")

# 92428  Wrong
# 104930 Digit and len correct