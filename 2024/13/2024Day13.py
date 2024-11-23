
# Everybody Codes - Day 13, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/13
# Solution by: [abbasmoosajee07]
# Brief: [Grid traversal problem w/ Djikstra]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# List of input file names
input_files = ["Day13_p1_input.txt", "Day13_p2_input.txt", "Day13_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]
# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def get_adjacent_positions(position):
    row, col = position
    return [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]

def filter_valid_positions(position, grid):

    return [adj_pos for adj_pos in get_adjacent_positions(position) if adj_pos in grid]

def calculate_min_transition_cost(value_a, value_b):

    return min(abs(value_a - value_b), abs(10 - value_a + value_b), abs(10 - value_b + value_a))

def traverse_grid(input_data):
    """
    Solves a single part of the problem and prints the result.
    
    Args:
        part (int): The part number (1, 2, or 3).
    """
    # Load the grid data
    lines = input_data
    grid = {
        (row, col): char for row, line in enumerate(lines)
        for col, char in enumerate(line) if char not in "# "
    }

    # Identify start and end positions
    start_positions = [pos for pos, value in grid.items() if value == "S"]
    end_position, = (pos for pos, value in grid.items() if value == "E")

    # Convert grid values to integers, defaulting to 0 for non-numeric values
    grid = {pos: int(value) if value.isnumeric() else 0 for pos, value in grid.items()}

    # Initialize cost dictionary
    min_costs = {position: float('inf') for position in grid}
    min_costs[end_position] = 0  # Cost to reach the endpoint is zero

    # Initialize set of positions to update
    positions_to_update = set(filter_valid_positions(end_position, grid))

    # Propagate costs until no updates remain
    while positions_to_update:
        new_positions_to_update = set()
        for current_position in positions_to_update:
            # Calculate the new cost for the current position
            adjacent_positions = filter_valid_positions(current_position, grid)
            new_cost = min(
                [min_costs[adj_pos] + calculate_min_transition_cost(grid[current_position], grid[adj_pos]) + 1
                 for adj_pos in adjacent_positions] or [float('inf')]
            )

            # If the cost improves, update and mark adjacent positions for reevaluation
            if new_cost < min_costs[current_position]:
                min_costs[current_position] = new_cost
                new_positions_to_update.update(adjacent_positions)
        
        positions_to_update = new_positions_to_update  # Update positions to process

    # Compute the minimum cost to any start position
    result = min(min_costs[start_pos] for start_pos in start_positions)
    return result
# Solve for all three parts
ans_p1 = traverse_grid(input_data_p1)
print("Quest 1:", ans_p1)

ans_p2 = traverse_grid(input_data_p2)
print("Quest 2:", ans_p2)

ans_p3 = traverse_grid(input_data_p3)
print("Quest 3:", ans_p3)
