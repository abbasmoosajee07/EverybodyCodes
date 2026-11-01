"""Everybody Codes - Quest 5, Year 2026
Solution Started: October 31, 2026
Puzzle Link: https://everybody.codes/event/2026/quests/5
Solution by: Abbas Moosajee
Brief: [The Cartograffity]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
# List of input file names
input_files = ["Day05_input_p1.txt", "Day05_input_p2.txt", "Day05_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class Cartograffity:
    neighbors = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (-1,1), (1,-1)]

    def __init__(self, init_grid):
        self.mid_point = (len(init_grid)//2, len(init_grid[0])//2)
        grid_dict = defaultdict(int)
        for row_no, row in enumerate(init_grid):
            for col_no, cell in enumerate(row):
                pos = (row_no, col_no)
                grid_dict[pos] = int(cell)
        self.grid_dict = grid_dict

    def build_land(self):
        land = {self.mid_point}
        queue = deque([self.mid_point])

        def qualifies(cell):
            count = 0
            for dr, dc in self.neighbors:
                n = (cell[0] + dr, cell[1] + dc)
                if n in land or self.grid_dict.get(n, 0) == 1:
                    count += 1
            return count >= 5

        while queue:
            curr = queue.popleft()
            for dr, dc in self.neighbors:
                cand = (curr[0] + dr, curr[1] + dc)
                if cand in land or cand not in self.grid_dict:
                    continue
                if qualifies(cand):
                    land.add(cand)
                    queue.append(cand)

        return land

    def add_coast(self):
        land = self.build_land()  # build_land must return the set

        sand = set()
        for point in land:
            for dr, dc in self.neighbors:
                cand = (point[0] + dr, point[1] + dc)
                if cand not in land:
                    sand.add(point)

        queue = deque(sand)
        while queue:
            curr = queue.popleft()
            for dr, dc in self.neighbors:
                cand = (curr[0] + dr, curr[1] + dc)
                if cand not in land or cand in sand:
                    continue
                count = sum(
                    (cand[0] + a, cand[1] + b) in sand
                    for a, b in self.neighbors
                )
                if count >= 5:
                    sand.add(cand)
                    queue.append(cand)

        return sand

    def plant_trees(self):
        land = self.build_land()
        sand = self.add_coast()

        ground = land - sand

        stamp = [(dr, dc) for dr in range(-2, 3) for dc in range(-2, 3)
                    if not (abs(dr) == 2 and abs(dc) == 2)]

        trees = {
            (r, c) for (r, c) in ground
            if all((r + dr, c + dc) in ground for dr, dc in stamp)
        }

        for _ in range(2):
            new_trees = set()
            for cell in ground - trees:
                nbrs = [(cell[0] + dr, cell[1] + dc) for dr, dc in self.neighbors]
                if any(n in sand for n in nbrs):
                    continue
                if sum(n in trees for n in nbrs) >= 4:
                    new_trees.add(cell)
            trees |= new_trees

        return trees
print("EC 2026, Quest 05")
print("Part 1:",len(Cartograffity(input_data_p1).build_land()))
print("Part 2:",len(Cartograffity(input_data_p2).add_coast()))
print("Part 2:",len(Cartograffity(input_data_p3).plant_trees()))

