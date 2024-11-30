
# Everybody Codes - Day 17, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/17
# Solution by: [abbasmoosajee07]
# Brief: [Stars and Constellations]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# List of input file names
input_files = ["Day17_p1_input.txt", "Day17_p2_input.txt", "Day17_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def find_positions(grid, char='*'):
    """
    Finds all positions of the specified character in the grid.
    """
    return [(r, c) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell == char]

def find_root(union_find, position):
    """
    Finds the root of a position in the Union-Find structure with path compression.
    """
    if union_find[position] != position:
        union_find[position] = find_root(union_find, union_find[position])
    return union_find[position]

def union_positions(union_find, pos1, pos2):
    """
    Unites two sets in the Union-Find structure.
    """
    union_find[find_root(union_find, pos1)] = find_root(union_find, pos2)

def calculate_mst_cost(positions):
    """
    Computes the Minimum Spanning Tree (MST) cost using Kruskal's algorithm.
    """
    union_find = {p: p for p in positions}
    edges = [(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]), p1, p2) for i, p1 in enumerate(positions) for p2 in positions[i + 1:]]
    edges.sort()

    mst_cost = 0
    for cost, p1, p2 in edges:
        if find_root(union_find, p1) != find_root(union_find, p2):
            mst_cost += cost
            union_positions(union_find, p1, p2)

    return mst_cost

positions_p1 = find_positions(input_data_p1)
ans_p1 = calculate_mst_cost(positions_p1) + len(positions_p1)
print(f"Quest 1: {ans_p1}")

positions_p2 = find_positions(input_data_p2)
ans_p2 = calculate_mst_cost(positions_p2) + len(positions_p2)
print(f"Quest 2: {ans_p2}")

positions_p3 = find_positions(input_data_p3)

E = []
UF = {p: p for p in positions_p3}
for p1 in positions_p3:
    for p2 in positions_p3:
        if p1 != p2:
            distance = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
            if distance < 6:
                E.append((distance, p1, p2))

def find(x):
    if UF[x] == x:
        return x
    UF[x] = find(UF[x])
    return UF[x]

def mix(p1,p2):
    UF[find(p1)] = find(p2)

E = sorted(E)
ans = 0
for (cost, p1, p2) in E:
    if cost > 6:
        continue
    if find(p1) != find(p2):
        ans += cost
        mix(p1,p2)
ans += len(positions_p3)

def getCost(group):
    P = group
    E = []
    UF = {p: p for p in P}
    for p1 in P:
        for p2 in P:
            if p1 != p2:
                distance = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
                if distance < 6:
                    E.append((distance, p1, p2))
    def find(x):
        if UF[x] == x:
            return x
        UF[x] = find(UF[x])
        return UF[x]
    def mix(p1,p2):
        UF[find(p1)] = find(p2)

    E = sorted(E)
    ans = 0
    for (cost, p1, p2) in E:
        if find(p1) != find(p2):
            ans += cost
            mix(p1,p2)
    ans += len(P)
    return ans

groups = defaultdict(list)
for p in positions_p3:
    group = find(p)
    groups[group].append(p)
sizes = sorted(getCost(group) for group in groups.values())
ans_p3 = sizes[-1]*sizes[-2]*sizes[-3]
print(f"Quest 3: {ans_p3}")


