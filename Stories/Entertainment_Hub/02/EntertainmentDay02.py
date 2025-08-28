"""Everybody Codes - Quest 2, Story Enigmatus
Solution Started: August 27, 2025
Puzzle Link: https://everybody.codes/story/2/quests/2
Solution by: Abbas Moosajee
Brief: [The Pocket-Money Popper]"""

#!/usr/bin/env python3
from pathlib import Path

# List of input file names
input_files = ["Quest02_input_p1.txt", "Quest02_input_p2.txt", "Quest02_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class PocketPopper:
    FLUFF_BOLTS = ["R", "G", "B"]
    def __init__(self, balloons):
        self.balloons_order = list(balloons)

    def shoot_bolts_linear(self):
        balloons = self.balloons_order.copy()
        bolts_shot = 0
        bolt_idx = 0

        while balloons:
            bolt_color = self.FLUFF_BOLTS[bolt_idx]
            bolt_idx = (bolt_idx + 1) % len(self.FLUFF_BOLTS)
            bolts_shot += 1

            # Pop matching balloons from the front
            while balloons and bolt_color == balloons[0]:
                balloons.pop(0)

            # Pop one non-matching balloon if exists
            if balloons:
                balloons.pop(0)

        return bolts_shot

    def shoot_bolts_circular(self, repeat_count: int = 100):
        balloons = self.balloons_order * repeat_count
        remaining = n = len(balloons)
        popped = [False] * n
        bolts_shot = 0
        bolt_idx = 0
        idx = 0

        while remaining > 0:
            bolts_shot += 1
            bolt_color = self.FLUFF_BOLTS[bolt_idx]
            bolt_idx = (bolt_idx + 1) % len(self.FLUFF_BOLTS)

            # --- record front balloon before popping ---
            while popped[idx]:
                idx += 1

            if (remaining % 2) == 0 and bolt_color == balloons[idx]:
                mid_index = -remaining // 2
                popped[mid_index] = True
                remaining -= 1

            popped[idx] = True
            remaining -= 1

        return bolts_shot

pops_p1 = PocketPopper(input_data_p1[0])
bolts_p1  = pops_p1.shoot_bolts_linear()
print("Quest 1:", bolts_p1)


pops_p21 = PocketPopper(input_data_p2[0])
bolts_p21  = pops_p21.shoot_bolts_circular(100)
print("Quest 2:", bolts_p21)

pops_p3 = PocketPopper(input_data_p3[0])
bolts_p3  = pops_p3.shoot_bolts_circular(100000)
print("Quest 3:", bolts_p3)

