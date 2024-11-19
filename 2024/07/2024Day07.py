# Everybody Codes - Day 7, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/7
# Solution by: [abbasmoosajee07]
# Brief: [Race Tracks and Fights]

#!/usr/bin/env python3

import os, re, copy, itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# List of input file names
input_files = ["Day07_p1_input.txt", "Day07_p2_input.txt", "Day07_p3_input.txt", "race_track_p2.txt", "race_track_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3, track_p2_txt, track_p3_txt = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(race_track), print(input_data_p3)
def ranking_grid(input_data, loops = 1):
    rank_grid = []
    for row in input_data:
        row_data = row.split(':')
        start_rank = 10
        row_rank = []
        ranks = row_data[1].split(',')

        for _ in range(loops):  # Loop `loops` times
            for i in range(len(ranks)):
                rank = ranks[i % len(ranks)]  # Circular iteration
                if rank == '+':
                    start_rank += 1
                elif rank == '-':
                    start_rank -= 1
                elif rank == '=':
                    start_rank = start_rank  # No change for '='
                row_rank.append(start_rank)

        rank_grid.append([row_data[0], sum(row_rank)])
    rank_array = np.array(rank_grid)

    # Sort the second column (ranking) in descending order
    sorted_indices = np.argsort(rank_array[:, 1])[::-1]
    sorted_rankings = rank_array[sorted_indices, 0]  # Reordered first column (knights)
    return ''.join(sorted_rankings), rank_array

def flatten_race_track(race_track_array):
    race_start = ''.join(race_track_array[0][1:])
    race_end = ''.join(race_track_array[-1][::-1])
    race_track = [race_start]
    line_end = []
    for row_no in range(1, len(race_track_array) - 1):
        current_track = race_track_array[row_no]
        race_track.append(current_track[-1])
        line_end.append(current_track[0])
    line_end.append('S')
    race_track.append(race_end)
    race_track += line_end
    return ''.join(race_track)

def running_race(input_data, race_track , total_laps):
    race_grid = []
    by_score = {}
    for row in input_data:
        knight, segments = row.split(':')
        segments = segments.split(',')

        updated_row = [knight, ':']
        updated_essence = []

        idx = 0
        for lap in range(total_laps):
            # Iterate through race_track (circularly)
            for track_symbol in race_track:
                pos = idx % len(segments)  # Circular indexing into segments
                old_essence = segments[pos]

                # Update `updated_essence` based on the symbol in `race_track`
                if track_symbol == '=' or track_symbol == 'S':
                    updated_essence.append(old_essence)
                elif track_symbol == '+':
                    updated_essence.append('+')
                elif track_symbol == '-':
                    updated_essence.append('-')
                idx += 1

        updated_row.append(','.join(updated_essence))
        race_grid.append(''.join(updated_row))

    # Get rankings and timeline for the race
    race_results, race_timeline = ranking_grid(race_grid)

    return race_results, np.array(race_timeline)

ans_p1, _ = ranking_grid(input_data_p1)
print(f"Quest 1: {ans_p1}")

race_track_p2 = flatten_race_track(track_p2_txt)
ans_p2, timeline_p2 = running_race(input_data_p2, race_track_p2, 10)
print(f"Quest 2: {ans_p2}")

def create_race_track(track_map):
    rows, cols = len(track_map), len(track_map[0])
    row, col, direction = 0, 0, 1
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N, E, S, W
    path = ''
    is_done = False
    steps = 0
    while not is_done:
        if len(path) > 0 and track_map[row][col] == 'S':
            break
        if is_done:
            break
        for new_direction in [direction, (direction + 3) % 4, (direction + 1) % 4]:
            new_row = row + directions[new_direction][1]
            new_col = col + directions[new_direction][0]
            if 0 <= new_row < len(track_map) and 0 <= new_col < len(track_map[new_row]) and track_map[new_row][new_col] != ' ':
                path += track_map[new_row][new_col]
                row, col = new_row, new_col
                direction = new_direction
                steps += 1
                break
        if track_map[row][col] == 'S':
            is_done = True
    return path

def score_one(action_sequence, track_map, memo):
    action_key = tuple(action_sequence)
    if action_key in memo:
        return memo[action_key]

    current_power = 0
    total_score = 0
    action_index = 0

    for track_symbol in track_map:
        if track_symbol == '=' or track_symbol == 'S':
            track_symbol = action_sequence[action_index % len(action_sequence)]

        if track_symbol == '+':
            current_power += 1
        elif track_symbol == '-':
            current_power -= 1
        else:
            assert track_symbol == '=' or track_symbol == 'S', track_symbol

        total_score += current_power
        action_index += 1

    memo[action_key] = (total_score, current_power)
    return (total_score, current_power)

def score(actions, track, rounds, DP):
    score = 0
    power = 10
    i = 0
    for round_ in range(rounds):
        round_actions = actions[i:] + actions[:i]
        #print(f'{i=} {round_actions=} {actions=}')
        round_score, round_power = score_one(round_actions, track, DP)
        score += round_score + power * len(track)
        power += round_power
        i = (i+len(track))%len(actions)
    return score

def action_plan(input_lines, track):
    actions_by_player_id = {}

    for line in input_lines:
        player_id, actions = line.split(':')
        action_sequence = actions.split(',')
        actions_by_player_id[player_id] = action_sequence

    memo = {}
    num_rounds = 2024
    opponent_score = score(actions_by_player_id['A'], track, num_rounds, memo)

    num_optimal_plans = 0
    all_possible_plans = set(itertools.permutations('+++++---==='))

    for i, plan in enumerate(all_possible_plans):
        plan_score = score(plan, track, num_rounds, memo)

        if plan_score > opponent_score:
            num_optimal_plans += 1

    return num_optimal_plans

track_str = create_race_track(track_p3_txt)
ans_p3 = action_plan(input_data_p3, track_str)

print(f"Quest 3: {ans_p3}")