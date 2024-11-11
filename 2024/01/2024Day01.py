# Everybody Codes - Day 1, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/1
# Solution by: [abbasmoosajee07]
# Brief: [Letter Math and Fights]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D1_file = "Day1_input.txt"
D1_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D1_file)

# Read and sort input data into a grid
with open(D1_file_path) as file:
    input_data = file.read().strip().split('\n')

"""------------------------Functional Approach------------------------"""
def calculate_potions(fighters, split_size):
    potions_req = 0

    # Step 1: Split into groups of `split_size`
    grouped_foes = [fighters[i:i+split_size] for i in range(0, len(fighters), split_size)]

    # Step 2: Initialize counters for single and grouped fighters
    fighter_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'x': 0}
    extra_boost = 0

    # Step 3: Count occurrences based on groups
    for group in grouped_foes:
        fighter_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'x': 0}
        # Handle single fighter case (when 'x' is present in the group)
        fight_group = group.replace("x", "")
        extra_boost = max(len(fight_group) - 1, 0)

        for fighter in fight_group:
            fighter_count[fighter] += 1

        # Step 4: Calculate potions for required by each fighter
        A_potion = (fighter_count['A'] * 0) + ((fighter_count['A'] * extra_boost) if fighter_count['A'] != 0 else 0)
        B_potion = (fighter_count['B'] * 1) + ((fighter_count['B'] * extra_boost) if fighter_count['B'] != 0 else 0)
        C_potion = (fighter_count['C'] * 3) + ((fighter_count['C'] * extra_boost) if fighter_count['C'] != 0 else 0)
        D_potion = (fighter_count['D'] * 5) + ((fighter_count['D'] * extra_boost) if fighter_count['D'] != 0 else 0)
        fight_potion = A_potion + B_potion + C_potion + D_potion

        # print(group, fight_group, len(fight_group), extra_boost)
        # print(fight_potion, A_potion, B_potion, C_potion, D_potion)

        # Step 5: Total potions required
        potions_req += fight_potion

    return potions_req

# Example usage with different split sizes
single_fighters = input_data[0] # 1321
# single_fighters = 'ABBAC'       # 5
potions_p1 = calculate_potions(single_fighters, split_size=1)  # Split into pairs
print(f"Part 1: Potions required for single fights: {potions_p1}")

double_fighter = input_data[1] # 5643
# double_fighter = 'AxBCDDCAxD'  # 28
potions_p2 = calculate_potions(double_fighter, split_size=2)  # Split into pairs
print(f"Part 2: Potions required for paired foes: {potions_p2}")

triple_fighter = input_data[2]
# triple_fighter = 'xBxAAABCDxCC' # 30
potions_p3 = calculate_potions(triple_fighter, split_size=3)  # Split into triplets
print(f"Part 3: Potions required for triplet foes: {potions_p3}")
