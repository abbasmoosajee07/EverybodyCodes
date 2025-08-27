"""Everybody Codes - Quest 1, Story Enigmatus
Solution Started: August 26, 2025
Puzzle Link: https://everybody.codes/story/2/quests/1
Solution by: Abbas Moosajee
Brief: [Nail Down Your Luck]"""

#!/usr/bin/env python3
import numpy as np
from pathlib import Path
from scipy.optimize import linear_sum_assignment

# List of input file names
input_files = ["Quest01_input_p1.txt", "Quest01_input_p2.txt", "Quest01_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n\n')
    for file in input_files
]

class SlotMachine:
    MOVEMENTS_DICT = {"L": (0, -1), "R": (0, +1)}

    def __init__(self, slot_machine, instructions) -> None:
        self.slot_machine = self.__parse_machine(slot_machine.split("\n"))
        self.solution_manual = {no: rules for no, rules in enumerate(instructions.split("\n"), start= 1)}

    def __parse_machine(self, slot_machine):
        slot_dict = {}
        for row_no, row_data in enumerate(slot_machine, start=1):
            for col_no, cell in enumerate(row_data, start=1):
                slot_dict[(row_no, col_no)] = cell
        self.bounds = max(slot_dict.keys())
        # print("Bounds:", self.bounds)
        return slot_dict

    def _token_movement(self, token_start, chosen_rules):
        token_row, token_col = (1, token_start)
        max_row, max_col = self.bounds
        rule_idx = 0
        while token_row <= max_row:
            token_pos = (token_row, token_col)
            if self.slot_machine[token_pos] == ".":
                token_row += 1
            elif self.slot_machine[token_pos] == "*":
                sel_move = chosen_rules[rule_idx]
                dr, dc = self.MOVEMENTS_DICT[sel_move]
                new_col = token_col + dc
                if sel_move == "R" and new_col > max_col:
                    new_col = token_col - 1
                elif sel_move == "L" and new_col < 1:
                    new_col = token_col + 1
                token_col = new_col
                rule_idx = (rule_idx + 1) % len(chosen_rules)
        return token_col

    def __calc_coins_won(self, final_slot:int, toss_slot: int) -> int:
        return (final_slot * 2) - toss_slot

    def play_slots(self):
        total_coins_won = 0
        for token_slot, token_rules in self.solution_manual.items():
            token_col = self._token_movement((token_slot*2)-1, token_rules)
            coins_won = self.__calc_coins_won((token_col + 1)//2, token_slot)
            total_coins_won += max(coins_won, 0)
        return total_coins_won

    def _find_valid_slots(self, slot_machine):
        valid_slots = [ col
            for (row, col), cell in slot_machine.items()
            if row == 1 and cell == "*"
        ]
        return valid_slots

    def maximize_winnings(self):
        total_coins_won = 0
        valid_slots = self._find_valid_slots(self.slot_machine)
        for token_no, token_rules in self.solution_manual.items():
            max_token_winnings = 0
            for token_slot in valid_slots:
                token_col = self._token_movement(token_slot, token_rules)
                coins_won = self.__calc_coins_won((token_col + 1)//2, (token_slot + 1)//2)
                max_token_winnings = max(max(coins_won, 0), max_token_winnings)
            total_coins_won += max_token_winnings
        return total_coins_won

    def min_max_winnings(self):
        valid_slots = self._find_valid_slots(self.slot_machine)
        slot_tokens_dict = {}
        for token_no, token_rules in self.solution_manual.items():
            token_coins = {}
            for token_slot in valid_slots:
                token_col = self._token_movement(token_slot, token_rules)
                toss_slot = (token_slot + 1)//2
                coins_won = self.__calc_coins_won((token_col + 1)//2, toss_slot)
                token_coins[toss_slot] = max(coins_won, 0)
            slot_tokens_dict[token_no] = token_coins

        # Convert dict → matrix
        matrix = np.array([[slot_tokens_dict[row][col] for col in range(1, len(valid_slots)+1)] for row in range(1, len(slot_tokens_dict)+1)])

        # --- Find minimum assignment ---
        row_ind, col_ind = linear_sum_assignment(matrix)
        min_value = matrix[row_ind, col_ind].sum()

        # --- Find maximum assignment ---
        row_ind_max, col_ind_max = linear_sum_assignment(-matrix)
        max_value = matrix[row_ind_max, col_ind_max].sum()

        return f"{int(min_value)} {int(max_value)}"

slots_p1 = SlotMachine(input_data_p1[0], input_data_p1[1])
coins_p1 = slots_p1.play_slots()
print("Quest 1:", coins_p1)

slots_p2 = SlotMachine(input_data_p2[0], input_data_p2[1])
coins_p2 = slots_p2.maximize_winnings()
print("Quest 2:", coins_p2)

slots_p3 = SlotMachine(input_data_p3[0], input_data_p3[1])
coins_p3 = slots_p3.min_max_winnings()
print("Quest 3:", coins_p3)