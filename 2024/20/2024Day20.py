
# Everybody Codes - Day 20, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/20
# Solution by: [abbasmoosajee07]
# Brief: [Glider and finding Altitude]

#!/usr/bin/env python3

import os, re, copy, heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# List of input file names
input_files = ["Day20_p1_input.txt", "Day20_p2_input.txt", "Day20_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

# Directions
NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
MOVES = {
    NORTH: [(0, -1, WEST), (-1, 0, NORTH), (0, 1, EAST)],
    EAST: [(-1, 0, NORTH), (0, 1, EAST), (1, 0, SOUTH)],
    SOUTH: [(0, 1, EAST), (1, 0, SOUTH), (0, -1, WEST)],
    WEST: [(1, 0, SOUTH), (0, -1, WEST), (-1, 0, NORTH)],
}
ALTITUDE_CHANGE = {"+": 1, ".": -1, "-": -2, "S": -1, "A": -1, "B": -1, "C": -1}
CHECK_POINTS = "ABC"

# Functions for encoding and decoding state
def encode_state(r, c, d, p=0):
    """Encodes the state into a single integer."""
    return (r << 28) | (c << 16) | (d << 4) | p

def decode_state(state):
    """Decodes the state from a single integer."""
    return state >> 28, (state >> 16) & 0xFFF, (state >> 4) & 0xF, state & 0xF

def find_start_position(grid):
    """Finds the starting position 'S' in the grid."""
    return 0, next(c for c, v in enumerate(grid[0]) if v == "S")

def solve_part_1(grid):
    """Solves part 1."""
    n, m = len(grid), len(grid[0])
    rs, cs = find_start_position(grid)
    states = {encode_state(rs, cs, d): 1000 for d in MOVES.keys()}  # Initial states

    for _ in range(100):  # Simulation for 100 steps
        next_states = {}
        for state, altitude in states.items():
            r, c, d, _ = decode_state(state)
            for dr, dc, new_d in MOVES[d]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] in ".-+":
                    new_alt = altitude + ALTITUDE_CHANGE[grid[nr][nc]]
                    new_state = encode_state(nr, nc, new_d)
                    next_states[new_state] = max(next_states.get(new_state, float("-inf")), new_alt)
        states = next_states

    return max(states.values())

def solve_part_2(grid):
    """Solves part 2."""
    n, m = len(grid), len(grid[0])
    rs, cs = find_start_position(grid)
    states = {encode_state(rs, cs, d, 0): 10_000 for d in MOVES.keys()}
    t = 0

    while True:
        t += 1
        next_states = {}
        for state, altitude in states.items():
            r, c, d, p = decode_state(state)
            for dr, dc, new_d in MOVES[d]:
                nr, nc, new_p = r + dr, c + dc, p
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] in ".-+ABCS":
                    new_alt = altitude + ALTITUDE_CHANGE[grid[nr][nc]]

                    if grid[nr][nc] == "S" and new_alt >= 10_000 and new_p == len(CHECK_POINTS):
                        return t
                    elif grid[nr][nc] in CHECK_POINTS:
                        if new_p == CHECK_POINTS.index(grid[nr][nc]):
                            new_p += 1
                        else:
                            continue

                    new_state = encode_state(nr, nc, new_d, new_p)
                    next_states[new_state] = max(next_states.get(new_state, float("-inf")), new_alt)
        states = next_states

# Part 1
grid_part_1 = input_data_p1
ans1 = solve_part_1(grid_part_1)
print(f"Quest 1: {ans1}")

# Part 2
grid_part_2 = input_data_p2
ans2 = solve_part_2(grid_part_2)
print(f"Quest 2: {ans2}")

map_ = []
for i in input_data_p3:
    lst = []
    for j in i:
        lst.append(j)
    map_.append(lst)

mapsize = len(input_data_p3)


# Directions for movement: up, down, left, right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Function to check if a position is within bounds and not a wall
def is_valid(x, y, map_):
    return 0 <= x and 0 <= y < len(map_[0]) and map_[x%mapsize][y] != '#'

           
def get_height(tile):
    if tile == '-':
        return -2
    elif tile == '.':
        return -1
    elif tile in 'SABC':
        return -1
    return 1

def drawmap(path,x):
    times = 1 + (x//mapsize)
    print()
    for m in range(times):
        for i in range(len(map_)):
            ln = ''
            for j in range(len(map_[i])):
                if (i+m*mapsize,j) in path:
                    ln = ln + '*'
                else:
                    ln = ln + map_[i][j]
            print(ln)

# Function to find the shortest path visiting waypoints in order
def find_ordered_path(start, map_, startheight):
    # Priority queue: (current_time, x, y, current_waypoint_index)
    pq = [(startheight, start[0], start[1], start, [], 0, [])]
    
    DP = {}

    fs = 0    
    ct = 0
    ht = 0
    
    best = 0

    while pq:
        height, x, y, previous, path, steps, kvisited  = heapq.heappop(pq)
        
        ct += 1


        if height < 1:        
            fs += 1

            best = max(best,x)
            if fs > 30000:                     
                return x
            continue
                
        if (x, y) in DP:
            if height <= DP[(x, y)]:
                ht += 1
                #print('hit',ht)      
                continue
            else:
                #print('quicker route found')
                    DP[(x, y)] = height # , previous[0], previous[1])
        else:
                DP[(x, y)] = height  # , previous[0], previous[1])

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy            
            if (nx, ny) != previous:                
                if is_valid(nx, ny, map_):                        
                    nheight = height + get_height(map_[nx%mapsize][ny])
                    #print('new height',nheight)
                    npath = path[:]
                    npath.append(x) 
                    npath.append(y) 
                    npath.append(height)                         
                    npath.append('|')  
                    nkvisited = []
                    for kv in kvisited:
                        nkvisited.append((kv[0],kv[1]))
                    nkvisited.append((nx,ny))                    
                    heapq.heappush(pq, (nheight, nx, ny, (x,y), npath, steps+1, nkvisited))
    
    return best
#float('inf')  # If no valid path is found


def find_checkpoints(grid):
    checkpoints = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] not in ['#', '.', '+', '-']:# and grid[i][j] != 'S':
                checkpoints[grid[i][j]] = (i, j)
    return checkpoints

fs = find_checkpoints(map_)

ds = []

for t in range(1,40):
    total_dist = find_ordered_path(fs['S'], map_, t)
    ds.append([t,total_dist])

seek = 384400

dist = ds[-1][1]

leap1 = ds[-2][1] - ds[-3][1]
leap2 = ds[-1][1] - ds[-2][1]
lp = leap1
for i in range(seek - ds[-1][0]):
    dist += lp
    if lp == leap1:
        lp = leap2
    else:
        lp = leap1

ans_p3 = dist
print("Quest 3:", ans_p3)

