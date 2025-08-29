"""Everybody Codes - Quest 3, Story Enigmatus
Solution Started: August 28, 2025
Puzzle Link: https://everybody.codes/story/2/quests/3
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]"""

#!/usr/bin/env python3
import re
from pathlib import Path

# List of input file names
input_files = ["Quest03_input_p1.txt", "Quest03_input_p2.txt", "Quest03_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n\n')
    for file in input_files
]

class DieGames:
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    def __init__(self, all_die):
        self.die_info = {}
        self.die_dict = {}
        for info in all_die:
            no, faces, seed = self._parse_info(info)
            self.die_info[no] = {"all_faces":faces, "seed":seed}
            self.die_dict[no] = {"face_i":0, "pulse": seed}

    def _parse_info(self, raw_info):
        dice_no = raw_info.split(":")[0]
        values_match = re.search(r"faces=\[(.*?)\]", raw_info)
        values = list(map(int, values_match.group(1).split(",")))

        # Extract the seed
        seed_match = re.search(r"seed=(\d+)", raw_info)
        seed = int(seed_match.group(1))
        return int(dice_no), values, seed

    def _roll_die(self, die_no, roll_no):
        die_info = self.die_info[die_no]
        die_state = self.die_dict[die_no]
        pulse = die_state["pulse"]
        spin = roll_no * pulse
        spin_to = (die_state["face_i"] + spin) % len(die_info["all_faces"])
        face_val = die_info["all_faces"][spin_to]

        # Update pulses
        pulse_1 = pulse + spin
        pulse_2 = pulse_1 % die_info["seed"]
        pulse_3 = pulse_2 + 1 + roll_no + die_info["seed"]
        new_pulse = pulse_3

        self.die_dict[die_no] = {"face_i": spin_to, "pulse":new_pulse}
        # print(f"{roll_no=} {spin=} {face_val=} {new_pulse=}")

        return face_val

    def collect_points(self, target_points = 10000):
        total_rolls = 0
        total_points = 0
        all_dies = self.die_info.keys()

        while total_points < target_points:
            results = []
            total_rolls += 1
            for die_no in all_dies:
                die_result = self._roll_die(die_no, total_rolls)
                results.append(die_result)
            total_points += sum(results)
            # print(f"roll_no={total_rolls} dice={results} roll_points={sum(results)} {total_points=}")
        return total_rolls

    def run_race(self, race_track):
        turn = 0
        die_playing = list(self.die_info.keys())
        finishing_order = []
        standings = {die_no: 0 for die_no in die_playing}
        while die_playing and turn <= 1_000_000:
            turn += 1
            turn_results = {}
            finished_dice = []
            for dice_idx, dice_no in enumerate(die_playing):
                dice_pos = standings[dice_no]
                standing_on = race_track[dice_pos]
                no_rolled = self._roll_die(dice_no, turn)
                turn_results[dice_no] = no_rolled
                if no_rolled == int(standing_on):
                    if (dice_pos + 1) >= len(race_track):
                        # print(f"{turn}: removed {dice_no} @ {dice_idx}")
                        finishing_order.append(str(dice_no))
                        finished_dice.append(dice_idx)
                    else:
                        standings[dice_no] += 1
            # print(f"{turn}:{standings} {turn_results}")
            for rem_dice in finished_dice:
                del die_playing[rem_dice]
        return ','.join(finishing_order)

    def __build_game_board(self, init_board):
        board_dict = {}
        for row_no, row_data in enumerate(init_board.split("\n")):
            for col_no, col_data in enumerate(row_data):
                board_dict[(row_no, col_no)] = int(col_data)
        return board_dict

    def play_game(self, game_board):
        board_dict = self.__build_game_board(game_board)
        die_playing = list(self.die_info.keys())

        # Init coins + rolls
        coins = {pos: 0 for pos in board_dict.keys()}
        rolls = {d: [] for d in die_playing}

        q = []
        seen = set()
        for (r, c), cell in board_dict.items():
            for d in die_playing:
                if cell == self.die_info[d]["all_faces"][0]:
                    continue
                state = (r, c, d, 0)   # tuple instead of bit-packed int
                q.append(state)
                seen.add(state)

        while q:
            r, c, d, i = q.pop()
            ni = i + 1

            # Ensure we roll the die when needed
            if len(rolls[d]) == i:
                rolls[d].append(self._roll_die(d, ni))

            # Skip if mismatch
            if board_dict[(r, c)] != rolls[d][i]:
                continue

            coins[(r,c)] = 1

            # Expand neighbors
            for dr, dc in [(0, 0)] + self.DIRECTIONS:  # include staying put
                nr, nc = r + dr, c + dc
                if (nr, nc) in board_dict:  # only expand valid cells
                    state = (nr, nc, d, ni)
                    if state not in seen:
                        q.append(state)
                        seen.add(state)

        return sum(coins.values())

die_p1 = DieGames(input_data_p1[0].split("\n"))
rolls_p1  = die_p1.collect_points()
print("Quest 1:", rolls_p1)

die_p2 = DieGames(input_data_p2[0].split("\n"))
race_p2  = die_p2.run_race(input_data_p2[1])
print("Quest 2:", race_p2)

die_p3 = DieGames(input_data_p3[0].split("\n"))
race_p3  = die_p3.play_game(input_data_p3[1])
print("Quest 3:", race_p3)