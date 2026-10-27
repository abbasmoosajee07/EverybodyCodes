"""Everybody Codes - Quest 1, Year 2026
Solution Started: October 27, 2026
Puzzle Link: https://everybody.codes/event/2026/quests/1
Solution by: Abbas Moosajee
Brief: [The Coneservation]"""

#!/usr/bin/env python3
from pathlib import Path
from math import sqrt, ceil
input_files = ["Day01_input_p1.txt", "Day01_input_p2.txt", "Day01_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def fill_pine_sqr(cones):
    cone_sqrt = sqrt(cones)
    cone_rdup = ceil(cone_sqrt)
    return cone_rdup ** 2 - cones


def fill_pine_perimeter(cones):
    target = 8 # smallest box size(3x3)
    while target < cones:
        target += 4
    return target - cones

def fill_pine_box(cones):
    size = ceil(sqrt(cones))

    while True:
        size += size % 2 == 0
        target = size**2 - 1

        if cones <= target:
            return target - cones

        size += 1

cones_p1 = [fill_pine_sqr(int(cone)) for cone in input_data_p1[0].split(",")]
cones_p2 = [fill_pine_perimeter(int(cone)) for cone in input_data_p2[0].split(",")]
cones_p3 = [fill_pine_box(int(cone)) for cone in input_data_p3[0].split(",")]

print("EC 2026, Quest 01")
print("Part 1:", sum(cones_p1))
print("Part 2:", sum(cones_p2))
print("Part 3:", sum(cones_p3))
