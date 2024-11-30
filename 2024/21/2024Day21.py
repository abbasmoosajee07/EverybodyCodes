
# Everybody Codes - Day 21, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/21
# Solution by: [abbasmoosajee07]
# Brief: [Thank You Message]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# List of input file names
input_files = ["Day21_p1_input.txt"]

# Read and split the input data into individual lists
input_data = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n\n')
    for file in input_files
][0]

# Constants
DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
SHOW_GRID = True

# Helper Functions
def ff(row, col, num_cols):
    """Convert (row, col) to a 1D index."""
    return row * num_cols + col


def fr(index, num_cols):
    """Convert 1D index to (row, col)."""
    return divmod(index, num_cols)


def rotate(direction, grid, center_row, center_col):
    """
    Rotate the 8 surrounding cells of a given center cell in a grid.

    Parameters:
    - direction: 'L' for left, 'R' for right
    - grid: 2D list representing the grid
    - center_row, center_col: Center cell coordinates
    """
    assert direction in "LR"
    offset = 1 if direction == "L" else -1
    memory = [grid[center_row + dx][center_col + dy] for dx, dy in DIRECTIONS]
    for i in range(8):
        dx, dy = DIRECTIONS[i]
        new_value = memory[(i + offset) % 8]
        grid[center_row + dx][center_col + dy] = new_value


def calc_mapping(grid, key):
    """
    Calculate the mapping of the grid after applying rotations based on the key.

    Parameters:
    - grid: 2D list representing the grid
    - key: String representing the rotation sequence

    Returns:
    - A 2D list representing the mapping of each cell
    """
    rows, cols = len(grid), len(grid[0])
    index_grid = [[ff(r, c, cols) for c in range(cols)] for r in range(rows)]

    key_index = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            rotate(key[key_index], index_grid, r, c)
            key_index = (key_index + 1) % len(key)

    mapping = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            rr, cc = fr(index_grid[r][c], cols)
            mapping[rr][cc] = ff(r, c, cols)

    return mapping


def find_cycle(start_row, start_col, mapping):
    """
    Find a cycle starting from a given cell in the mapping.

    Parameters:
    - start_row, start_col: Starting cell coordinates
    - mapping: 2D list representing the mapping of the grid

    Returns:
    - List of 1D indices representing the cycle
    """
    cols = len(mapping[0])
    cycle = [ff(start_row, start_col, cols)]
    r, c = start_row, start_col

    while True:
        r, c = fr(mapping[r][c], cols)
        if (r, c) == (start_row, start_col):
            break
        cycle.append(ff(r, c, cols))

    return cycle


def calc_cycles(grid, key):
    """
    Calculate all cycles in the grid based on the key.

    Parameters:
    - grid: 2D list representing the grid
    - key: String representing the rotation sequence

    Returns:
    - List of cycles, cycle IDs, and cycle positions
    """
    rows, cols = len(grid), len(grid[0])
    mapping = calc_mapping(grid, key)
    cycles, cycle_id, cycle_pos = [], [[-1] * cols for _ in range(rows)], [[-1] * cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            if cycle_id[r][c] == -1:
                cycle = find_cycle(r, c, mapping)
                cycle_index = len(cycles)
                cycles.append(cycle)

                for pos, index in enumerate(cycle):
                    rr, cc = fr(index, cols)
                    cycle_id[rr][cc] = cycle_index
                    cycle_pos[rr][cc] = pos

    return cycles, cycle_id, cycle_pos


def simulate(grid, key, count):
    """
    Simulate the grid transformations and extract the string between '>' and '<'.

    Parameters:
    - grid: 2D list representing the initial grid
    - key: String representing the rotation sequence
    - count: Number of transformations to simulate

    Returns:
    - Extracted string between '>' and '<'
    """
    rows, cols = len(grid), len(grid[0])
    result = [["."] * cols for _ in range(rows)]
    cycles, cycle_id, cycle_pos = calc_cycles(grid, key)

    for r in range(rows):
        for c in range(cols):
            cycle_index = cycle_id[r][c]
            position = cycle_pos[r][c]
            new_index = (position + count) % len(cycles[cycle_index])
            rr, cc = fr(cycles[cycle_index][new_index], cols)
            result[rr][cc] = grid[r][c]

    if SHOW_GRID:
        print("\nGrid After Simulation:")
        for row in result:
            print("".join(row))

    for row in result:
        if ">" in row and "<" in row:
            s = "".join(row)
            return s[s.index(">") + 1: s.index("<")]


num, key = input_data[0].split(":")
grid = [list(row) for row in input_data[1].split("\n")]

# Solve Part 1
ans1 = simulate(grid, key, int(num))

