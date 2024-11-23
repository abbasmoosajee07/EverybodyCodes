
# Everybody Codes - Day 12, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/12
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import inf
from typing import List, Tuple

# List of input file names
input_files = ["Day12_p1_input.txt", "Day12_p2_input.txt", "Day12_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def parse_targets_and_sources(lines: List[str]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]], List[int]]:
    """
    Parses the lines of the input to extract target and source coordinates and hardness levels.
    """
    targets = []
    sources = []
    hardness = []
    max_y = len(lines) - 2

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in "TH":
                targets.append((x, max_y - y))
                hardness.append(2 if char == "H" else 1)
            if char in "ABC":
                sources.append((x, max_y - y))
    return targets, sources, hardness


def calculate_power(source: Tuple[int, int], target: Tuple[int, int]) -> int:
    """
    Calculates the power required to reach a target from a source based on the problem's rules.
    """
    dx = target[0] - source[0]
    dy = target[1] - source[1]

    if dx == dy:
        return dx * (1 + source[1])

    if dx - dy <= dy:
        return dy * (1 + source[1])

    if (dx + dy) % 3 == 0:
        return (dx + dy) // 3 * (1 + source[1])

    return inf


"""
Solves part 1 of the problem by summing up the minimum power required to hit each target.
"""
targets, sources, _ = parse_targets_and_sources(input_data_p1)
total_power_p1 = sum(min(calculate_power(src, tgt) for src in sources) for tgt in targets)
print(f"Quest 1: {total_power_p1}")


"""
Solves part 2 by incorporating hardness into the power calculation.
"""
targets, sources, hardness = parse_targets_and_sources(input_data_p2)
total_power_p2 = sum(h * min(calculate_power(src, tgt) for src in sources) for tgt, h in zip(targets, hardness))
print(f"Quest 1: {total_power_p2}")


def calculate_power_with_meteor(source: Tuple[int, int], meteor: Tuple[int, int]) -> Tuple[int, int]:
    """
    Calculates the power required to reach a meteor considering delays.
    """
    for delay in range(10):
        delayed_target = (meteor[0] - delay, meteor[1] - delay)
        dx = delayed_target[0] - source[0]
        dy = delayed_target[1] - source[1]

        if dx == dy and dx % 2 == 0:
            power = dx // 2
            return (power + source[1], power * (1 + source[1]))

        t = dx - dy
        power = dy - dx // 2
        if dx % 2 == 0 and 0 < t <= power:
            return (power + source[1], power * (1 + source[1]))

        t = dx // 2 - 2 * dy // 3
        power = dy // 3
        if dy % 3 == 0 and dx % 2 == 0 and t > 0:
            return (power + source[1], power * (1 + source[1]))

    return (-1, inf)


"""
Solves part 3 by calculating the maximum power hit for meteors.
"""
sources = [(0, 0), (0, 1), (0, 2)]
meteors = [tuple(map(int, line.split())) for line in input_data_p3]
total_power_p3 = 0

for meteor in meteors:
    powers = [calculate_power_with_meteor(src, meteor) for src in sources]
    total_power_p3 += max(powers, key=lambda x: (x[0], -x[1]))[1]


print(f"Quest 3: {total_power_p3}")
