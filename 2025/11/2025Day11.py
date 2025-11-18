"""Everybody Codes - Quest 11, Year 2025
Solution Started: November 17, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/11
Solution by: Abbas Moosajee
Brief: [The Scout Duck Protocol]"""

#!/usr/bin/env python3
from pathlib import Path
import time
start_time = time.time()
# List of input file names
input_files = ["Day11_input_p1.txt", "Day11_input_p2.txt", "Day11_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]


class Ducks:
    def __init__(self, init_ducks):
        self.ducks = {
            idx: int(duck_count)
            for idx, duck_count in enumerate(init_ducks, start = 1)
        }

    @staticmethod
    def calculate_flocksum(ducks_dict):
        return sum(idx * duck_count for idx, duck_count in ducks_dict.items())

    def first_phase(self, ducks_dict):
        ducks_moved = False
        for col_idx in range(1, len(ducks_dict)):
            next_idx  = col_idx + 1
            col_ducks, next_ducks = ducks_dict[col_idx], ducks_dict[next_idx]
            if next_ducks < col_ducks:
                ducks_moved = True
                ducks_dict[col_idx] -= 1
                ducks_dict[next_idx] += 1
        return ducks_dict, ducks_moved

    def second_phase(self, ducks_dict):
        ducks_moved = False
        for col_idx in range(1, len(ducks_dict)):
            next_idx = col_idx + 1
            col_ducks, next_ducks = ducks_dict[col_idx], ducks_dict[next_idx]

            if next_ducks > col_ducks:
                ducks_moved = True
                ducks_dict[col_idx] += 1
                ducks_dict[next_idx] -= 1

        return ducks_dict, ducks_moved

    def simulate_rounds(self, total_rounds = 10):
        first_phase, second_phase = True, False
        use_ducks = self.ducks.copy()
        for round in range(1, total_rounds + 1):
            if first_phase:
                use_ducks, ducks_moved = self.first_phase(use_ducks)
                # print("first", round, use_ducks.values(), self.calculate_flocksum(use_ducks))
                if not ducks_moved:
                    first_phase = False
                    second_phase = True
            if second_phase:
                use_ducks, ducks_moved = self.second_phase(use_ducks)
                # print("second", round, use_ducks.values(), self.calculate_flocksum(use_ducks))
        return self.calculate_flocksum(use_ducks)

    def balance_flock(self, slow_solve = False):
        first_phase, second_phase, round = True, False, 0
        use_ducks = self.ducks.copy()
        while True:
            if first_phase:
                use_ducks, ducks_moved = self.first_phase(use_ducks)
                # print("first", round, use_ducks.values(), self.calculate_flocksum(use_ducks))
                if not ducks_moved:
                    first_phase = False
                    second_phase = True
            if second_phase:
                if slow_solve:
                    use_ducks, ducks_moved = self.second_phase(use_ducks)
                    # print("second", round, use_ducks.values(), self.calculate_flocksum(use_ducks))
                    if not ducks_moved:
                        break
                else:
                    second_rounds = self.ascend_solve(use_ducks.values())
                    round += second_rounds
                    break
            round += 1
        return round

    def ascend_solve(self, use_ducks = None):
        all_ducks = use_ducks or self.ducks.values()
        target_val = sum(all_ducks) // len(all_ducks)
        return sum(abs(target_val - duck) for duck in all_ducks) // 2

ducks_p1 = Ducks(input_data_p1).simulate_rounds()
print("Quest 11, P1:", ducks_p1)

ducks_p2 = Ducks(input_data_p2).balance_flock(False)
print("Quest 11, P2:", ducks_p2)

ducks_p3 = Ducks(input_data_p3).ascend_solve()
print("Quest 11, P3:", ducks_p3)
# print(f"Execution Time: {time.time() - start_time:5f}s")