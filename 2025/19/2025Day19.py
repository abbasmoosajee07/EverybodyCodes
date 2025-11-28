"""Everybody Codes - Quest 19, Year 2025
Solution Started: November 27, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/19
Solution by: Abbas Moosajee
Brief: [Flappy Quack]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
import time, math
start_time = time.time()

# List of input file names
input_files = ["Day19_input_p1.txt", "Day19_input_p2.txt", "Day19_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class GoldenTemple:
    def __init__(self, segment_data):
        segments = [tuple(map(int, row.split(","))) for row in segment_data]
        self.temple_map = self.build_temple(segments)

    def build_temple(self, blueprints):
        map_dict = defaultdict(list)
        for col, start, size in blueprints:
            map_dict[col].append((start, start + size - 1))
        return map_dict

    def count_flaps(self, y, dx, min_gap, max_gap):
        needed = (min_gap - y + dx) / 2
        flaps = max(0, math.ceil(needed))
        new_y = y + 2*flaps - dx
        if new_y > max_gap:
            return None
        return flaps, new_y

    def play_game(self):
        total_flaps = 0
        x, y = 0, 0

        for col in sorted(self.temple_map.keys()):
            dx = col - x

            best_flaps = float("inf")
            best_new_y = None

            for (min_gap, max_gap) in self.temple_map[col]:
                res = self.count_flaps(y, dx, min_gap, max_gap)
                if res is None:
                    continue
                flaps, new_y = res
                if flaps < best_flaps:
                    best_flaps = flaps
                    best_new_y = new_y

            total_flaps += best_flaps
            y = best_new_y
            x = col

        return total_flaps

temple_p1 = GoldenTemple(input_data_p1)
flaps_p1 = temple_p1.play_game()
print("Quest 19, P1:", flaps_p1)

temple_p2 = GoldenTemple(input_data_p2)
flaps_p2 = temple_p2.play_game()
print("Quest 19, P2:", flaps_p2)

temple_p3 = GoldenTemple(input_data_p3)
flaps_p3 = temple_p3.play_game()
print("Quest 19, P3:", flaps_p3)

print(f"Execution Time: {time.time() - start_time:5f}s")