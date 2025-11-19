"""Everybody Codes - Quest 12, Year 2025
Solution Started: November 18, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/12
Solution by: Abbas Moosajee
Brief: [One Spark to Burn Them All]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import deque, defaultdict
import time
start_time = time.time()
# List of input file names
input_files = ["Day12_input_p1.txt", "Day12_input_p2.txt", "Day12_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class Barrels:
    DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    def __init__(self, barrel_map):
        self.barrel_dict = defaultdict()
        for row_no, row_data in enumerate(barrel_map):
            for col_no, cell in enumerate(row_data):
                self.barrel_dict[(row_no, col_no)] = int(cell)

    def light_fire(self, ignited = (0, 0)):
        visited = set()
        barrels_destroyed = set()
        queue = deque([ignited])
        while queue:
            current = queue.popleft()
            barrel_val = self.barrel_dict[current]
            barrels_destroyed.add(current)
            for dr, dc in self.DIRECTIONS:
                next_pos = (current[0] + dr, current[1] + dc)
                state = (current, next_pos)
                if state in visited or next_pos not in self.barrel_dict:
                    continue
                visited.add(state)
                next_barrel = self.barrel_dict[next_pos]
                if next_barrel <= barrel_val:
                    queue.append(next_pos)
        return barrels_destroyed

    def max_destruction(self, picks=3):
        total_destroyed = set()

        for i in range(picks):
            best_point = None
            best_gain = 0
            best_set = None

            # try every starting point
            for test_pos  in self.barrel_dict.keys():
                if test_pos in total_destroyed:
                    continue
                destroyed = self.light_fire(test_pos)
                gain = len(destroyed - total_destroyed)
                if gain > best_gain:
                    best_gain = gain
                    best_point = test_pos
                    best_set = destroyed

            if best_set:
                total_destroyed |= best_set

            # print(f"Pick {i}: ignite at {best_point}, total destroyed = {len(total_destroyed)}")
        return total_destroyed

from collections import deque, defaultdict
import heapq

class Barrels:
    DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def __init__(self, barrel_map, precompute = False):
        self.barrel_dict = {}

        for row_no, row_data in enumerate(barrel_map):
            for col_no, cell in enumerate(row_data):
                self.barrel_dict[(row_no, col_no)] = int(cell)
        if precompute:
            # Precompute destruction sets
            self._precompute_destruction_sets()

    def _precompute_destruction_sets(self):
        """Precompute destruction sets for all positions once."""
        self.destruction_cache = {}
        for pos in self.barrel_dict:
            self.destruction_cache[pos] = self.light_fire(pos)

    def light_fire(self, ignited=(0, 0)):
        visited = set()
        barrels_destroyed = set()
        queue = deque([ignited])

        while queue:
            current = queue.popleft()
            if current in barrels_destroyed:
                continue

            barrel_val = self.barrel_dict[current]
            barrels_destroyed.add(current)

            for dr, dc in self.DIRECTIONS:
                next_pos = (current[0] + dr, current[1] + dc)
                if next_pos not in self.barrel_dict or next_pos in barrels_destroyed:
                    continue

                next_barrel = self.barrel_dict[next_pos]
                if next_barrel <= barrel_val:
                    queue.append(next_pos)

        return barrels_destroyed

    def max_destruction(self, picks=3):
        total_destroyed = set()
        available_positions = set(self.barrel_dict.keys())

        for _ in range(picks):
            if not available_positions:
                break

            best_point = None
            best_gain = 0
            best_set = None

            # Consider only positions that are still available
            for test_pos in list(available_positions):
                destroyed = self.destruction_cache[test_pos]
                new_destroyed = destroyed - total_destroyed
                gain = len(new_destroyed)

                # Early termination if no gain
                if gain == 0:
                    available_positions.discard(test_pos)
                    continue

                if gain > best_gain:
                    best_gain = gain
                    best_point = test_pos
                    best_set = destroyed

            if best_point is None:
                break

            # Update sets
            total_destroyed |= best_set
            available_positions -= best_set
        return total_destroyed

barrels_p1 = Barrels(input_data_p1)
destroyed_p1 = barrels_p1.light_fire()
print("Quest 12, P1:", len(destroyed_p1))

barrels_p2 = Barrels(input_data_p2)
ignition_points = (min(barrels_p2.barrel_dict.keys()), max(barrels_p2.barrel_dict.keys()))
destroyed_p2 = barrels_p2.light_fire(ignition_points[0]) | barrels_p2.light_fire(ignition_points[1])
print("Quest 12, P2:", len(destroyed_p2))

barrels_p3 = Barrels(input_data_p3, True)
destroyed_p3 = barrels_p3.max_destruction()
print("Quest 12, P3:", len(destroyed_p3))
# print(f"Execution Time: {time.time() - start_time:5f}s")