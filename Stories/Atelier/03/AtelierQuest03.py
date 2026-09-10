"""Everybody Codes - Quest 3, Story The Digital Atelier
Solution Started: September 10, 2026
Puzzle Link: https://everybody.codes/story/4/quests/3
Solution by: Abbas Moosajee
Brief: [Hitomezashi Sashiko Floorplan]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
import numpy as np

input_files = ["Quest03_input_p1.txt", "Quest03_input_p2.txt", "Quest03_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class Sashiko_FloorPlan:
    def __init__(self, raw_input):
        for line in raw_input:
            split_line = line.split("=")
            if split_line[0] == "width":
                width = int(split_line[1])
            elif split_line[0] == "height":
                height = int(split_line[1])
            elif "horizontal" in split_line[0]:
                horizontal = split_line[1]
            elif "vertical" in split_line[0]:
                vertical = split_line[1]
        self.width = width
        self.height = height
        self.size = (list(range(1, height + 1)), range(1, width + 1))
        self.offsets = (horizontal, vertical)
        self.floorplan = None
        self.isolated = []
        self.color = {}

    @staticmethod
    def build_foorplan(size):
        floorplan = {}
        for row_no in size[0]:
            for col_no in size[1]:
                floorplan[(row_no, col_no)] = {"T": 0, "B": 0, "R": 0, "L": 0}
        return floorplan

    def fill_boxes(self):
        floorplan = self.build_foorplan(self.size)
        height = self.height
        width = self.width
        horizontal, vertical = self.offsets

        for line_no in range(1, height + 2):
            h_offset = horizontal[(line_no - 1) % len(horizontal)]
            for col_no in self.size[1]:
                col_stitch = (col_no + int(h_offset)) % 2
                top_row = (line_no, col_no)
                bot_row = (line_no - 1, col_no)
                if top_row in floorplan:
                    floorplan[top_row]["T"] = col_stitch
                if bot_row in floorplan:
                    floorplan[bot_row]["B"] = col_stitch

        for line_no in range(1, width + 2):
            v_offset = vertical[(line_no - 1) % len(vertical)]
            for row_no in self.size[0]:
                row_stitch = (row_no + int(v_offset)) % 2
                r_col = (row_no, line_no - 1)
                l_col = (row_no, line_no)
                if r_col in floorplan:
                    floorplan[r_col]["R"] = row_stitch
                if l_col in floorplan:
                    floorplan[l_col]["L"] = row_stitch

        self.floorplan = floorplan

        full_box = 0
        isolated = []
        for coord, box in floorplan.items():
            if sum(box.values()) == 4:
                isolated.append(coord)
                full_box += 1
        self.isolated = isolated
        return full_box

    def two_color(self):
        if self.floorplan is None:
            self.fill_boxes()

        fp = self.floorplan
        height, width = self.height, self.width
        color = {}

        start = (1, 1)
        color[start] = 0
        dq = deque([start])

        while dq:
            r, c = dq.popleft()
            cur = color[(r, c)]
            box = fp[(r, c)]
            neighbors = [
                ((r - 1, c), box["T"]),
                ((r + 1, c), box["B"]),
                ((r, c - 1), box["L"]),
                ((r, c + 1), box["R"]),
            ]
            for (nr, nc), stitch in neighbors:
                if 1 <= nr <= height and 1 <= nc <= width:
                    new_color = cur ^ stitch
                    if (nr, nc) not in color:
                        color[(nr, nc)] = new_color
                        dq.append((nr, nc))
                    # else: already coloured; pattern guarantees consistency

        self.color = color
        return color

    def larger_isolated_group(self):

        if self.floorplan is None:
            self.fill_boxes()
        if not self.color:
            self.two_color()

        group_0 = [t for t in self.isolated if self.color[t] == 0]
        group_1 = [t for t in self.isolated if self.color[t] == 1]

        if len(group_0) >= len(group_1):
            larger_color, larger_group = 0, group_0
            smaller_count = len(group_1)
        else:
            larger_color, larger_group = 1, group_1
            smaller_count = len(group_0)

        return {
            "group_0": group_0,
            "group_1": group_1,
            "larger_group": larger_group,
            "larger_color": larger_color,
            "larger_count": len(larger_group),
            "smaller_count": smaller_count,
        }

class PeriodicSashikoV2:
    def __init__(self, raw_input):
        for line in raw_input:
            split_line = line.split("=")
            if split_line[0] == "width":
                width = int(split_line[1])
            elif split_line[0] == "height":
                height = int(split_line[1])
            elif "horizontal" in split_line[0]:
                horizontal = split_line[1]
            elif "vertical" in split_line[0]:
                vertical = split_line[1]
        self.width = width
        self.height = height
        self.h_digits = np.array([int(ch) for ch in horizontal], dtype=np.uint8)
        self.v_digits = np.array([int(ch) for ch in vertical], dtype=np.uint8)
        self.Lh = len(self.h_digits)
        self.Lv = len(self.v_digits)

    def _build_small(self, h, w):
        """Same vectorized H/V/isolated/color build as before, for a small (h, w)."""
        Lh, Lv = self.Lh, self.Lv
        line_idx_h = np.arange(h + 1, dtype=np.int64) % Lh
        offset_h = self.h_digits[line_idx_h]
        cols_parity = (np.arange(1, w + 1, dtype=np.int64) % 2).astype(np.uint8)
        H = (cols_parity[None, :] ^ offset_h[:, None]).astype(np.uint8)

        line_idx_v = np.arange(w + 1, dtype=np.int64) % Lv
        offset_v = self.v_digits[line_idx_v]
        rows_parity = (np.arange(1, h + 1, dtype=np.int64) % 2).astype(np.uint8)
        V = (rows_parity[:, None] ^ offset_v[None, :]).astype(np.uint8)

        isolated = (H[:-1, :] & H[1:, :] & V[:, :-1] & V[:, 1:]).astype(bool)

        col0_color = np.zeros(h, dtype=np.uint8)
        if h > 1:
            col0_color[1:] = np.cumsum(H[1:h, 0], dtype=np.uint8) % 2
        row_prefix = np.zeros((h, w), dtype=np.uint8)
        if w > 1:
            row_prefix[:, 1:] = np.cumsum(V[:, 1:w], axis=1, dtype=np.uint8) % 2
        color = row_prefix ^ col0_color[:, None]

        return isolated, color

    def count_isolated_groups(self):
        height, width = self.height, self.width
        Lh, Lv = self.Lh, self.Lv

        Pr = 2 * Lh   # row period: always safe, matches reference "th"
        Pc = 2 * Lv   # col period: always safe, matches reference "tw"

        # Build one exact period tile -- but cap at the real grid size in
        # case the grid is smaller than a full period (small-grid edge case).
        build_h = min(height, Pr)
        build_w = min(width, Pc)
        isolated, color = self._build_small(build_h, build_w)

        mask0 = isolated & (color == 0)
        mask1 = isolated & (color == 1)

        def prefix_sum(mask):
            p = np.zeros((mask.shape[0] + 1, mask.shape[1] + 1), dtype=np.int64)
            p[1:, 1:] = mask.astype(np.int64)
            return np.cumsum(np.cumsum(p, axis=0), axis=1)

        pre0 = prefix_sum(mask0)
        pre1 = prefix_sum(mask1)

        full_r, rem_r = divmod(height, Pr) if height >= Pr else (0, height)
        full_c, rem_c = divmod(width, Pc) if width >= Pc else (0, width)
        # when the grid is smaller than one period, build_h/build_w == height/width
        # and full_r/full_c are 0 with rem_r/rem_c == height/width -- consistent.

        def block_total(pre):
            block_full = pre[min(Pr, build_h), min(Pc, build_w)]
            block_partial_c = pre[min(Pr, build_h), rem_c]
            block_partial_r = pre[rem_r, min(Pc, build_w)]
            block_corner = pre[rem_r, rem_c]
            return (
                full_r * full_c * block_full
                + full_r * block_partial_c
                + full_c * block_partial_r
                + block_corner
            )

        count0 = int(block_total(pre0))
        count1 = int(block_total(pre1))
        return {
            "Pr": Pr, "Pc": Pc,
            "group_0": count0,
            "group_1": count1,
            "total_isolated": count0 + count1,
            "larger_count": max(count0, count1),
            "smaller_count": min(count0, count1),
        }

print("The Digital Atelier, Quest 03")
print("Part 1:", Sashiko_FloorPlan(input_data_p1).fill_boxes())
print("Part 2:", Sashiko_FloorPlan(input_data_p2).larger_isolated_group()['larger_count'])
print("Part 3:", PeriodicSashikoV2(input_data_p3).count_isolated_groups()['larger_count'])


