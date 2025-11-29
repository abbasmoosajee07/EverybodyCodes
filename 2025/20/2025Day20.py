"""Everybody Codes - Quest 20, Year 2025
Solution Started: November 28, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/20
Solution by: Abbas Moosajee
Brief: [Dream in Triangles]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
from itertools import zip_longest
import time
start_time = time.time()

# List of input file names
input_files = ["Day20_input_p1.txt", "Day20_input_p2.txt", "Day20_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class Triangles:
    NEIGHBORS = [
        [(0, 0, 1), (0, 1, 1), (-1, 0, 1)], # Down
        [(0, 0, -1), (0, 1, -1), (1, 0, -1)], # Upper triangle
    ]
    def __init__(self, inp_grid):
        self.grid_dict = self.parse_grid(inp_grid)
    def parse_grid(self, input_grid):
        grid_dict = {}
        for row_no, row_data in enumerate(input_grid):
            for col_no, cell in enumerate(row_data):
                if cell == '.':
                    continue
                if row_no % 2 == 0:
                    state = col_no % 2
                else:
                    state = 1 - (col_no % 2)
                # state = (row_no + col_no) % 2
                pos = (row_no, col_no, state)
                grid_dict[pos] = cell
                if cell == "E":
                    self.end_pos = pos
                elif cell == 'S':
                    self.start_pos = pos
        return grid_dict

    def get_neighbors(self, pos):
        row, col, state = pos
        state_neighbors = self.NEIGHBORS[state]
        all_neighbors = []
        for dr, dc, ds in state_neighbors:
            new_pos = (row + dr, col + dc, state + ds)
            all_neighbors.append(new_pos)
        return all_neighbors

    def count_trampolines(self):
        total_jumps = set()
        self.valid_jumps = defaultdict(list)
        for pos, cell in self.grid_dict.items():
            all_neighbors = self.get_neighbors(pos)
            if cell  not in 'TSE':
                continue
            for test in all_neighbors:
                neighbor_type = self.grid_dict.get(test, '.')
                if neighbor_type not in 'TSE':
                    continue
                total_jumps.add(tuple(sorted((pos, test))))
                self.valid_jumps[pos].append(test)
                
        return total_jumps

    def bfs_path(self):
        queue = deque([(self.start_pos, [self.start_pos])])
        visited = set()
        print(self.start_pos, self.end_pos)
        valid_jumps = self.count_trampolines()
        print(len(valid_jumps))
        while queue:
            current_pos, current_path = queue.popleft()

            if current_pos == self.end_pos:
                return current_path

            valid_neighbors = self.valid_jumps[current_pos]
            print(current_pos, valid_neighbors)
            for neighbor in valid_neighbors:
                try_jump = tuple(sorted((current_pos, neighbor)))
                if try_jump not in visited:
                    visited.add(try_jump)
                    queue.append((neighbor, current_path + [neighbor]))
                    #print(current_pos, current_path + [neighbor])

        return []

def adj(p):
    i, j = p
    yield i, j - 1
    yield i, j + 1
    if j % 2:  # ^
        yield i + 1, j - 1
    else:  # v
        yield i - 1, j + 1

class TriangleGrid:
    def __init__(self, grid_data):
        self.grid_dict = self.parse_grid(grid_data)

    def parse_grid(self, grid_data):
        grid_dict = {}
        for row_no, row_data in enumerate(grid_data):
            for col_no, cell in enumerate(row_data.strip('.')):
                if cell == '.':
                    continue
                pos = (row_no, col_no)
                # Convert S and E to T like original code
                if cell == 'S':
                    self.start_pos = pos
                    cell = 'T'  # Convert to T
                elif cell == 'E':
                    self.end_pos = pos  
                    cell = 'T'  # Convert to T
                grid_dict[pos] = cell
        return grid_dict
    
    def get_adjacent(self, pos):
        
        return list(adj(pos))
    
    def count_trampoline_pairs(self):
        total = 0
        for p, cell in self.grid_dict.items():
            if cell == 'T':
                for a in adj(p):
                    total += self.grid_dict.get(a) == 'T'
        return total // 2

    def find_shortest_path(self):
        grid_dict = self.grid_dict
        start = self.start_pos
        end = self.end_pos
        
        costs = {}
        # Only include T cells in costs (S and E were converted to T)
        for p, cell in grid_dict.items():
            if cell == 'T':
                costs[p] = 10**10
        costs[start] = 0

        q = deque([start])
        in_q = set(q)
        while q:
            p = q.popleft()
            in_q.remove(p)
            cost = costs[p] + 1
            for a in adj(p):
                if a in costs and cost < costs[a]:
                    costs[a] = cost
                    if a not in in_q:
                        q.append(a)
                        in_q.add(a)
        return costs.get(end, -1)  # Use get() to avoid KeyError

class RotatingHexGrid(TriangleGrid):
    def __init__(self, grid_data):
        super().__init__(grid_data)
        self.rotation_grid = self.build_rotation_grid(grid_data)
    
    def build_rotation_grid(self, original_grid):
        """EXACT copy of your rotation code"""
        grid = [line.strip('.') for line in original_grid]
        
        temp_rotation_grid = [[(i, j) for j, cell in enumerate(row)] for i, row in enumerate(grid)]
        temp_rotation_grid = [row[e::2] for row in temp_rotation_grid for e in (0, 1)]
        temp_rotation_grid.reverse()
        temp_rotation_grid = [list(filter(None, r)) for r in zip_longest(*temp_rotation_grid)]
        rotation_grid = {(i, j): d for i, row in enumerate(temp_rotation_grid) for j, d in enumerate(row)}
        
        return rotation_grid
    
    def rotate_coord(self, p):
        return self.rotation_grid.get(p)
    
    def adjr(self, p):
        yield self.rotate_coord(p)  # in place
        for a in adj(p):
            yield self.rotate_coord(a)
    
    def find_shortest_path_rotated(self):
        grid_dict = self.grid_dict
        start = self.start_pos
        end = self.end_pos
        
        costs = {}
        for p, cell in grid_dict.items():
            if cell == 'T':
                costs[p] = 10**10
        costs[start] = 0

        q = deque([start])
        in_q = set(q)
        while q:
            p = q.popleft()
            in_q.remove(p)
            cost = costs[p] + 1
            for a in self.adjr(p):
                if a in costs and cost < costs[a]:
                    costs[a] = cost
                    if a not in in_q:
                        q.append(a)
                        in_q.add(a)
        return costs.get(end, -1)  # Use get() to avoid KeyError

triangles_p1 = TriangleGrid(input_data_p1)
jumps_p1 = triangles_p1.count_trampoline_pairs()
print("Quest 20, P1:", (jumps_p1))

triangles_p2 = TriangleGrid(input_data_p2)
path_p2 = triangles_p2.find_shortest_path()
print("Quest 20, P2:", (path_p2))

triangles_p3 = RotatingHexGrid(input_data_p3)
path_p3 = triangles_p3.find_shortest_path_rotated()
print("Quest 20, P2:", path_p3)
print(f"Execution Time: {time.time() - start_time:5f}s")