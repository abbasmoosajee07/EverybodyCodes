
# Everybody Codes - Day 9, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/9
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, sys, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.setrecursionlimit(10**9)  # Increase the recursion depth

# List of input file names
input_files = ["Day09_p1_input.txt", "Day09_p2_input.txt", "Day09_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)


def find_combinations(num, stamps, DP):
    if num < 0:
        return 10**9  # Return a large number to indicate invalid cases
    if num == 0:
        return 0  # Base case: no stamps needed for a total of 0
    if num in DP:
        return DP[num]  # Return cached result if available

    ans = 10**9  # Initialize with a large number
    for stamp in stamps:
        ans = min(ans, 1 + find_combinations(num - stamp, stamps, DP))

    DP[num] = ans  # Cache the result
    return ans

def find_total_combos(num_str, stamps):
    num_list = [int(num) for num in num_str]
    total_count = 0
    for num in num_list:
        DP = {}
        count = find_combinations(num, stamps, DP)
        # print(count)
        total_count += count
    return total_count

# Run Code for Day 9, 2024
stamps_p1 = [1, 3, 5, 10]
ans_p1 = find_total_combos(input_data_p1, stamps_p1)
print(f"Part 1: {ans_p1}")

stamps_p2 = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30]
ans_p2 = find_total_combos(input_data_p2, stamps_p2)
print(f"Part 2: {ans_p2}")

def beetles_for_kings_order(input_data, stamps):
    """
    Calculate the total number of beetles required for the King's order.

    :param input_data: List of integers representing the King's orders.
    :param stamps: List of available stamps.
    :return: Total number of beetles required.
    """

    # Step 1: Precompute the minimum number of stamps needed for each value up to 10^7
    MAX_VALUE = 10**7
    INF = 10**9  # Represent a very large number for invalid cases

    # Create a list to store minimum stamps for each value
    min_stamps = [INF] * (MAX_VALUE + 1)
    min_stamps[0] = 0  # Base case: 0 stamps needed for value 0

    for x in range(1, MAX_VALUE + 1):
        for stamp in stamps:
            if x - stamp >= 0:
                min_stamps[x] = min(min_stamps[x], 1 + min_stamps[x - stamp])

    # Step 2: Define helper functions for calculations

    def f(n):
        """Return the precomputed minimum stamps for value `n`."""
        return min_stamps[n]

    def g(n):
        """
        For a given `n`, calculate the minimum stamps required
        considering possible splits into two close parts.
        """
        mid = n // 2
        best_score = INF

        # Check values around the midpoint to ensure balanced parts
        for x in range(max(mid - 200, 0), min(mid + 200, n + 1)):
            y = n - x
            if abs(x - y) <= 100:  # Ensure x and y are close
                score = f(x) + f(y)
                if score < best_score:
                    best_score = score
        return best_score

    # Step 3: Process each order in input_data

    total_beetles = 0
    for line in input_data:
        order_value = int(line.strip())
        total_beetles += g(order_value)

    return total_beetles
stamps_p3 = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101]
ans_p3 = beetles_for_kings_order(input_data_p3, stamps_p3)
print(f"Part 3: {ans_p3}")

# 149562 Wrong ans, Correct len and first digit