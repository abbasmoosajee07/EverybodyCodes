"""Everybody Codes - Quest 6, Year 2025
Solution Started: November 11, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/6
Solution by: Abbas Moosajee
Brief: [Mentorship Matrix]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
from itertools import chain, islice, repeat, tee
# List of input file names
input_files = ["Day06_input_p1.txt", "Day06_input_p2.txt", "Day06_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def identify_mentorships(all_roles: str, valid_mentorship):
    valid_roles = [role for role in all_roles if role in valid_mentorship]
    possible_pairs = []
    for knight_idx, knight_role in enumerate(valid_roles):
        if not knight_role.isupper():
            continue
        for novice_idx, novice_role in enumerate(valid_roles[knight_idx:]):
            if novice_role.isupper():
                continue
            possible_pairs.append((knight_idx, knight_idx + novice_idx))
    return possible_pairs

def identify_all_mentorships(all_roles):
    sword_pairs = identify_mentorships(all_roles, "Aa")
    archery_pairs = identify_mentorships(all_roles, "Bb")
    magic_pairs = identify_mentorships(all_roles, "Cc")
    return sword_pairs + archery_pairs + magic_pairs

def identify_expanded_mentorships(base_roles, mult):
    mentors = Counter()

    WINDOW_SIZE = 1000

    all_roles = chain(
        repeat(None, WINDOW_SIZE*2),
        chain.from_iterable(repeat(base_roles, mult)),
        repeat(None, WINDOW_SIZE)
    )

    lows, values, highs = tee(all_roles, 3)
    values = islice(values, WINDOW_SIZE,   None)
    highs  = islice(highs,  WINDOW_SIZE*2, None)

    result = 0
    for lo, x, hi in zip(lows, values, highs):
        if hi is not None and hi.isupper():
            mentors[hi] += 1

        if x is not None and x.islower():
            result += mentors[x.upper()]

        if lo is not None and lo.isupper():
            mentors[lo] -= 1

    return result

sword_pairs = identify_mentorships(input_data_p1[0], "Aa")
print("Quest 06, P1:", len(sword_pairs))

all_pairs = identify_all_mentorships(input_data_p2[0])
print("Quest 06, P2:", len(all_pairs))

expanded_mentors = identify_expanded_mentorships(input_data_p3[0], 1000)
print("Quest 06, P3:", expanded_mentors)