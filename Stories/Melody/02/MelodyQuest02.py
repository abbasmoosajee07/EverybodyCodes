# %%
"""Everybody Codes - Quest 2, Story Melody Made of Code
Solution Started: March 4, 2026
Puzzle Link: https://everybody.codes/story/3/quests/2
Solution by: Abbas Moosajee
Brief: [How Echoes Quack Back]"""

#!/usr/bin/env python3
from pathlib import Path


from collections import defaultdict
input_files = ["Quest02_input_p1.txt", "Quest02_input_p2.txt", "Quest02_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]



def build_grid_dict(grid_data):
    grid_dict = {}
    for row_no, row_data in enumerate(grid_data):
        for col_no, cell in enumerate(row_data):
            grid_dict[(row_no, col_no)] = cell
            if cell == "@":
                start = row_no, col_no
    return grid_dict, start

def print_grid(grid):
    max_row = max(r for r, c in grid)
    max_col = max(c for r, c in grid)
    for r in range(max_row + 1):
        print("".join(grid[(r, c)] for c in range(max_col + 1)))

def simulate_sound_waves(grid, start):
    current = start
    move_pos = 0
    steps = 0
    grid[current] = '+'
    MOVES_ORDER = "^>v<"
    MOVES_DICT = {"^":(-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    while True:
        for i in range(len(MOVES_ORDER)):
            sound_dir = MOVES_ORDER[(move_pos + i) % len(MOVES_ORDER)]
            dr, dc = MOVES_DICT[sound_dir]
            new_pos = (current[0] + dr, current[1] + dc)
            next_cell = grid[new_pos]
            if next_cell == "#":
                return steps + 1

            if next_cell != "+":  # unvisited, take this move
                move_pos = (move_pos + i + 1) % len(MOVES_ORDER)
                current = new_pos
                grid[current] = '+'
                steps += 1
                break
        else:
            return steps  # all directions blocked

grid_p1, start_p1  = build_grid_dict(input_data_p1)
print("Melody Quest 02, P1:", simulate_sound_waves(grid_p1, start_p1))
MOVES_ORDER = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # ^>v<

def all_adjs(p):
    r, c = p
    return [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]

def get_next(pos, step_index):
    r, c = pos
    dr, dc = MOVES_ORDER[step_index % 4]
    return (r + dr, c + dc)

def is_enclosed(p, seen):
    return not (set(all_adjs(p)) - seen)

def block_enclosed(p, seen):
    for a in all_adjs(p):
        if a not in seen and is_enclosed(a, seen):
            seen.add(a)
            block_enclosed(a, seen)

def surround_sound_waves(grid, start):
    obstacles = [pos for pos, cell in grid.items() if cell == "#"]
    seen = {start, *obstacles}
    goal = {a for obs in obstacles for a in all_adjs(obs)}

    pos = start
    step_index = 0
    num_steps = 0
    fails = 0

    while goal - seen:
        new = get_next(pos, step_index)
        step_index += 1
        if new not in seen:
            fails = 0
            pos = new
            num_steps += 1
            seen.add(pos)
            block_enclosed(pos, seen)
        else:
            fails += 1
            if fails > 10:
                break  # truly stuck

    return num_steps

grid_p2, start_p2 = build_grid_dict(input_data_p2)
print("Melody Quest 02, P2:", surround_sound_waves(grid_p2, start_p2))

def flood_block(seen):
    min_r = min(r for r, c in seen) - 1
    max_r = max(r for r, c in seen) + 1
    min_c = min(c for r, c in seen) - 1
    max_c = max(c for r, c in seen) + 1

    # Seed the flood from the entire border of the expanded bounding box
    reachable = (
        {(min_r, c) for c in range(min_c, max_c + 1)} |
        {(max_r, c) for c in range(min_c, max_c + 1)} |
        {(r, min_c) for r in range(min_r, max_r + 1)} |
        {(r, max_c) for r in range(min_r, max_r + 1)}
    )
    all_cells = {(r, c) for r in range(min_r, max_r + 1) for c in range(min_c, max_c + 1)}

    # BFS outward from border, blocked by seen cells
    changes = True
    while changes:
        changes = False
        for cell in list(reachable):
            if cell not in seen:
                for adj in all_adjs(cell):
                    if adj in all_cells and adj not in reachable:
                        reachable.add(adj)
                        changes = True

    # Everything not reachable from outside is enclosed — add it to seen
    seen |= all_cells - reachable

def get_next_p3(pos, step_index):
    r, c = pos
    dr, dc = MOVES_ORDER[(step_index // 3) % 4]
    return (r + dr, c + dc)

def surround_sound_waves_p3(grid, start):
    obstacles = [pos for pos, cell in grid.items() if cell == "#"]
    seen = {start, *obstacles}
    goal = {a for obs in obstacles for a in all_adjs(obs)}

    pos = start
    step_index = 0
    num_steps = 0
    fails = 0

    flood_block(seen)  # mark any cells already enclosed at the start

    while goal - seen:
        new = get_next_p3(pos, step_index)
        step_index += 1
        if new not in seen:
            fails = 0
            pos = new
            num_steps += 1
            seen.add(pos)
            flood_block(seen)
        else:
            fails += 1
            if fails > 10:
                break  # truly stuck

    return num_steps

grid_p3, start_p3 = build_grid_dict(input_data_p3)
print("Melody Quest 02, P3:", surround_sound_waves_p3(grid_p3, start_p3))