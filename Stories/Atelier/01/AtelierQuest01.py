"""Everybody Codes - Quest 1, Story The Digital Atelier
Solution Started: September 7, 2026
Puzzle Link: https://everybody.codes/story/4/quests/1
Solution by: Abbas Moosajee
Brief: [The Recamán Drapery]"""

#!/usr/bin/env python3
from pathlib import Path
import bisect

# Load input file
input_files = ["Quest01_input_p1.txt", "Quest01_input_p2.txt", "Quest01_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def recaman_basic(full_seq):
    visited = set()
    idx = 0
    for jump in full_seq:
        new_idx = idx - jump
        if new_idx <= 0 or new_idx in visited:
            idx += jump

        else:
            idx -= jump
        visited.add(idx)
    return idx

def recaman_fwd(full_seq):
    visited = set()
    idx = 0
    for jump in full_seq:
        new_idx = idx - jump
        if new_idx <= 0 or new_idx in visited:
            idx += jump
            while True:
                if idx in visited:
                    idx += 1
                else:
                    break
        else:
            idx -= jump
        visited.add(idx)
    return idx


class _Side:
    """Tracks arcs for one side (above/below), sorted two ways:
    - by start (a1), to answer: max(a2) among arcs with a1 in (lo,hi)
    - by end   (a2), to answer: min(a1) among arcs with a2 in (lo,hi)
    """
    __slots__ = ('starts', 'start_ends', 'ends', 'end_starts')

    def __init__(self):
        self.starts = []       # sorted a1 values
        self.start_ends = []   # a2, parallel to `starts`
        self.ends = []         # sorted a2 values
        self.end_starts = []   # a1, parallel to `ends`

    def crosses(self, lo, hi):
        # Case 1: an arc starts inside (lo,hi) and ends at/after hi.
        i = bisect.bisect_right(self.starts, lo)
        j = bisect.bisect_left(self.starts, hi)
        if i < j and max(self.start_ends[i:j]) >= hi:
            return True
        # Case 2: an arc ends inside (lo,hi) and starts at/before lo.
        i = bisect.bisect_right(self.ends, lo)
        j = bisect.bisect_left(self.ends, hi)
        if i < j and min(self.end_starts[i:j]) <= lo:
            return True
        return False

    def add(self, a1, a2):
        i = bisect.bisect_left(self.starts, a1)
        self.starts.insert(i, a1)
        self.start_ends.insert(i, a2)
        j = bisect.bisect_left(self.ends, a2)
        self.ends.insert(j, a2)
        self.end_starts.insert(j, a1)


class _NextFree:
    """Union-find that answers 'smallest free integer >= x' in near O(1)
    amortized time, replacing a 'while forward in visited: forward += 1'
    loop (which is O(n) per call in the worst case)."""
    __slots__ = ('parent',)

    def __init__(self):
        self.parent = {}

    def find(self, x):
        p = self.parent
        path = []
        while x in p:
            path.append(x)
            x = p[x]
        for node in path:
            p[node] = x
        return x

    def occupy(self, x):
        self.parent[x] = x + 1

def recaman_full(full_seq, max_forward_trials=10_000):
    visited = {0}
    next_free = _NextFree()
    next_free.occupy(0)

    sides = [_Side(), _Side()]
    arc_count = 0
    idx = 0

    for jump in full_seq:
        base = idx
        placed = False
        side = sides[arc_count % 2]

        backward = idx - jump
        if backward > 0 and backward not in visited:
            lo, hi = (base, backward) if base < backward else (backward, base)
            if not side.crosses(lo, hi):
                idx = backward
                side.add(lo, hi)
                placed = True

        if not placed:
            trial_jump = jump
            for _ in range(max_forward_trials):
                forward = base + trial_jump
                if forward in visited:
                    forward = next_free.find(forward)
                lo, hi = (base, forward) if base < forward else (forward, base)
                if not side.crosses(lo, hi):
                    idx = forward
                    side.add(lo, hi)
                    placed = True
                    break
                trial_jump += 1

        if not placed:
            idx = base
            continue

        arc_count += 1
        visited.add(idx)
        next_free.occupy(idx)

    return idx

def run_sequences(all_sequences, func):
    last_vals = []
    for seq_no, raw_seq in enumerate(all_sequences):
        seq_nums = list(map(int, raw_seq.split(",")))
        final_val = func(seq_nums)
        last_vals.append(final_val)
        # print(seq_no, final_val, sum(last_vals))
    return last_vals

print("The Digital Atelier, Quest 01")
print("Part 1:", sum(run_sequences(input_data_p1, recaman_basic)))
print("Part 2:", sum(run_sequences(input_data_p2, recaman_fwd)))
print("Part 3:", sum(run_sequences(input_data_p3, recaman_full)))


