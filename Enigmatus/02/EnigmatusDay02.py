"""# Everybody Codes - Day 2, Story Enigmatus
# Solved in Jun, 2025
# Puzzle Link: https://everybody.codes/story/1/quests/2
# Solution by: [abbasmoosajee07]
# Brief: [Tangled Trees]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys
from collections import defaultdict
start_time = time.time()

# List of input file names
input_files = ["Day02_p1_input.txt", "Day02_p2_input.txt", "Day02_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

class SingleTree:
    def __init__(self):
        self.nodes = {}  # Stores node paths and their values
        self.depths = defaultdict(int)  # Tracks depth counts
        self.ids = {}    # Maps IDs to node paths

    def add(self, id_, value, symbol):
        node_path = ''
        while node_path in self.nodes:
            node_value = self.nodes[node_path][0]
            if value < node_value:
                node_path += 'L'
            else:
                node_path += 'R'

        self.nodes[node_path] = (value, symbol)
        self.depths[len(node_path)] += 1
        self.ids[id_] = node_path

    def message(self):
        if not self.depths:
            return ''

        # Find the depth with the most nodes
        max_depth = max(self.depths.values())
        target_depths = [d for d, count in self.depths.items() if count == max_depth]

        # If multiple depths have the same max count, choose the smallest one
        target_depth = min(target_depths)

        # Collect symbols at target depth and sort by path
        symbols = []
        for path, (_, symbol) in self.nodes.items():
            if len(path) == target_depth:
                symbols.append((path, symbol))

        symbols.sort()
        return ''.join(symbol for _, symbol in symbols)

    def message_dict(self):
        """Alternative representation of the message data"""
        message_data = defaultdict(list)
        for path, (value, symbol) in self.nodes.items():
            depth = len(path)
            message_data[depth].append((value, symbol))
        return message_data

class TangledTrees:
    def __init__(self, notes: list[tuple]):
        self.notes_list = notes
        self.command_list = self.parse_input()
        self.left_tree = SingleTree()
        self.right_tree = SingleTree()

    def parse_input(self):
        operations_dict = {}
        pattern = (
            r'(?P<operation>\w+)\s+id=(?P<id>\d+)\s+'
            r'left=\[(?P<left_pos>\d+),(?P<left_val>[^\],]+)\]\s+'
            r'right=\[(?P<right_pos>\d+),(?P<right_val>[^\],]+)\]'
        )
        for line_no, line in enumerate(self.notes_list):
            match = re.match(pattern, line.strip())
            if match:
                line_id = int(match.group('id'))
                oper = match.group('operation')
                line_dict = {
                    'L': (int(match.group('left_pos')), match.group('left_val')),
                    'R': (int(match.group('right_pos')), match.group('right_val'))
                }
                operations_dict[line_no] = (oper, line_id,  line_dict['L'], line_dict['R'])
            elif "SWAP" in line:
                swap, swap_no = line.split(' ')
                operations_dict[line_no] = (swap, int(swap_no))

        return operations_dict

    def build_tree(self):
        for command in self.command_list.values():
            if command[0] == 'ADD':
                _, id_, left, right = command
                self.left_tree.add(id_, left[0], left[1])
                self.right_tree.add(id_, right[0], right[1])
            elif command[0] == 'SWAP':
                _, id_ = command
                self.swap_nodes(id_)
        return {
            'L': self.left_tree.message_dict(),
            'R': self.right_tree.message_dict()
        }

    def swap_nodes(self, id_):
        # Get the node paths from both trees
        left_node = self.left_tree.ids.get(id_)
        right_node = self.right_tree.ids.get(id_)

        if left_node and right_node:
            # Swap the values between the trees
            left_val = self.left_tree.nodes[left_node]
            right_val = self.right_tree.nodes[right_node]

            self.left_tree.nodes[left_node] = right_val
            self.right_tree.nodes[right_node] = left_val

    def find_message(self):
        self.build_tree()
        return self.left_tree.message() + self.right_tree.message()


message_p1 = TangledTrees(input_data_p1).find_message()
print("Quest 1:", message_p1)

message_p2 = TangledTrees(input_data_p2).find_message()
print("Quest 2:", message_p2)

class ConnectedTrees:
    def __init__(self):
        self.nodes = {}
        self.id_map = defaultdict(list)  # Maps ID to node paths

    def add(self, start, id_, value, symbol):
        node = start
        while node in self.nodes:
            node_value = self.nodes[node][1]
            if value < node_value:
                node += 'L'
            else:
                node += 'R'
        self.nodes[node] = [id_, value, symbol]
        self.id_map[id_].append(node)

    def swap(self, id_):
        if id_ not in self.id_map or len(self.id_map[id_]) != 2:
            return

        node1, node2 = self.id_map[id_]

        # Create new mapping with swapped nodes
        new_nodes = {}
        for node, value in self.nodes.items():
            if node.startswith(node1):
                new_node = node2 + node[len(node1):]
            elif node.startswith(node2):
                new_node = node1 + node[len(node2):]
            else:
                new_node = node
            new_nodes[new_node] = value

        # Update id_map for all affected nodes
        self.nodes = new_nodes
        self.id_map = defaultdict(list)
        for node, (id_, _, _) in self.nodes.items():
            self.id_map[id_].append(node)

    def submessage(self, start):
        subtree = {node: value for node, value in self.nodes.items() 
                    if node.startswith(start)}
        if not subtree:
            return ''

        # Find all lengths in the subtree
        lengths = {len(node) for node in subtree}

        # Count nodes at each length and find the length with most nodes
        length_counts = [(length, sum(1 for n in subtree if len(n) == length)) 
                        for length in lengths]
        max_count = max(count for _, count in length_counts)
        target_lengths = [length for length, count in length_counts 
                            if count == max_count]
        target_length = min(target_lengths)  # Prefer shallower depth if tie

        # Collect and sort symbols at target length
        symbols = [(node, value[2]) for node, value in subtree.items() 
                    if len(node) == target_length]
        symbols.sort()
        return ''.join(symbol for _, symbol in symbols)

    def message(self):
        return self.submessage('L') + self.submessage('R')

def build_forest(commands):
    connected_trees = ConnectedTrees()
    for command in commands.values():
        if command[0] == 'ADD':
            _, id_, lvalue, rvalue = command
            connected_trees.add('L', id_, *lvalue)
            connected_trees.add('R', id_, *rvalue)
        elif command[0] == 'SWAP':
            _, id_ = command
            connected_trees.swap(id_)
    return connected_trees.message()

message_p3 = build_forest(TangledTrees(input_data_p3).parse_input())
print("Quest 3:", message_p3)
print(f"Execution Time = {time.time() - start_time:.5f}s")
