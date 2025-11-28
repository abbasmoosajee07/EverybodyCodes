"""Everybody Codes - Quest 18, Year 2025
Solution Started: November 26, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/18
Solution by: Abbas Moosajee
Brief: [When Roots Remember]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
from copy import deepcopy
import time, re
start_time = time.time()

# List of input file names
input_files = ["Day18_input_p1.txt", "Day18_input_p2.txt", "Day18_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

class Plants:
    def __init__(self, plant_data):
        self.parse_data(plant_data)

    def parse_data(self, input_data):
        def find_nums(text):
            return list(map(int, re.findall(r'-?\d+', text)))

        self.root_network = defaultdict(dict)
        self.controllable_plants = []
        self.test_cases = []
        current_plant = 0
        for row_data in input_data:
            if row_data.startswith("Plant "):
                plant_no, thickness = find_nums(row_data)
                current_plant = plant_no
                self.root_network[plant_no] = {"inner": thickness}
            elif row_data.startswith("- free"):
                thickness, = find_nums(row_data)
                self.root_network[current_plant]["free"] = thickness
                self.controllable_plants.append(current_plant)
            elif row_data.startswith("- branch"):
                branch_to, thickness, = find_nums(row_data)
                self.root_network[current_plant][branch_to] = thickness
            elif row_data.startswith("0") or row_data.startswith("1"):
                self.test_cases.append(find_nums(row_data))

    def calculate_brightness(self, test_network=None):
        energy_dict = defaultdict(int)
        if not test_network:
            test_network = self.root_network.copy()
        # Process plants in order (assuming plants are numbered sequentially)
        all_plants = sorted(test_network.keys())
        for plant in all_plants:
            plant_root = test_network[plant]
            if "free" in plant_root.keys():
                inner, free = (plant_root["inner"], plant_root["free"])
                if inner == free:
                    energy_dict[plant] = inner * free
                else:
                    energy_dict[plant] = 0
            else:
                total_energy = 0
                for branch, thickness in plant_root.items():
                    if branch == "inner":
                        continue
                    branch_energy = energy_dict[branch]
                    total_energy += (thickness * branch_energy)
                if total_energy < plant_root["inner"]:
                    total_energy = 0
                energy_dict[plant] = total_energy
        return energy_dict

    def run_case_studies(self):
        results = {}
        og_network = deepcopy(self.root_network)
        for study_no, study in enumerate(self.test_cases):
            test_network = deepcopy(og_network)
            for plant, change in enumerate(study, 1):
                if plant in test_network:
                    test_network[plant]["free"] = change
            study_results = self.calculate_brightness(test_network)
            results[study_no] = study_results[max(study_results.keys())] if study_results else 0
        return results

    def maximise_energy(self):
        all_case_studies = self.run_case_studies()
        changeable_plants = len(self.controllable_plants)
        best = [0] * changeable_plants

        # Build link branches information for optimization
        link_branches = defaultdict(list)
        for plant_id, plant_data in self.root_network.items():
            if "free" not in plant_data:  # Only plants without free branches can be sources
                for target, thickness in plant_data.items():
                    if target != "inner" and thickness > 0:
                        link_branches[plant_id].append((target, thickness))

        # Process link branches to find optimal starting points
        for branches in link_branches.values():
            for source, thickness in branches:
                if thickness > 0 and source in self.controllable_plants:
                    idx = self.controllable_plants.index(source)
                    if idx < changeable_plants:
                        best[idx] = 1

        # Calculate optimal score
        test_network = deepcopy(self.root_network)
        for i, value in enumerate(best):
            if i < len(self.controllable_plants):
                plant_id = self.controllable_plants[i]
                test_network[plant_id]["free"] = value
        energy_dict = self.calculate_brightness(test_network)
        optimal_score = energy_dict[max(energy_dict.keys())]

        return {study_no: (optimal_score - score) for study_no, score in all_case_studies.items() if score > 0}

plants_p1 = Plants(input_data_p1)
brightness = plants_p1.calculate_brightness()
print("Quest 18, P1:", max(brightness.values()))

plants_p2 = Plants(input_data_p2)
case_studies_p2 = plants_p2.run_case_studies()
print("Quest 18, P2:", sum(case_studies_p2.values()))

plants_p3 = Plants(input_data_p3)
case_studies_p3 = plants_p3.maximise_energy()
print("Quest 18, P3:", sum(case_studies_p3.values()))

# print(f"Execution Time: {time.time() - start_time:5f}s")