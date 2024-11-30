
# Everybody Codes - Day 16, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/16
# Solution by: [abbasmoosajee07]
# Brief: [Slot Machine]

#!/usr/bin/env python3

import os, sys, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
sys.setrecursionlimit(10**6)

# List of input file names
input_files = ["Day16_p1_input.txt", "Day16_p2_input.txt", "Day16_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def parse_input(input_data):
    """
    Parses the input data into a list of numbers and a list of face rows.
    """
    numbers, face_grid = input_data
    numbers = [int(x) for x in numbers.split(',')]
    face_rows = face_grid.split('\n')
    return numbers, face_rows

def organize_faces(input_data):
    """
    Organizes the face data into columns based on the grid format.
    """
    numbers, face_rows = parse_input(input_data)
    num_columns = (len(face_rows[0]) + 1) // 4
    face_columns = [[] for _ in range(num_columns)]
    
    for row in face_rows:
        for col_index in range(num_columns):
            # Extract a 3-character segment for each column
            face = row[col_index * 4: col_index * 4 + 3]
            if face.strip():
                face_columns[col_index].append(face)
    
    return numbers, face_columns

def compute_result(numbers, face_columns):
    """
    Computes the result by selecting a face for each column based on the numbers list.
    """
    result = []
    for col_index, number in enumerate(numbers):
        selected_index = (number * 100) % len(face_columns[col_index])
        result.append(face_columns[col_index][selected_index])
    return ' '.join(result)

numbers_p1, face_columns_p1 = organize_faces(input_data_p1)
ans_p1 = compute_result(numbers_p1, face_columns_p1)
print("Quest 1:", ans_p1)

def calculate_final_score(xs, face_columns, total_iterations):
    """
    Simulates the process and computes the final score after `total_iterations` steps.
    """
    num_columns = len(xs)
    state = [0] * num_columns
    t = 0
    score_total = 0
    state_history = {}

    while t < total_iterations:
        t += 1
        # Compute new state
        new_state = [(state[i] + xs[i]) % len(face_columns[i]) for i in range(num_columns)]
        state = new_state

        # Check for cycles
        key = tuple(state)
        if key in state_history:
            prev_t, prev_score = state_history[key]
            cycle_length = t - prev_t
            cycle_score = score_total - prev_score
            cycles_to_skip = (total_iterations - t) // cycle_length

            # Skip cycles
            t += cycles_to_skip * cycle_length
            score_total += cycles_to_skip * cycle_score
        else:
            state_history[key] = (t, score_total)

        # Compute score for the current state
        score_counter = Counter()
        for col_index in range(num_columns):
            face = face_columns[col_index][state[col_index]]
            score_counter[face[0]] += 1
            score_counter[face[2]] += 1

        # Calculate the score for this step
        step_score = sum(max(0, count - 2) for count in score_counter.values())
        score_total += step_score

        # Debug output (optional)
        # print(f'{t=} {score_total=}')

    return score_total

# Organize faces into columns
numbers_p2, face_columns_p2 = organize_faces(input_data_p2)

# Calculate the final score
ans_p2 = calculate_final_score(numbers_p2, face_columns_p2,
                                total_iterations = 202420242024)
print(f'Quest 2: {ans_p2}')

def calculate_score(face_columns, positions):
    """
    Computes the score for a given set of positions in the face columns.
    """
    char_count = Counter()
    for column_index, position in enumerate(positions):
        face = face_columns[column_index][position]
        char_count[face[0]] += 1  # First character in the face
        char_count[face[2]] += 1  # Third character in the face
    return sum(max(0, count - 2) for count in char_count.values())

def dynamic_programming(steps_remaining, positions, find_min, movement_rates, face_columns, memo):
    """
    Dynamic programming function to compute the maximum or minimum score
    over a given number of steps.
    """
    if steps_remaining == 0:
        return 0

    state_key = (steps_remaining, tuple(positions), find_min)
    if state_key in memo:
        return memo[state_key]

    best_score = None
    for position_change in [-1, 0, 1]:
        # Calculate new positions based on movement rates and the position change
        new_positions = [
            (positions[column_index] + position_change + movement_rates[column_index] + len(face_columns[column_index]))
            % len(face_columns[column_index])
            for column_index in range(len(movement_rates))
        ]
        # Calculate the score for the new state
        current_score = calculate_score(face_columns, new_positions)
        total_score = current_score + dynamic_programming(
            steps_remaining - 1, new_positions, find_min, movement_rates, face_columns, memo
        )

        # Update the best score based on whether we are minimizing or maximizing
        if best_score is None:
            best_score = total_score
        elif find_min:
            best_score = min(best_score, total_score)
        else:
            best_score = max(best_score, total_score)

    memo[state_key] = best_score
    return best_score

# Organize faces into columns
numbers_p3, face_columns_p3 = organize_faces(input_data_p3)

# Initialize starting positions and memoization dictionary
starting_positions = [0] * len(numbers_p3)
memo = {}

# Compute minimum and maximum scores over 256 steps
min_score = dynamic_programming(256, starting_positions, find_min=True, movement_rates=numbers_p3,
                                    face_columns=face_columns_p3, memo=memo)
max_score = dynamic_programming(256, starting_positions, find_min=False, movement_rates=numbers_p3,
                                    face_columns=face_columns_p3, memo=memo)

print("Quest 3:", max_score, min_score)


