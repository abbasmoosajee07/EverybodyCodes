"""Everybody Codes - Quest 15, Year 2025
Solution Started: November 21, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/15
Solution by: Abbas Moosajee
Brief: [Definitely Not a Maze]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import deque, defaultdict
import time, heapq
start_time = time.time()

# List of input file names
input_files = ["Day15_input_p1.txt", "Day15_input_p2.txt", "Day15_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class NotMaze:
    TURN_DIRECTIONS = {
        "R": {"^": ">", ">":"v", "v":"<", "<":"^"},
        "L": {"^": "<", "<":"v", "v":">", ">":"^"}
    }
    DIRECTIONS = {
        "^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)
    }

    def __init__(self, build_instructions):
        self.instructions = build_instructions[0].split(",")

    def maze_dimensions(self, maze):
        min_rows = min(r for (r, _) in maze.keys())
        min_cols = min(c for (_, c) in maze.keys())
        max_rows = max(r for (r, _) in maze.keys())
        max_cols = max(c for (_, c) in maze.keys())
        return (min_rows, max_rows, min_cols, max_cols)

    def print_maze(self, print_maze, path = []):
        min_rows, max_rows, min_cols,  max_cols = self.maze_dimensions(print_maze)
        grid = []
        for r in range(min_rows, max_rows + 1):
            line = []
            for c in range(min_cols, max_cols + 1):
                cell = print_maze.get((r, c), " ")
                if (r, c) in path and cell not in "SE":
                    cell = "."
                line.append(cell)
            grid.append(" ".join(line))
        print("\n".join(grid))

    def build_maze(self, instructions, start_pos = (0, 0)):
        current_pos, current_dir = (start_pos, "^")
        maze_dict = {current_pos: "S"}
        for instruc in instructions:
            turn_dir, magn = instruc[0], int(instruc[1:])
            next_dir = self.TURN_DIRECTIONS[turn_dir][current_dir]
            dr, dc = self.DIRECTIONS[next_dir]
            for shift in range(1, magn + 1):
                new_pos = (current_pos[0] + (dr * shift), current_pos[1] + (dc * shift))
                maze_dict[new_pos] = "#"
            current_pos, current_dir = (new_pos, next_dir)
        maze_dict[current_pos] = "E"
        return maze_dict

    def bfs_traverse(self, visualize = False):
        start_pos = (0, 0)
        maze_dict = self.build_maze(self.instructions, start_pos)
        min_rows, max_rows, min_cols, max_cols = self.maze_dimensions(maze_dict)
        path_lens = set()

        queue = deque([[start_pos]])
        visited = set([start_pos])   # <-- add this

        while queue:
            current_path = queue.popleft()
            current_pos = current_path[-1]

            if maze_dict.get(current_pos, " ") == "E":
                path_lens.add(len(current_path))
                if visualize:
                    print("Path Len:", len(current_path))
                    self.print_maze(maze_dict, current_path)
                continue

            for dr, dc in self.DIRECTIONS.values():
                new_pos = (current_pos[0] + dr, current_pos[1] + dc)

                if not (min_rows <= new_pos[0] <= max_rows and min_cols <= new_pos[1] <= max_cols):
                    continue

                if maze_dict.get(new_pos, " ") == '#':
                    continue

                if new_pos in visited:
                    continue  # <-- prevent repeat visits

                visited.add(new_pos)
                queue.append(current_path + [new_pos])

        return min(path_lens) - 1


    def build_maze(self, instructions, start_pos = (0, 0)):
        current_pos, current_dir = (start_pos, "^")
        maze_dict = {current_pos: "S"}
        for instruc in instructions:
            turn_dir, magn = instruc[0], int(instruc[1:])
            next_dir = self.TURN_DIRECTIONS[turn_dir][current_dir]
            dr, dc = self.DIRECTIONS[next_dir]
            for shift in range(1, magn + 1):
                new_pos = (current_pos[0] + (dr * shift), current_pos[1] + (dc * shift))
                maze_dict[new_pos] = "#"
            current_pos, current_dir = (new_pos, next_dir)
        maze_dict[current_pos] = "E"
        return maze_dict


    def is_wall(self, rx, ry, segments):
        for (x1, y1, x2, y2) in segments:
            if (min(x1, x2) <= rx <= max(x1, x2) and
                min(y1, y2) <= ry <= max(y1, y2)):
                return True
        return False

    def express_search(self):

        # --- Initial state ---
        x, y = 0, 0
        start_x, start_y = 0, 0
        current_dir = "^"

        segments = []
        interesting = defaultdict(set)
        interesting["x"].add(0)
        interesting["y"].add(0)

        # --- Build segments and gather interesting coordinates ---
        for instr in self.instructions:
            turn = instr[0]
            steps = int(instr[1:])

            # Rotate direction
            current_dir = self.TURN_DIRECTIONS[turn][current_dir]
            dx, dy = self.DIRECTIONS[current_dir]

            next_x = x + dx * steps
            next_y = y + dy * steps

            segments.append((x, y, next_x, next_y))
            x, y = next_x, next_y

            # Add neighbors for compression
            interesting["x"].update({x, x - 1, x + 1})
            interesting["y"].update({y, y - 1, y + 1})

        end_x, end_y = x, y

        # --- Coordinate compression ---
        sorted_x = sorted(interesting["x"])
        sorted_y = sorted(interesting["y"])

        ix_start = sorted_x.index(start_x)
        iy_start = sorted_y.index(start_y)
        ix_end = sorted_x.index(end_x)
        iy_end = sorted_y.index(end_y)

        start = (ix_start, iy_start)
        end = (ix_end, iy_end)

        max_x = len(sorted_x)
        max_y = len(sorted_y)

        # --- Priority queue Dijkstra ---
        pq = [(0, start)]
        visited = {}

        while pq:
            cost, (ix, iy) = heapq.heappop(pq)

            if (ix, iy) == end:
                return cost

            if (ix, iy) in visited and visited[(ix, iy)] <= cost:
                continue
            visited[(ix, iy)] = cost

            # Explore 4-way adjacency
            for dx, dy in self.DIRECTIONS.values():
                nix = ix + dx
                niy = iy + dy

                # Bounds
                if not (0 <= nix < max_x and 0 <= niy < max_y):
                    continue

                real_x = sorted_x[nix]
                real_y = sorted_y[niy]

                safe_node = (
                    (real_x == start_x and real_y == start_y) or
                    (real_x == end_x and real_y == end_y)
                )

                if not safe_node and self.is_wall(real_x, real_y, segments):
                    continue

                # Manhattan distance between compressed coords
                step_cost = abs(real_x - sorted_x[ix]) + abs(real_y - sorted_y[iy])
                new_cost = cost + step_cost

                heapq.heappush(pq, (new_cost, (nix, niy)))

        return "No Path Found"

maze_p1 = NotMaze(input_data_p1)
shortest_p1 = maze_p1.bfs_traverse()
print("Quest 15, P1:", shortest_p1)

maze_p2 = NotMaze(input_data_p2)
shortest_p2 = maze_p2.express_search()
print("Quest 15, P2:", shortest_p2)

maze_p3 = NotMaze(input_data_p3)
shortest_p3 = maze_p3.express_search()
print("Quest 15, P3:", shortest_p3)

print(f"Execution Time: {time.time() - start_time:5f}s")

