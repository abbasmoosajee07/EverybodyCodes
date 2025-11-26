"""Everybody Codes - Quest 17, Year 2025
Solution Started: November 25, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/17
Solution by: Abbas Moosajee
Brief: [Deadline-Driven Development]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
import time
start_time = time.time()

# List of input file names
input_files = ["Day17_input_p1.txt", "Day17_input_p2.txt", "Day17_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class Volcano:
    def __init__(self, init_map):
        self.map_dict = self.parse_map(init_map)

    def parse_map(self, base_map):
        map_dict = {}
        for row_no, row_data in enumerate(base_map):
            for col_no, cell in enumerate(row_data):
                if cell == "@":
                    self.volcano_pos = (row_no, col_no)
                elif cell == "S":
                    self.start_pos = (row_no, col_no)
                    cell = 0
                else:
                    cell = int(cell)
                map_dict[(row_no, col_no)] = cell
        return map_dict

    def valid_dist(self, C, V):
        Xv, Yv = C
        Xc, Yc = V
        return (Xv - Xc) * (Xv - Xc) + (Yv - Yc) * (Yv - Yc)

    def check_formula(self, C, V, R):
        return self.valid_dist(C, V) <= R * R

    def adjacent(self, cell):
        i, j = cell
        return [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]

    def lava_flow(self, radius):
        total = 0
        for check_pos, cell in self.map_dict.items():
            if check_pos == self.volcano_pos:
                continue
            if self.check_formula(check_pos, self.volcano_pos, radius):
                total += int(cell)
        return total

    def max_destruction(self):
        destruction_calc = {}
        test_radii = list(range(1, self.volcano_pos[0]  + 1))
        current_map = self.map_dict.copy()
        
        for radius in test_radii:
            total = 0
            for check_pos, cell in current_map.items():
                if check_pos == self.volcano_pos or cell == "S":
                    continue
                if self.check_formula(check_pos, self.volcano_pos, radius):
                    total += int(cell)
                    current_map[check_pos] = 0
            destruction_calc[radius] = (total, total * radius)
        return max(destruction_calc.items(), key=lambda x: x[1][0])

    def loop_for_radius(self, radius):
        states = defaultdict(lambda: (10**12, None))
        states[self.start_pos] = (0, None)

        queue = deque(self.adjacent(self.start_pos))
        visited = set(queue)

        while queue:
            p = queue.popleft()
            visited.remove(p)

            best_cost = 10**12
            best_from = None

            for a in self.adjacent(p):
                if self.destruction_radius.get(a, -1) >= radius:
                    cost = states[a][0]
                    if cost < best_cost:
                        best_cost = cost
                        best_from = a

            best_cost += self.grid_weights.get(p, 10**15)

            if best_cost < states[p][0]:
                states[p] = (best_cost, best_from)
                for a in self.adjacent(p):
                    if self.destruction_radius.get(a, -1) >= radius and a not in visited:
                        queue.append(a)
                        visited.add(a)

        def trace(p):
            while p is not None:
                yield p
                p = states[p][1]

        # detect left/right crossings
        mi, mj = self.volcano_pos

        def side(path):
            for i, j in path:
                if i == mi:
                    return "left" if j < mj else "right"

        paths = {p: side(trace(p)) for p in states if states[p][0] < 10**14}

        left = {p for p, s in paths.items() if s == "left"}
        right = {p for p, s in paths.items() if s == "right"}

        # connect a left point to a right point
        best = float("inf")
        for l in left:
            for a in self.adjacent(l):
                if a in right:
                    cost = states[l][0] + states[a][0]
                    if cost < best:
                        best = cost

        return best

    def build_loop(self):

        self.grid_weights = self.map_dict.copy()
        # radius each cell falls under
        self.destruction_radius = {
            pos: int(self.valid_dist(pos, self.volcano_pos)**0.5 - 0.0001)
            for pos, c in self.map_dict.items()
            if c != '@'
        }

        # sweep radii
        max_r = max(self.destruction_radius.values())
        for radius in range(1, max_r):
            time_limit = 30 * (radius + 1)
            res = self.loop_for_radius(radius)
            if res < time_limit:
                return radius * res  # final answer
        return None

volcano_p1 = Volcano(input_data_p1)
lava_p1 = volcano_p1.lava_flow(10)
print("Quest 17, P1:", lava_p1)

volcano_p2 = Volcano(input_data_p2)
lava_p2 = volcano_p2.max_destruction()
print("Quest 17, P2:", lava_p2[1][1])

volcano_p3 = Volcano(input_data_p3)
recurlia_cost = volcano_p3.build_loop()
print("Quest 17, P3:", recurlia_cost)

print(f"Execution Time: {time.time() - start_time:5f}s")