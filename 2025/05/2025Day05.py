"""Everybody Codes - Quest 5, Year 2025
Solution Started: November 7, 2025
Puzzle Link: https://everybody.codes/event/20252/quests/5
Solution by: Abbas Moosajee
Brief: [Fishbone Order]"""

#!/usr/bin/env python3
from pathlib import Path

# List of input file names
input_files = ["Day05_input_p1.txt", "Day05_input_p2.txt", "Day05_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def build_spine(input_data: str):
    sword_id, all_bones = input_data.split(":")
    all_bones = list(map(int, all_bones.split(",")))

    spine = []
    spine.append({0: all_bones[0]})

    for bone in all_bones[1:]:
        placed = False

        # Try each segment in order from top to bottom
        for segment in spine:
            pivot_dir = segment[0]

            if bone < pivot_dir:
                if -1 not in segment:
                    segment[-1] = bone
                    placed = True
                    break
            elif bone > pivot_dir:
                if 1 not in segment:
                    segment[1] = bone
                    placed = True
                    break
            else:
                continue
        if not placed:
            spine.append({0: bone})
    conc_spine = {}
    for seg, data in enumerate(spine):
        conc_spine[seg] = int(f"{data.get(-1, "")}{data[0]}{data.get(1, "")}")
    return int("".join(str(seg[0]) for seg in spine)), conc_spine

def build_armory(input_list):
    armory = []
    for id, data in enumerate(input_list):
        sword_quality = build_spine(data)[0]
        armory.append(sword_quality)
    return max(armory) - min(armory)

def identify_swords(data):
    sword_list = []
    for id, numdata in enumerate(data, 1):
        spine, fishbone = build_spine(numdata)
        sword_list.append((spine, list(fishbone.values()), id))
    sword_list.sort(reverse=True)
    return sum(i*n[2] for i,n in enumerate(sword_list, 1))

print("Quest 05, P1:", build_spine(input_data_p1[0])[0])
print("Quest 05, P2:", build_armory(input_data_p2))
print("Quest 05, P3:", identify_swords(input_data_p3))
