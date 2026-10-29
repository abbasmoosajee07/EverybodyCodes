"""Everybody Codes - Quest 3, Year 2026
Solution Started: October 29, 2026
Puzzle Link: https://everybody.codes/event/2026/quests/3
Solution by: Abbas Moosajee
Brief: [The ISOlation]"""

#!/usr/bin/env python3
from pathlib import Path

# List of input file names
input_files = ["Day03_input_p1.txt", "Day03_input_p2.txt", "Day03_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def extend_pattern(s, target):
    n = len(target)
    return (s * (n // len(s) + 1))[-n:]

def vote_calc(power_base, mult_base):
    power_base = extend_pattern(power_base, mult_base)
    power_to = len(mult_base)
    vote_total = 0
    for power, mult in zip(power_base, mult_base):
        power_to -= 1
        vote_total += int(mult) * int(power) ** power_to
    return vote_total

def convert_iso_vote(iso_str):
    power_base, mult_base = iso_str.strip("ISO-").split(" ")
    # print(mult_base, power_base, vote_total)
    return vote_calc(power_base, mult_base)

def min_mult_base(power_base, target, max_len=500):
    if target == 0:
        return "0"

    p = [int(c) for c in reversed(power_base)]
    w, cap = [], []        # weight per position; max total of positions 0..i
    memo = {}

    def solve(i, rem):
        if i < 0:
            return "" if rem == 0 else None
        if (i, rem) in memo:
            return memo[i, rem]
        below = cap[i - 1] if i else 0
        res = None
        for d in range(10 if w[i] else 1):      # weight 0 -> digit must be 0
            r = rem - d * w[i]
            if r < 0:
                break
            if r <= below and (sub := solve(i - 1, r)) is not None:
                res = str(d) + sub
                break
        memo[i, rem] = res
        return res

    for k in range(max_len):                    # try lengths k+1 = 1, 2, 3...
        w.append(p[k % len(p)] ** k)
        cap.append((cap[-1] if cap else 0) + 9 * w[k])
        if w[k] == 0 or cap[k] < target:
            continue
        for d in range(1, 10):                  # leading digit non-zero
            r = target - d * w[k]
            if r < 0:
                break
            if r <= (cap[k - 1] if k else 0) and (sub := solve(k - 1, r)) is not None:
                return str(d) + sub
    return None                                 # unreachable within max_len

def validate_vote(iso_str):
    power_base, mult_base = iso_str.removeprefix("ISO2-").split(" ")
    target_vote = vote_calc(power_base, mult_base)
    min_mult = min_mult_base(power_base, target_vote)
    if min_mult == mult_base:
        return target_vote
    return 0

votes_p1 = [convert_iso_vote(line) for line in input_data_p1]
votes_p2 = [convert_iso_vote(line) for line in input_data_p2]
votes_p3 = [validate_vote(line) for line in input_data_p3]

print("EC 2026, Quest 03")
print("Part 1:", sum(votes_p1))
print("Part 2:", sum(votes_p2))
print("Part 3:", sum(votes_p3))