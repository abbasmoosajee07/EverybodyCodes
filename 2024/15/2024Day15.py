
# Everybody Codes - Day 15, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/15
# Solution by: [abbasmoosajee07]
# Brief: [Herb Races]

#!/usr/bin/env python3
import sys, os
from collections import defaultdict, deque
from itertools import permutations
from functools import lru_cache

# List of input file names
input_files = ["Day15_p1_input.txt", "Day15_p2_input.txt", "Day15_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Function to load the grid from the input file
def load_grid(part):
    with open(os.path.join(os.path.dirname(__file__), f"Day15_p{part}_input.txt")) as f:
        grid = {}
        for i, row in enumerate(f.read().splitlines()):
            for j, cell in enumerate(row):
                if cell not in "#~":
                    grid[(i, j)] = cell
        return grid

# Add two points (tuples)
def add_points(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

# BFS to compute minimum costs from a starting position
def compute_costs(start, grid):
    costs = {loc: float('inf') for loc in grid}
    costs[start] = 0
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for direction in DIRECTIONS:
            neighbor = add_points(current, direction)
            if neighbor in grid and costs[neighbor] > costs[current] + 1:
                costs[neighbor] = costs[current] + 1
                queue.append(neighbor)
    return costs

# Recursive function to compute the minimum cost of visiting all herbs
@lru_cache(None)
def min_cost_order(current, remaining_herbs, end):
    if not remaining_herbs:
        return all_costs[current][end]
    next_herb = remaining_herbs[0]
    next_locations = herb_locations[next_herb]
    return min(
        all_costs[current][next_loc] +
        min_cost_order(next_loc, remaining_herbs[1:], end)
        for next_loc in next_locations
    )

# Main loop for each part of the problem
for part in (1, 2, 3):
    # Load the grid and reset the cache
    min_cost_order.cache_clear()
    grid = load_grid(part)

    # Extract the start position and herb locations
    start = min(grid)
    herb_locations = defaultdict(list)
    for pos, value in grid.items():
        if value.isalpha():
            herb_locations[value].append(pos)

    # Generate the list of required locations (start + all herb locations)
    required_locations = [start]
    required_locations.extend(loc for locs in herb_locations.values() for loc in locs)

    # Precompute all-pairs shortest paths
    all_costs = {}
    for base in required_locations:
        all_costs[base] = compute_costs(base, grid)

    # Solve the problem for part 1 and part 2
    if part < 3:
        ans = min(
            min_cost_order(start, perm, start) for perm in permutations(herb_locations)
        )
        print(f"Quest {part}: {ans}")

    # Special logic for part 3
    else:
        mid_e = max(herb_locations["E"])
        mid_r = min(herb_locations["R"])

        abcde = min(
            min_cost_order(mid_e, perm, mid_e) for perm in permutations("ABCDE")
        )
        ghijk = min(
            min_cost_order(start, perm, start) for perm in permutations("EGHIJKR")
        )
        nopqr = min(
            min_cost_order(mid_r, perm, mid_r) for perm in permutations("NOPQR")
        )

        print(f"Quest {part}: {abcde + ghijk + nopqr}")
