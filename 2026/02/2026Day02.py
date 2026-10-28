"""Everybody Codes - Quest 2, Year 2026
Solution Started: October 28, 2026
Puzzle Link: https://everybody.codes/event/2026/quests/2
Solution by: Abbas Moosajee
Brief: [The Axeperiment]"""

#!/usr/bin/env python3
from pathlib import Path
from graphlib import TopologicalSorter

# List of input file names
input_files = ["Day02_input_p1.txt", "Day02_input_p2.txt", "Day02_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def arrange_alloys(alloy_list: str) -> int:
    sorter = TopologicalSorter()
    for pair in alloy_list.split():
        if ">" in pair:
            bigger, smaller = pair.split(">")
        else:
            smaller, bigger = pair.split("<")
        sorter.add(int(smaller), int(bigger))  # smaller depends on bigger
    return int("".join(map(str, sorter.static_order())))

alloy_p1 = [arrange_alloys(metals) for metals in input_data_p1[:]]
alloy_p2 = [arrange_alloys(metals) for metals in input_data_p2[:]]
alloy_p3 = [arrange_alloys(metals) for metals in input_data_p3[:]]

print("EC 2026, Quest 02")
print("Part 1:", sum(alloy_p1))
print("Part 2:", sum(alloy_p2))
print("Part 3:", sum(alloy_p3))