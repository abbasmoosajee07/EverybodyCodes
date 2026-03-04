"""Everybody Codes - Quest 1, Story Melody Made of Code
Solution Started: March 3, 2026
Puzzle Link: https://everybody.codes/story/3/quests/1
Solution by: Abbas Moosajee
Brief: [Scales, Bags and a Bit of a Messs]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
input_files = ["Quest01_input_p1.txt", "Quest01_input_p2.txt", "Quest01_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def convert_to_num(color_str):
    bin_num = ""
    for letter in color_str:
        conv_val = "0"
        if letter.isupper():
            conv_val = "1"
        bin_num += conv_val
    return int(bin_num, 2)

dominant_green_p1 = []
for row_scales in input_data_p1:
    scale_no, scale_data = row_scales.split(":")
    red, green, blue = scale_data.split()
    red_num, green_num, blue_num = convert_to_num(red), convert_to_num(green), convert_to_num(blue)

    scale_dict = {"red": red_num, "green": green_num, "blue": blue_num}
    if len(set(scale_dict.values())) == len(scale_dict.values()) and max(scale_dict, key=scale_dict.get) == "green":
        dominant_green_p1.append(int(scale_no))

print("Melody Quest 01, P1:", sum(dominant_green_p1))

shine_dict = {}
for row_scales in input_data_p2:
    scale_no, scale_data = row_scales.split(":")
    red, green, blue, shine = scale_data.split()
    red_num, green_num, blue_num, shine_num = convert_to_num(red), convert_to_num(green), convert_to_num(blue), convert_to_num(shine)
    scale_dict = {"red": red_num, "green": green_num, "blue": blue_num}
    color_val = red_num + blue_num + green_num
    shine_dict[int(scale_no)] = {"shine": shine_num, "color": color_val}
sorted_keys = sorted(shine_dict, key=lambda k: (-shine_dict[k]['shine'], shine_dict[k]['color']))

print("Melody Quest 01, P2:", sorted_keys[0])

color_dict = defaultdict(list)
for row_scales in input_data_p3:
    scale_no, scale_data = row_scales.split(":")
    red, green, blue, shine = scale_data.split()
    red_num, green_num, blue_num, shine_num = convert_to_num(red), convert_to_num(green), convert_to_num(blue), convert_to_num(shine)
    scale_dict = {"red": red_num, "green": green_num, "blue": blue_num}
    values = list(scale_dict.values())
    if values.count(max(values)) == 1:
        dominant_color = max(scale_dict, key=scale_dict.get)
    else:
        continue
    if shine_num <= 30:
        shine_type = "matte"
    elif shine_num >= 33:
        shine_type = "shiny"
    else:
        continue
    color_group = f"{dominant_color}-{shine_type}"
    color_dict[color_group].append(int(scale_no))

biggest_color = max(color_dict, key=lambda k: len(color_dict[k]))

print("Melody Quest 01, P3:", sum(color_dict[biggest_color]))