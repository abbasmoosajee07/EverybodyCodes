# Everybody Codes - Day 19, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/19
# Solution by: [abbasmoosajee07]
# Brief: [Decoding Messages]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle

# List of input file names
input_files = ["Day19_p1_input.txt", "Day19_p2_input.txt", "Day19_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def adjacent_spaces(point):
    """Returns a list of adjacent points (8 directions)."""
    i, j = point
    return [
        (i-1, j-1), (i-1, j), (i-1, j+1),
        (i, j+1), (i+1, j+1), (i+1, j), (i+1, j-1),
        (i, j-1)
    ]

def flatten(grid):
    """Flattens a 2D grid into a string."""
    return "\n".join("".join(row) for row in grid)

def rotate(grid, point, direction):
    """Rotates the grid values around a given point (left or right)."""
    adj = adjacent_spaces(point)
    vals = [grid[i][j] for (i, j) in adj]
    if direction == "L":
        adj = adj[-1:] + adj[:-1]  # Rotate left
    elif direction == "R":
        adj = adj[1:] + adj[:1]  # Rotate right
    else:
        raise ValueError("Invalid rotation direction")
    
    for (i, j), c in zip(adj, vals):
        grid[i][j] = c

def generate_mappings(grid, pattern, target):
    """Generates the mappings of grid positions for each rotation size."""
    loc_grid = [[(i, j) for j, _ in enumerate(line)] for i, line in enumerate(grid)]
    rotation_points = [(i, j) for i in range(1, len(grid) - 1) for j in range(1, len(grid[i]) - 1)]
    
    # Apply the pattern to the grid using a cycle of rotations
    for d, p in zip(cycle(pattern), rotation_points):
        rotate(loc_grid, p, d)

    # Initialize mappings with the base grid
    mappings = {1: {(i, j): (oi, oj) for i, row in enumerate(loc_grid) for j, (oi, oj) in enumerate(row)}}
    
    # Iteratively double the mapping size until the target is reached
    size = 1
    while size < target:
        size *= 2
        mappings[size] = {k: mappings[size // 2][v] for k, v in mappings[size // 2].items()}

    return mappings

def apply_mappings(grid, mappings, required_mappings):
    """Applies the required mappings to the grid."""
    new_grid = [row.copy() for row in grid]
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            oi, oj = i, j
            for rm in required_mappings:
                oi, oj = mappings[rm][oi, oj]
            new_grid[i][j] = grid[oi][oj]
    return new_grid

def solve_puzzle(input_data, iters = 1):
    """Solves the puzzle for a specific part."""

    pattern = input_data[0]
    grid = [list(line) for line in input_data[1].split('\n')]

    # Generate the mappings for the grid and pattern
    mappings = generate_mappings(grid, pattern, iters)
    
    # Find the required mappings that fit the target
    required_mappings = [k for k in mappings if k & iters]

    # Apply the required mappings to transform the grid
    transformed_grid = apply_mappings(grid, mappings, required_mappings)
    
    # Flatten the transformed grid and extract the solution part
    solution = flatten(transformed_grid)
    solution = solution[solution.index(">")+1:solution.index("<")]
    return solution

ans_p1 = solve_puzzle(input_data_p1, iters = 1)
print(f"Quest 1: {ans_p1}")

ans_p2 = solve_puzzle(input_data_p2, iters = 100)
print(f"Quest 2: {ans_p2}")

ans_p3 = solve_puzzle(input_data_p3, iters = 1048576000)
print(f"Quest 3: {ans_p3}")