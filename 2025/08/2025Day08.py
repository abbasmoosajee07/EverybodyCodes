"""Everybody Codes - Quest 8, Year 2025
Solution Started: November 13, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/8
Solution by: Abbas Moosajee
Brief: [The Art of Connection]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
import math
import matplotlib.pyplot as plt

# List of input file names
input_files = ["Day08_input_p1.txt", "Day08_input_p2.txt", "Day08_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n\n')
    for file in input_files
]

class CircleConnections:
    def __init__(self, path_str):
        self.full_path = list(map(int, path_str.split(",")))
        # self.visualize_circle()

    def identify_opposites(self, all_points):
        opposite_points = {}
        unique_points = list(set(all_points))
        total_points = len(unique_points)
        for idx, point in enumerate(unique_points):
            opposite_idx = int((idx + total_points / 2) % total_points)
            opposite_points[point] = unique_points[opposite_idx]
        return opposite_points

    def follow_centre(self):
        opposite_points = self.identify_opposites(self.full_path)
        through_centre = 0
        for a, b in zip(self.full_path, self.full_path[1:]):
            opp_a = opposite_points[a]
            if opp_a == b:
                through_centre += 1
        return through_centre

    def count_knots(self):
        points = self.full_path
        segments = []
        total_knots = 0

        # Build list of all segments (normalize endpoints so a<b)
        for a, b in zip(points, points[1:]):
            if a > b:
                a, b = b, a
            segments.append((a, b))

        # Compare all pairs of segments to count crossings
        for i, (a,b) in enumerate(segments):
            for (c,d) in segments[i+1:]:
                # Normalize second segment too
                if c > d:
                    c, d = d, c
                # Skip if they share an endpoint (no knot at nails)
                if len({a, b, c, d}) < 4:
                    continue
                # Interleave test (crossing)
                if (a < c < b < d) or (c < a < d < b):
                    total_knots += 1
        return total_knots

    def cut_best_string(self):
        points = self.full_path
        n = max(points)
        links = defaultdict(list)

        # Build adjacency for the thread path
        for a, b in zip(points, points[1:]):
            links[a].append(b)
            links[b].append(a)

        best_cuts = 0
        for a in range(1, n + 1):
            cuts = 0
            for b in range(a + 2, n + 1):
                cuts -= sum(1 for c in links[b] if a < c < b - 1)
                cuts += sum(1 for c in links[b - 1] if not a <= c <= b)
                best_cuts = max(best_cuts, cuts + (b in links[a]))
        return best_cuts

    def visualize_circle(self, radius=1.0):
        """Draw nails around a circle and connect them according to the path."""
        n = max(self.full_path)
        pts = []
        for i in range(n):
            theta = 2 * math.pi * i / n
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            pts.append((x, y))

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_aspect('equal')
        ax.axis('off')

        # draw all nails
        xs, ys = zip(*pts)
        ax.scatter(xs, ys, s=20, color='black', zorder=3)

        # draw connecting threads
        for a, b in zip(self.full_path, self.full_path[1:]):
            x1, y1 = pts[a - 1]
            x2, y2 = pts[b - 1]
            ax.plot([x1, x2], [y1, y2], color="#000000", linewidth=0.15, alpha=0.7)

        plt.show()


centre_cuts = CircleConnections(input_data_p1[0]).follow_centre()
print("Quest 08, P1:", centre_cuts)

total_knots = CircleConnections(input_data_p2[0]).count_knots()
print("Quest 08, P2:", total_knots)

best_cut = CircleConnections(input_data_p3[0]).cut_best_string()
print("Quest 08, P3:", best_cut)
