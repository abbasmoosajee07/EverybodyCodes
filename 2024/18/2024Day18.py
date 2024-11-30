
# Everybody Codes - Day 18, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/18
# Solution by: [abbasmoosajee07]
# Brief: [Water Flow and Gardens]

#!/usr/bin/env python3

import os, re, copy, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
sys.setrecursionlimit(10**6)

# List of input file names
input_files = ["Day18_p1_input.txt", "Day18_p2_input.txt", "Day18_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

# Helper function to get all open cells and palms in the grid
def identify_cells(grid):
    """Identifies all open cells ('.') and palms ('P') in the grid."""
    open_cells = []
    palms = set()
    rows = len(grid)
    cols = len(grid[0])
    
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '.':
                open_cells.append((row, col))
            elif grid[row][col] == 'P':
                palms.add((row, col))
                
    return open_cells, palms

# Function to find the starting position of the search (first '.' in the first column)
def find_start_position(grid):
    """Finds the starting position of the search (first '.' in the first column)."""
    for row_idx, row in enumerate(grid):
        if row[0] == '.':
            return row_idx, 0
    return None, None  # In case no start position is found

# Function to count the number of palms ('P') in the grid
def count_palms(grid):
    """Counts the number of palms ('P') in the grid."""
    return sum(row.count('P') for row in grid)

# BFS function to find the shortest distance to collect all palms
def bfs_to_find_all_palms(grid, start_row, start_col, num_palms):
    """Performs a BFS to find all palms in the grid."""
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Directions: up, down, left, right
    
    queue = deque([(0, start_row, start_col)])  # Queue for BFS: (distance, row, col)
    seen = set()  # Set to track visited positions
    
    while queue:
        distance, row, col = queue.popleft()
        
        # Skip if already visited
        if (row, col) in seen:
            continue
        seen.add((row, col))
        
        # Check for 'P' (palm) at the current position
        if grid[row][col] == 'P':
            num_palms -= 1
            if num_palms == 0:  # If all palms are found, return the current distance
                return distance
        
        # Explore all four directions
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] != '#':
                queue.append((distance + 1, new_row, new_col))
    
    return -1  # Return -1 if no solution is found

# Function to calculate distances from a given start point (sr, sc) using BFS
def get_distances(grid, start_row, start_col):
    """Calculates distances from a start point to all reachable cells in the grid."""
    distances = {}  # Dictionary to store distances from (start_row, start_col)
    queue = deque([(0, start_row, start_col)])  # Queue for BFS: (distance, row, col)
    seen = set()  # Set to track visited cells
    
    while queue:
        dist, row, col = queue.popleft()
        
        # Skip if this cell has already been visited
        if (row, col) in seen:
            continue
        seen.add((row, col))
        
        # If the cell is an open cell ('.'), record the distance
        if grid[row][col] == '.':
            distances[(row, col)] = dist
        
        # Explore neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + dr
            new_col = col + dc
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] != '#':
                queue.append((dist + 1, new_row, new_col))
    
    return distances

# Function to perform BFS from the border cells to collect all palms
def bfs_from_border(grid):
    """Performs BFS from open cells in the border to find the shortest path to all palms."""
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    queue = deque([(0, row, col) for row in range(rows) for col in [0, cols - 1] if grid[row][col] == '.'])
    num_palms = count_palms(grid)
    visited = set()

    while queue:
        distance, row, col = queue.popleft()
        
        if (row, col) in visited:
            continue
        visited.add((row, col))
        
        if grid[row][col] == 'P':
            num_palms -= 1
            if num_palms == 0:
                return distance
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] != '#':
                queue.append((distance + 1, new_row, new_col))
    
    return -1

# Function to calculate the minimal distance to collect all palms by considering all open cells
def find_minimum_distance_to_palms(grid):
    """Finds the minimal total distance to collect all palms in the grid."""
    open_cells, palms = identify_cells(grid)
    
    # Calculate distances from each palm tree to all open cells
    palm_distances = [get_distances(grid, palm[0], palm[1]) for palm in palms]
    
    # Initialize best score as infinity
    best_score = float('inf')
    
    # For each open cell, calculate the total distance to all palms
    for open_cell in open_cells:
        total_distance = sum(distances.get(open_cell, float('inf')) for distances in palm_distances)
        best_score = min(best_score, total_distance)
    
    return best_score

# Quest 1: Find the shortest distance to collect all palms starting from the first column
def quest_1(grid):
    """Solves Quest 1: Find the shortest distance to collect all palms."""
    start_row, start_col = find_start_position(grid)
    num_palms = count_palms(grid)
    return bfs_to_find_all_palms(grid, start_row, start_col, num_palms)

# Quest 2: Perform BFS from open cells in the first and last columns to find the shortest distance
def quest_2(grid):
    """Solves Quest 2: Find the shortest distance to all palms from the border."""
    return bfs_from_border(grid)

# Quest 3: Find the best cell that minimizes the total distance to all palms
def quest_3(grid):
    """Solves Quest 3: Find the minimal total distance to all palms."""
    return find_minimum_distance_to_palms(grid)

# Quest 1
grid = input_data_p1
result_quest1 = quest_1(grid)
print("Quest 1:", result_quest1)

# Quest 2
grid = input_data_p2
result_quest2 = quest_2(grid)
print("Quest 2:", result_quest2)

# Quest 3
grid = input_data_p3
result_quest3 = quest_3(grid)
print("Quest 3:", result_quest3)

