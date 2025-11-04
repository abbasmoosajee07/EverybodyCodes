"""Everybody Codes - Quest 1, Year 2025
Solution Started: November 3, 2025
Puzzle Link: https://everybody.codes/event/20252/quests/1
Solution by: Abbas Moosajee
Brief: [Whispers in the Shell]"""

#!/usr/bin/env python3
from pathlib import Path

# List of input file names
input_files = ["Day01_input_p1.txt", "Day01_input_p2.txt", "Day01_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def parse_instructions(instruction_str):
    parsed = []
    for inst in instruction_str.split(","):
        parsed.append((inst[0], int(inst[1:])))
    return parsed

def run_instructions_linear(name_list, instructions):
    current_name = ""
    current_pos = 0
    total_len = len(name_list) - 1
    for dir, magn in instructions:
        if dir == "R":
            current_pos = min(current_pos + magn, total_len)
        elif dir == "L":
            current_pos = max(current_pos - magn, 0)
        current_name = name_list[current_pos]
    return current_name

def run_instructions_circular(name_list, instructions):
    current_name = ""
    current_pos = 0
    total_len = len(name_list)
    for dir, magn in instructions:
        if dir == "R":
            move = +1
        elif dir == "L":
            move = -1
        current_pos = (current_pos + (move * magn)) % total_len
        current_name = name_list[current_pos]
    return current_name

def run_instructions_swap(name_list, instructions):
    def swap_names(use_list, pos_1, pos_2):
        copy_list = use_list.copy()
        copy_list[pos_1] = use_list[pos_2]
        copy_list[pos_2] = use_list[pos_1]
        return copy_list
    total_len = len(name_list)
    for dir, magn in instructions:
        if dir == "R":
            move = +1
        elif dir == "L":
            move = -1
        swap_pos = (move * magn) % total_len
        name_list = swap_names(name_list, 0, swap_pos)
    return name_list[0]


quest_01_p1 = run_instructions_linear(input_data_p1[0].split(","), parse_instructions(input_data_p1[2]))
print("Quest 1, P1:", quest_01_p1)

quest_01_p2 = run_instructions_circular(input_data_p2[0].split(","), parse_instructions(input_data_p2[2]))
print("Quest 1, P2:", quest_01_p2)

quest_01_p3 = run_instructions_swap(input_data_p3[0].split(","), parse_instructions(input_data_p3[2]))
print("Quest 1, P3:", quest_01_p3)