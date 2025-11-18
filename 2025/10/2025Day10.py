"""Everybody Codes - Quest 10, Year 2025
Solution Started: November 15, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/10
Solution by: Abbas Moosajee
Brief: [Feast on the Board]"""

#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
from collections import defaultdict, deque
import time
start_time = time.time()

# List of input file names
input_files = ["Day10_input_p1.txt", "Day10_input_p2.txt", "Day10_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class DragonChess:
    dragon_moves = [
        (-1, -2), (-1, 2), (-2, -1), (-2, 1),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

    def __init__(self, init_chessboard):
        self.seen = {}
        self.board = self.parse_chessboard(init_chessboard)
        self.max_r = max(r for (r, _) in self.board.keys())

    def parse_chessboard(self, init_chessboard):
        board_dict = defaultdict(tuple)
        self.dragon_pos = (0, 0)
        self.all_sheep = set()
        for row_no, row_data in enumerate(init_chessboard):
            for col_no, cell in enumerate(row_data):
                pos = (row_no, col_no)
                if cell == "D":
                    self.dragon_pos = pos
                if cell == "S":
                    self.all_sheep.add(pos)
                board_dict[pos] = cell
        return board_dict

    def count_sheep(self, max_moves):
        init_pos = self.dragon_pos
        queue = deque([(init_pos, 0)])
        visited = set([init_pos])        # Only track positions, NOT (pos, moves)
        sheep_found = set()

        while queue:
            (row, col), moves = queue.popleft()
            if moves >= max_moves:
                continue

            for dr, dc in self.dragon_moves:
                nr, nc = row + dr, col + dc
                new_pos = (nr, nc)

                if new_pos not in self.board:
                    continue

                if new_pos in visited:
                    continue
                visited.add(new_pos)

                # Count sheep once
                if self.board[new_pos] == "S" and new_pos not in sheep_found:
                    sheep_found.add(new_pos)
                queue.append((new_pos, moves + 1))
        return len(sheep_found)

    def eat_sheeps(self, start: tuple, moves: int) -> set:
        """Return all sheep positions reachable by the dragon within `moves` knight-moves."""
        r, c = start

        if moves == 1:
            return {
                (r + dr, c + dc)
                for dr, dc in self.dragon_moves
                if (r + dr, c + dc) in self.all_sheep
            }

        found = set()
        for dr, dc in self.dragon_moves:
            nr, nc = r + dr, c + dc
            if (nr, nc) in self.all_sheep:
                found.add((nr, nc))
            found |= self.eat_sheeps((nr, nc), moves - 1)

        return found

    def can_be_eaten(self, sheep: tuple, rounds: int) -> bool:
        """Check if a sheep that moves downward each round can be eaten."""
        r, c = sheep

        for i in range(rounds):
            # Sheep is at (r+i, c) in round i
            pos_now = (r + i, c)
            pos_next = (r + i + 1, c)

            # Dragon reaches current sheep position
            if self.board.get(pos_now) != '#':
                if pos_now in self.dragons.get(i, ()) or pos_now in self.dragons.get(i + 1, ()):
                    return True

            # Dragon reaches next sheep position (after sheep moves)
            if self.board.get(pos_next) != '#':
                if pos_next in self.dragons.get(i + 1, ()):
                    return True
        return False

    def catch_moving_sheep(self, max_moves: int) -> int:
        """Simulate all dragon positions up to `max_moves` rounds and count how many sheep get eaten."""
        self.dragons = {0: {self.dragon_pos}}

        for i in range(max_moves):
            next_positions = set()
            for r, c in self.dragons[i]:
                for dr, dc in self.dragon_moves:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in self.board:
                        next_positions.add((nr, nc))
            self.dragons[i + 1] = next_positions

        return sum(self.can_be_eaten(sheep, max_moves) for sheep in self.all_sheep)

    def tournament(self, position: tuple, sheeps: set, is_sheep_turn: bool = True) -> int:
        if not sheeps:
            return 1
        key = (position, tuple(sheeps), is_sheep_turn)
        if key in self.seen:
            return self.seen[key]

        res = 0
        if is_sheep_turn:
            sheep_moved = False
            for sheep in sheeps:
                sr, sc = sheep
                if sr == self.max_r:
                    sheep_moved = True
                    continue
                if (sr + 1, sc) != position or self.board[(sr + 1, sc)] == '#':
                    new_sheeps = (sheeps - {sheep}) | {(sr + 1, sc)}
                    sheep_moved = True
                    res += self.tournament(position, new_sheeps, False)
            if not sheep_moved:
                res += self.tournament(position, sheeps, False)
        else:
            pr, pc = position
            for dr, dc in self.dragon_moves:
                new_position = (pr + dr, pc + dc)
                if new_position in self.board.keys():
                    if self.board[new_position] != "#":
                        new_sheeps = sheeps - {new_position}
                        res += self.tournament(new_position, new_sheeps, True)
                    else:
                        res += self.tournament(new_position, sheeps, True)
        self.seen[key] = res
        return res

chess_p1 = DragonChess(input_data_p1)
sheep_p1 = chess_p1.count_sheep(4)
print("Quest 10, P1:", sheep_p1)

chess_p2 = DragonChess(input_data_p2)
sheep_p2 = chess_p2.catch_moving_sheep(20)
print("Quest 10, P2:", sheep_p2)

chess_p3 = DragonChess(input_data_p3)
sheep_p3 = chess_p3.tournament(chess_p3.dragon_pos, chess_p3.all_sheep)
print("Quest 10, P3:", sheep_p3)

print(f"Execution Time: {time.time() - start_time:5f}s")