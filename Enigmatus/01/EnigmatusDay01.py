"""# Everybody Codes - Day 1, Year Enigmatus
# Solved in Jun, 2025
# Puzzle Link: https://everybody.codes/story/1/quests/1
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
start_time = time.time()

# List of input file names
input_files = ["Day01_p1_input.txt", "Day01_p2_input.txt", "Day01_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]
# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def eni_basic(input):
    """Compute N^1, N^2, ..., N^EXP mod MOD and reverse the list for result."""
    N, EXP, MOD = input
    score = 1
    rem_list = []
    for _ in range(EXP):
        score = score * N % MOD
        rem_list.append(str(score))
    return int(''.join(rem_list[::-1]))


def eni_trailing(input):
    """Compute the last 5 values of the sequence N^k mod MOD, considering cycles."""
    N, EXP, MOD = input
    if MOD == 1:
        return 0

    remainder_map = {}
    sequence = []
    score = 1

    for k in range(EXP):
        val = (score * N) % MOD
        if val in remainder_map:
            # Cycle detected
            start = remainder_map[val]
            cycle = sequence[start:]
            cycle_len = len(cycle)
            needed = max(0, EXP - 5)
            rem_list = []
            for i in range(needed, EXP):
                idx = i if i < start else start + (i - start) % cycle_len
                rem_list.append(str(sequence[idx] if idx < len(sequence) else cycle[(i - start) % cycle_len]))
            return int(''.join(rem_list[::-1][-5:]))

        remainder_map[val] = k
        sequence.append(val)
        score = val

    return int(''.join([str(x) for x in sequence[-5:]][::-1]))


def eni_sum(input):
    """Compute the sum of N^1, ..., N^EXP mod MOD, optimized using cycle detection."""
    N, EXP, MOD = input
    if MOD == 1:
        return 0

    remainder_map = {}
    sequence = []
    score = 1
    total_sum = 0

    for k in range(EXP):
        val = (score * N) % MOD
        if val in remainder_map:
            # Cycle detected
            start = remainder_map[val]
            cycle = sequence[start:]
            cycle_sum = sum(cycle)
            remaining = EXP - k
            full_cycles = remaining // len(cycle)
            rest = remaining % len(cycle)
            total_sum += full_cycles * cycle_sum + sum(cycle[:rest])
            return total_sum

        remainder_map[val] = k
        sequence.append(val)
        total_sum += val
        score = val

    return total_sum

def use_equation(params, eni_func):
    A, X = params['A'], params['X']
    B, Y = params['B'], params['Y']
    C, Z = params['C'], params['Z']
    M = params['M']
    return eni_func((A, X, M)) + eni_func((B, Y, M)) + eni_func((C, Z, M))


def evaluate_data(input_data, eni_func):
    values = []
    for line in input_data:
        tokens = {k: int(v) for k, v in (pair.split('=') for pair in line.split())}
        values.append(use_equation(tokens, eni_func))
    return values


values_q1 = evaluate_data(input_data_p1, eni_basic)
values_q2 = evaluate_data(input_data_p2, eni_trailing)
values_q3 = evaluate_data(input_data_p3, eni_sum)

print("Quest 1:", max(values_q1))
print("Quest 2:", max(values_q2))
print("Quest 3:", max(values_q3))
# print(f"Execution Time = {time.time() - start_time:.5f}s")