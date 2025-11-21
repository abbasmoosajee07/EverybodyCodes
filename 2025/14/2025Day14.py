"""Everybody Codes - Quest 14, Year 2025
Solution Started: November 20, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/14
Solution by: Abbas Moosajee
Brief: [The Game of Light]"""

#!/usr/bin/env python3
from pathlib import Path
import time
start_time = time.time()

# List of input file names
input_files = ["Day14_input_p1.txt", "Day14_input_p2.txt", "Day14_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class Light:
    DIAGONALS = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    def __init__(self, base_board):
        self.h = len(base_board)
        self.w = len(base_board[0])
        self.init_board = {
            (row, col): cell
            for row, row_data in enumerate(base_board)
            for col, cell in enumerate(row_data)
        }

    def print_grid(self, print_board):
        # find max row/col
        rows = max(r for (r, c) in print_board.keys()) + 1
        cols = max(c for (r, c) in print_board.keys()) + 1
        grid = []
        for r in range(rows):
            line = []
            for c in range(cols):
                line.append(str(print_board[(r, c)]))
            grid.append(" ".join(line))
        print("\n".join(grid))

    def count_neighbors(self, board, pos):
        count = 0
        for dr, dc in self.DIAGONALS:
            new_pos = (pos[0] + dr, pos[1] + dc)
            if board.get(new_pos, ".") == '#':
                count += 1
        return count

    def step_grid(self, active_board):
        next_board = {}
        for pos, cell in active_board.items():
            neighbor_count = self.count_neighbors(active_board, pos)
            next_state = '.'
            if cell == "#" and neighbor_count % 2 != 0:
                next_state = '#'
            elif cell == '.'and neighbor_count % 2 == 0:
                next_state = '#'
            next_board[pos] = next_state
        return next_board

    def play_game(self, total_rounds, visualize = False):
        total_count = 0
        active_board = self.init_board.copy()
        for round in range(1, total_rounds + 1):
            active_board = self.step_grid(active_board.copy())
            active_count = self.count_active(active_board)
            total_count += active_count
            if visualize:
                print(f"\nRound: {round} | Active: {active_count}")
                self.print_grid(active_board)
        return total_count

    def identify_pattern(self, rounds, visualize = False):
        seen = {}
        reference = self.init_board.copy()
        full_board_size = (34, 34)
        H, W = max(reference.keys())
        offset = (full_board_size[0] - H) // 2
        base = (offset, offset)

        grid = {
            (row, col): '.'
            for row in range(full_board_size[0])
            for col in range(full_board_size[1])
        }
        total_sum = 0
        round_ = 0

        while round_ < rounds:
            new_g = self.step_grid(grid)

            # loop detection
            if new_g in seen:
                n = seen[new_g]
                if n != 0:
                    raise RuntimeError("Loop found at wrong place")
                loops = rounds // round_
                extra = rounds % round_
                total_sum *= loops
                round_ = round_ * loops
                seen.clear()
            else:
                seen[new_g] = round_

            # matching subgrid
            if new_g.sub_grid_copied(base, reference.dim()) == reference:
                total_sum += new_g.count_true()

            g = new_g
            round_ += 1

        return total_sum

    def count_active(self, board):
        return sum(1 for v in board.values() if v == "#")

    def identify_pattern(self, total_rounds, visualize=False):

        MAX_SIZE = (34, 34)

        # build empty 34×34 base
        def blank_board():
            return {(r, c): "." for r in range(MAX_SIZE[0]) for c in range(MAX_SIZE[1])}

        # compute center offset
        off_r = (MAX_SIZE[0] - self.h) // 2
        off_c = (MAX_SIZE[1] - self.w) // 2

        # build reference board (initial pattern centered)
        ref_board = blank_board()
        for (r, c), v in self.init_board.items():
            ref_board[(off_r + r, off_c + c)] = v

        # convert reference board region into tuple
        def extract_subgrid(B):
            return tuple(
                B[(off_r + r, off_c + c)]
                for r in range(self.h)
                for c in range(self.w)
            )

        ref_pattern = extract_subgrid(ref_board)

        # simulation board
        board = blank_board()

        round_ = 0
        total_sum = 0

        seen = {}
        matches = []

        while round_ < total_rounds:
            if visualize:
                print(f"Current Round: {round_} | Total Count: {total_sum}")

            # step simulation
            board = self.step_grid(board)

            # canonical tuple of whole 34×34 board
            board_tuple = tuple(board[k] for k in sorted(board))

            # cycle detection
            if board_tuple in seen:
                start = seen[board_tuple]
                cycle_len = round_ - start

                remaining = total_rounds - round_
                full_cycles = remaining // cycle_len
                extra = remaining % cycle_len

                cycle_sum = sum(matches[start:])
                total_sum += cycle_sum * full_cycles
                total_sum += sum(matches[start:start+extra])
                if visualize:
                    print("Cycle Detected!!!")
                    print(f"Cycle Len: {cycle_len} | Total Cycles: {full_cycles}")
                return total_sum

            seen[board_tuple] = round_

            # check if subgrid matches initial
            if extract_subgrid(board) == ref_pattern:
                active = self.count_active(board)
                matches.append(active)
                total_sum += active
            else:
                matches.append(0)

            round_ += 1
        return total_sum

game_p1 = Light(input_data_p1)
tiles_p1 = game_p1.play_game(10)
print("Quest 14, P1:", tiles_p1)

game_p2 = Light(input_data_p2)
tiles_p2 = game_p2.play_game(2025)
print("Quest 14, P2:", tiles_p2)

game_p3 = Light(input_data_p3)
tiles_p3 = game_p3.identify_pattern(1_000_000_000)
print("Quest 14, P3:", tiles_p3)

print(f"Execution Time: {time.time() - start_time:5f}s")