
# Everybody Codes - Day 14, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/14
# Solution by: [abbasmoosajee07]
# Brief: [Build Trees]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
# List of input file names
input_files = ["Day14_p1_input.txt", "Day14_p2_input.txt", "Day14_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def parse_instructions(instructions):
    instruction_list = []
    for line in instructions:
        parsed_line = []
        line = list(line.split(','))
        for command in line:
            direction = command[0]
            magnitude = command[1:]
            parsed_line.append([direction, int(magnitude)])
        instruction_list.append(parsed_line)
    return instruction_list

def build_tree(command_list, start=(0, 0, 0)):
    """
    Builds a tree-like path based on command instructions.

    Args:
        command_list (list of tuples): List of commands in (action, magnitude) format.
        start (tuple): Starting position and direction as (x, y, dir).

    Returns:
        tuple:
            - tree_path (set): Set of all visited positions in the path.
            - max_y (int): Maximum y-coordinate reached during the path.
    """
    # Initialize starting position and direction
    x, y, z = start
    tree_path = set()
    max_y = 0

    # Movement dictionary: Maps actions to changes in (x, y, dir)
    movement = {
        'U': (0, 1, 0),   # Move up
        'D': (0, -1, 0),  # Move down
        'L': (-1, 0, 0),  # Move left
        'R': (1, 0, 0),   # Move right
        'F': (0, 0, 1),   # Move forward in current direction
        'B': (0, 0, -1)   # Move backward in current direction
    }

    # Process each command in the command list
    for action, magnitude in command_list:
        dx, dy, dz = movement[action]  # Get movement deltas
        for _ in range(magnitude):
            x += dx
            y += dy
            z += dz  # Update direction for F/B movements
            tree_path.add((x, y, z))  # Record position and direction
            max_y = max(max_y, y)  # Track maximum y-coordinate

    # Return the tree path and maximum y-coordinate
    return tree_path, max_y, (x, y, z)

command_p1 = parse_instructions(input_data_p1)
_, ans_p1, _ = build_tree(command_p1[0])
print("Quest 1:", ans_p1)

def find_unique_segments(command_group):
    all_segments = set()
    for command_line in command_group:
        visited, _, _ = build_tree(command_line)
        all_segments.update(visited)
    return len(all_segments)

command_p2 = parse_instructions(input_data_p2)
ans_p2 = find_unique_segments(command_p2)
print("Quest 2:", ans_p2)
def calc_murkiness(command_group):
    """
    Calculates the murkiness score based on visited positions and final leaf nodes.

    Args:
        command_group (list): A list of command instructions for the path.

    Returns:
        int: The best murkiness score.
    """
    final_positions = set()
    all_visited_positions = set()
    
    # Process each command line
    for command_line in command_group:
        visited_positions, _, final_position = build_tree(command_line)
        all_visited_positions.update(visited_positions)  # Add all visited positions
        final_positions.add(final_position)  # Add the final leaf positions

    best_murkiness_score = float('inf')  # Initialize the best score to a large value

    # Start BFS from the origin (0, 0, 0)
    for start_x, start_y, start_z in all_visited_positions:
        if start_x == 0 and start_z == 0:  # Only start from (0, 0, 0)
            murkiness_score = 0
            queue = deque([(0, start_x, start_y, start_z)])  # Queue for BFS with distance, x, y, z
            visited_set = set()  # Set to keep track of visited positions

            while queue:
                distance, x, y, z = queue.popleft()

                # Skip if we've already visited this position
                if (x, y, z) in visited_set:
                    continue

                visited_set.add((x, y, z))

                # If it's a final position, add the distance to the score
                if (x, y, z) in final_positions:
                    murkiness_score += distance

                # Explore neighboring positions
                for dx, dy, dz in {'U': (0, 1, 0), 'D': (0, -1, 0), 'R': (1, 0, 0), 
                                    'L': (-1, 0, 0), 'F': (0, 0, 1), 'B': (0, 0, -1)}.values():
                    next_x, next_y, next_z = x + dx, y + dy, z + dz

                    # Only add to the queue if the position has been visited
                    if (next_x, next_y, next_z) in all_visited_positions:
                        queue.append((distance + 1, next_x, next_y, next_z))

            # Track the best score
            best_murkiness_score = min(best_murkiness_score, murkiness_score)

    return best_murkiness_score

command_p3 = parse_instructions(input_data_p3)
ans_p3 = calc_murkiness(command_p3)
print("Quest 3:", ans_p3)