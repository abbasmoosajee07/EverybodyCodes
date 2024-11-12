# Everybody Codes - Day 3, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/3
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import Counter

# Load the input data from the specified file path
D3_file = "Day3_input.txt"
D3_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D3_file)

# Read and sort input data into a grid
with open(D3_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_data_p1 = input_data[0:14]
    input_data_p2 = input_data[15:49]
    input_data_p3 = input_data[51:]

def find_nearby_ground(earth_grid, x, y, royal_lands):
    
    if royal_lands is False:
    # Directions for 4 possible movements: up, down, left, right
        directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]
    else:
        # Define the directions of neighboring cells: 8 directions around (x, y)
        directions = [(-1, -1), (0, -1), (+1, -1),
                      (-1,  0),          (+1,  0),
                      (-1, +1), (0, +1), (+1, +1)]

    # Initialize the count dictionary
    land_mined = []
    current_earth = earth_grid[y][x]

    # Iterate through the 8 directions
    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        # Ensure correct bounds check and indexing
        if 0 <= ny < len(earth_grid) and 0 <= nx < len(earth_grid[0]):  # ny for row, nx for column
            # Add logic to check if it's a land type you're interested in, e.g., 'land'
            # print(x, y, current_earth, nx, ny)
            new_earth = int(earth_grid[ny][nx])
            land_mined.append(new_earth)

    return land_mined

def update_grid(earth_grid, royal_lands):
    # Create a copy of the grid to store updates
    updated_grid = np.copy(earth_grid)

    # Iterate through the grid, checking each cell
    for y in range(len(earth_grid)):
        for x in range(len(earth_grid[y])):
            current_earth = earth_grid[y][x]

            # Find nearby acres and store in a dictionary
            land_type = find_nearby_ground(earth_grid, x, y, royal_lands)
            land_count = Counter(land_type)
            most_common_element, highest_count = land_count.most_common(1)[0]

            # Check if the most common land type is dominant (e.g., more than half of the neighbors)
            if highest_count == len(land_type):  # More than half of the neighbors are the same
                # Update the current cell if the most common element is different
                if current_earth != 0:
                    if current_earth >= (most_common_element + 1):
                        pass
                    else:
                        updated_grid[y][x] += 1

    # Return the updated grid after the full iteration
    return updated_grid


def mine_earth(input_data, royal_lands = False):
    
    # Replace '.' with 0 and '#' with 1 in the input 2D list
    input_grid = np.array([
        [1 if item == '#' else 0 if item == '.' else item for item in row] 
        for row in input_data
    ])

    if royal_lands is True:
        input_grid = input_grid
        # Pad the smaller grid with zeros (or any other value) to make it larger
        # Pad with 1 row/column of zeros on all sides
        input_grid = np.pad(input_grid, pad_width=20, mode='constant', constant_values=0)


    iters = 0
    mined_grid = np.copy(input_grid)  # Create a copy of the input grid
    useful_land = True
    mined_earth = [(iters, int(sum(sum(input_grid))))]  # Store the initial time and sum

    while useful_land:
        mined_grid = update_grid(mined_grid, royal_lands)  # Update the grid with the mining process

        # Calculate the total mined earth
        earth_mined = int(sum(sum(mined_grid)))

        # Check if the total mined earth has stopped changing
        if earth_mined == mined_earth[-1][1]:
            useful_land = False
        else:
            # Append time and total mined earth to the mined_earth list
            iters += 1  # Increment time each iteration
            mined_earth.append((iters, earth_mined))  # Append the current state to mined_earth
            # print(mined_earth)  # Optionally print the progress

    return mined_earth, mined_grid


earth_mined_p1, _ = mine_earth(input_data_p1)
print(f"Part 1: After {earth_mined_p1[-1][0]} iterations, earth mined is {earth_mined_p1[-1][1]}")
# 139- wrong ans, correct length, Correct first digit
# 135- Correct Answer

earth_mined_p2, _ = mine_earth(input_data_p2)
print(f"Part 2: After {earth_mined_p2[-1][0]} iterations, earth mined is {earth_mined_p2[-1][1]}")
# 2646 Correct Ans

earth_mined_p3, _ = mine_earth(input_data_p3, royal_lands = True)
print(f"Part 3: After {earth_mined_p3[-1][0]} iterations, earth mined is {earth_mined_p3[-1][1]}")
# 16142 Wrong Ans, Correct length, Correct first digit
# 11680 Wrong Ans, Correct length, Correct first digit
# 10398 Correct Ans, needed to expand grid
