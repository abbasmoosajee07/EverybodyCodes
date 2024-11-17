
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
input_files = ["Day10_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
print(input_data_p3)

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

ignore = {".", "?"}  # Use a set for efficient lookups
def add_runic_letters(grid, size=6):
    """
    Process the entire grid to fill in missing letters for all sub-grids.
    """
    for row_no in range(size, len(grid), size):
        for col_no in range(size, len(grid[row_no]), size):
            # Extract a sub-grid (6x6 area with a 2-cell border)
            extracted_grid = [row[col_no-size:col_no+2] for row in grid[row_no-size:row_no+2]]

            # Fill missing symbols in the extracted grid
            new_grid = fill_missing_symbol(extracted_grid)

            # Update the main grid with the completed sub-grid
            for i, row in enumerate(range(row_no-size, row_no+2)):
                grid[row][col_no-size:col_no+2] = new_grid[i]
    return grid

def fill_missing_symbol(grid):
    """
    Fill missing symbols ('.' and '?') in the given grid by ensuring each
    symbol is unique in its row and column.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Iterate over each cell in the grid
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in {'.', '?'}:  # Only process missing symbols
                # Get symbols already in the same row and column
                row_symbols = set(grid[r]) - {'.', '?'}
                col_symbols = set(grid[i][c] for i in range(rows)) - {'.', '?'}

                # All possible symbols
                all_symbols = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                
                # Find the missing symbol for the current cell
                missing_symbol = (all_symbols - row_symbols - col_symbols).pop()
                
                # Replace the current cell with the missing symbol
                grid[r][c] = missing_symbol
    return grid


og_grid_p3 = create_letter_grid(input_data_p3)
index_list_rune = [(row, col) for row, subarray in enumerate(og_grid_p3) for col, value in enumerate(subarray) if value == '.']
# Create a list of indices with missing letters
ignore = {'.', '?'}
index_list1 = [(row, col) for row, subarray in enumerate(og_grid_p3) for col, value in enumerate(subarray) if value in ignore]
print(f"Initial missing letter count: {len(index_list1)}")

# Process the grid to fill in all missing letters
new_grid_p3 = add_runic_letters(og_grid_p3)

# Verify and print the final grid
for row in new_grid_p3:
    print(''.join(row))

# Count remaining missing letters (should be 0)
index_list_con = [(row, col) for row, subarray in enumerate(new_grid_p3) for col, value in enumerate(subarray) if value in ignore]
print(f"Remaining missing letter count: {len(index_list_con)}")

rune_p3 = []
for index in index_list_rune:
    rune_letter = new_grid_p3[index]
    new_grid_p3[index] ='.'
    rune_p3 += rune_letter
ans_p3 = calc_rune_power(rune_p3)
print(ans_p3)

# Verify and print the final grid
for row in new_grid_p3:
    print(''.join(row))