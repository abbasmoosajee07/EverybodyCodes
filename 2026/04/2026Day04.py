"""Everybody Codes - Quest 4, Year 2026
Solution Started: October 30, 2026
Puzzle Link: https://everybody.codes/event/2026/quests/4
Solution by: Abbas Moosajee
Brief: [The Rankening]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque

# List of input file names
input_files = ["Day04_input_p1.txt", "Day04_input_p2.txt", "Day04_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def calc_checksum_p1(input_data):
    time_dict = defaultdict(int)
    for line in input_data:
        data = {k: int(v) for item in line.split() for k, v in [item.split("=")]}
        time_dict[data["id"]] += data["time"]
    sort_times = sorted(time_dict.values())
    return sum(pos * val for pos, val in enumerate(sort_times, start=1))

def calc_checksum_p2(input_data):
    time_dict = defaultdict(lambda: {"time": 0, "part": 0})
    for line in input_data:
        data = {k: int(v) for item in line.split() for k, v in [item.split("=")]}
        time_dict[data["id"]]["time"] += data["time"]
        time_dict[data["id"]]["part"] += 1
    sorted_times = sorted(
        time_dict.items(),
        key=lambda kv: (-kv[1]["part"], kv[1]["time"]),
    )
    return sum(rank * val["time"] for rank, (_, val) in enumerate(sorted_times, start=1))

def score_quests(input_data):
    records = [[int(kv.split("=")[1]) for kv in line.split()] for line in input_data]

    n = len({rec[0] for rec in records})

    rounds = defaultdict(list)
    for pid, quest, part, time in records:
        rounds[(quest, part)].append((time, pid))

    scores = [0] * n
    totals = [0] * n
    for (quest, part), entries in sorted(rounds.items()):
        if part == 1:
            totals = [0] * n
        for time, pid in entries:
            totals[pid - 1] += time

        ranked = sorted((totals[pid - 1], pid) for _, pid in entries)
        base = part * 50
        prev = None
        points = base

        for idx, (t, pid) in enumerate(ranked):
            if t != prev:
                points = base - idx
                if points < 0:
                    break
            scores[pid - 1] += points
            prev = t

    total = 0
    rank = 0
    prev = None
    for idx, score in enumerate(sorted(scores, reverse=True), start=1):
        if score != prev:
            rank = idx
            prev = score
        total += rank * score
    return total

print("EC 2026, Quest 04")
print("Part 1:", calc_checksum_p1(input_data_p1))
print("Part 2:", calc_checksum_p2(input_data_p2))
print("Part 3:", score_quests(input_data_p3))