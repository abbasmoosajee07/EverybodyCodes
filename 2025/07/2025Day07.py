"""Everybody Codes - Quest 7, Year 2025
Solution Started: November 12, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/7
Solution by: Abbas Moosajee
Brief: [Namegraph]"""

#!/usr/bin/env python3
from pathlib import Path
import time
start_time = time.time()
# List of input file names
input_files = ["Day07_input_p1.txt", "Day07_input_p2.txt", "Day07_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n\n')
    for file in input_files
]

class NameChecker:
    def __init__(self, names, rules):
        self.name_list = names.split(",")
        self.rules_dict = self.parse_rules(rules)

    def parse_rules(self, init_rules):
        rules_dict = {}
        for rule in init_rules.split("\n"):
            key, greater = rule.split(">")
            greater = greater.strip().split(",")
            rules_dict[key.strip()] = tuple(greater)
        return rules_dict

    def validate_name(self, name):
        for i, (a, b) in enumerate(zip(name, name[1:])):
            valid_chars = self.rules_dict[a]
            if b not in valid_chars:
                return False
        return True

    def check_all_names(self):
        valid_names = {}
        for idx, name in enumerate(self.name_list[:], start = 1):
            name_validity = self.validate_name(name)
            if name_validity:
                valid_names[idx] = name
        return valid_names

    def extend_names(self, init_prefix):
        final_names = set()
        queue = [init_prefix]
        while queue:
            base_name = queue.pop()
            name_len = len(base_name)
            if name_len > self.max_len:
                continue
            if name_len >= self.min_len:
                final_names.add(base_name)
            last_letter = base_name[-1]
            next_letters = self.rules_dict.get(last_letter, [])
            for next in next_letters:
                queue.append(base_name + next)
        return final_names

    def build_all_names(self, min_len, max_len):
        self.min_len = min_len
        self.max_len = max_len
        possibilities = set()
        for prefix in self.name_list:
            if not self.validate_name(prefix):
                continue
            prefix_extensions = self.extend_names(prefix)
            possibilities.update(prefix_extensions)
        return possibilities

valid_names_p1 = NameChecker(input_data_p1[0], input_data_p1[1]).check_all_names()
print("Quest 07, P1:", list(valid_names_p1.values())[0])

valid_names_p2 = NameChecker(input_data_p2[0], input_data_p2[1]).check_all_names()
print("Quest 07, P2:", sum(valid_names_p2.keys()))

valid_names_p3 = NameChecker(input_data_p3[0], input_data_p3[1])
possible_names = valid_names_p3.build_all_names(7, 11)
print("Quest 07, P3:", len(possible_names))

print(f"Execution Time: {time.time() - start_time:5f}s")