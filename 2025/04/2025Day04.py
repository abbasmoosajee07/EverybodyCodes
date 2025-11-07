"""Everybody Codes - Quest 4, Year 2025
Solution Started: November 7, 2025
Puzzle Link: https://everybody.codes/event/20252/quests/4
Solution by: Abbas Moosajee
Brief: [Teeth of the Wind]"""

#!/usr/bin/env python3
from pathlib import Path
from math import prod, ceil, floor

# List of input file names
input_files = ["Day04_input_p1.txt", "Day04_input_p2.txt", "Day04_input_p3.txt"]

def parse_input(input_str: str) -> list[int]:
    return [int(x) for x in input_str]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def build_gears(gear_list):
    return [[int(i), int(i)] for i in gear_list]

def calc_gear_ratio(gears):
    return prod(a[1] / b[0] for a, b in zip(gears, gears[1:]))

def solve_quest(input_gears, part):
    if part == 1:
        parsed_gears = build_gears(input_gears)
        gear_ratio = calc_gear_ratio(parsed_gears)
        final_gear_turns = int(gear_ratio * 2025)
    elif part == 2:
        parsed_gears = build_gears(input_gears)
        gear_ratio = calc_gear_ratio(parsed_gears)
        final_gear_turns = ceil(10000000000000 / gear_ratio)
    elif part == 3:
        parsed_gears = [tuple(map(int, line.split("|"))) for line in input_gears]
        speed = 1
        (start_gear,), *between, (end_gear,) = parsed_gears
        for gear in between:
            speed *= gear[1] / gear[0]

        final_gear_turns = floor(100 * speed * start_gear / end_gear)
    return final_gear_turns


print("Quest 04, P1:", solve_quest(input_data_p1, 1))
print("Quest 04, P2:", solve_quest(input_data_p2, 2))
print("Quest 04, P3:", solve_quest(input_data_p3, 3))
