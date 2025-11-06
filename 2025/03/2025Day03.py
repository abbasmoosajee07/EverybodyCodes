"""Everybody Codes - Quest 3, Year 2025
Solution Started: November 6, 2025
Puzzle Link: https://everybody.codes/event/20252/quests/3
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
# List of input file names
input_files = ["Day03_input_p1.txt", "Day03_input_p2.txt", "Day03_input_p3.txt"]

def parse_input(input_str: str) -> list[int]:
    return [int(x) for x in input_str.split(",") if x.strip()]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    parse_input(open(Path(__file__).parent / file).read().strip().split('\n')[0])
    for file in input_files
]

print("Quest 03, P1:", sum(set(input_data_p1)))
print("Quest 03, P2:", sum(sorted(set(input_data_p2))[:20]))
print("Quest 03, P3:", max(Counter(input_data_p3).values()))

