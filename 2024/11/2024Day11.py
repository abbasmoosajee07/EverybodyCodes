# Everybody Codes - Day 11, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/11
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# List of input file names
input_files = ["Day11_p1_input.txt", "Day11_p2_input.txt", "Day11_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def parse_to_dict(strings):
    result = {}
    for string in strings:
        key, values = string.split(":", 1)
        result[key] = values.split(",")
    return result

# Example input

def termite_growth(input_data, total_gen, start = 'A'):
    growth_possibilities = parse_to_dict(input_data)
    termite_pop = [start]

    for gen in range(1, total_gen + 1):  # Iterate over generations
        next_gen = []  # Holds the next generation
        for termite in termite_pop:  # Process each termite in the current population
            offspring = growth_possibilities.get(termite, [])  # Get offspring from parsed_dict
            next_gen.extend(offspring)  # Add offspring to next generation
        termite_pop = next_gen  # Update termite_pop for the next generation
    return len(termite_pop)

ans_p1 = termite_growth(input_data_p1, 4, 'A')
print(f"Quest 1: {ans_p1}")

ans_p2 = termite_growth(input_data_p2, 10, 'Z')
print(f"Quest 2: {ans_p2}")

termite_pop_count = {}
parsed_dict = parse_to_dict(input_data_p3)  # Assuming input_data_p3 is your input
for termite in parsed_dict.keys():
    current_population = {termite: 1}
    for _ in range(20):
        next_population = defaultdict(int)
        for k, v in current_population.items():
            for offspring in parsed_dict[k]:
                next_population[offspring] += v
        current_population = next_population
    termite_pop_count[termite] = sum(current_population.values())

max_population = max(termite_pop_count.values())
min_population = min(termite_pop_count.values())
ans_p3 = max_population - min_population
print(f"Quest 3: {ans_p3}")
