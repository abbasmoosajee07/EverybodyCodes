"""Everybody Codes - Quest 2, Story The Digital Atelier
Solution Started: September 8, 2026
Puzzle Link: https://everybody.codes/story/4/quests/2
Solution by: Abbas Moosajee
Brief: [Sir Sierpiński's Sparkballs]"""

#!/usr/bin/env python3
from pathlib import Path

input_files = ["Quest02_input_p1.txt", "Quest02_input_p2.txt", "Quest02_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class SparkBalls:
    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.sky_dict, self.moves = self.parse_input(raw_input)

    def parse_input(self, raw_input):
        sky_dict = {}
        moves = None
        for line in raw_input:
            key, value = line.strip().split("=", 1)
            if key == "MOVES":
                moves = value
            else:
                sky_dict[key] = tuple(int(n) for n in value.strip("[]").split(","))
        return sky_dict, moves

    @staticmethod
    def calc_light_point(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        nx = min(x1, x2) + int(abs(x1 - x2)/2)
        ny = min(y1, y2) + int(abs(y1 - y2)/2)
        return nx, ny

    @staticmethod
    def find_fireflies(point):
        all_flies = set()
        for dx, dy in [(0,1), (1, 0),(-1,0),(0,-1)]:
            firefly = point[0] + dx, point[1] + dy
            all_flies.add(firefly)
        return all_flies

    def swarm_beetles(self):
        base_coord = self.sky_dict["START"]
        illuminated = {base_coord}
        for move_no, move_to in enumerate(self.moves, start=1):
            move_coord = self.sky_dict[move_to]
            new_coord = self.calc_light_point(base_coord,  move_coord)
            illuminated.add(new_coord)
            # print(base_coord, move_coord, new_coord)
            base_coord = new_coord
        return illuminated

    def swarm_fireflies(self, random = False):
        fireflies = set()
        illuminated = self.swarm_beetles_random() if random else self.swarm_beetles()
        for point in illuminated:
            new_flies = self.find_fireflies(point)
            # print(point, new_flies)
            fireflies.update(new_flies)
        return fireflies - illuminated

    def swarm_beetles_random(self):
        start = self.sky_dict["START"]
        beacons = [coord for key, coord in self.sky_dict.items() if key != "START"]

        illuminated = {start}
        frontier = [start]
        while frontier:
            next_frontier = []
            for point in frontier:
                for beacon in beacons:
                    nxt = self.calc_light_point(point, beacon)
                    if nxt not in illuminated:
                        illuminated.add(nxt)
                        next_frontier.append(nxt)
            frontier = next_frontier
        return illuminated

input_data_p11 = ['START=[5,0]', 'A=[0,0]', 'B=[10,0]', 'C=[5,10]', 'MOVES=ABCCBABCA']

print("The Digitl Atelier, Quest 02")
print("Part 1:", len(SparkBalls(input_data_p1).swarm_beetles()))
print("Part 2:", len(SparkBalls(input_data_p2).swarm_fireflies()))
print("Part 3:", len(SparkBalls(input_data_p3).swarm_fireflies(True)))