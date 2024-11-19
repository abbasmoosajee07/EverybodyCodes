# Everybody Codes - Day 6, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/6  # Web link without padding
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque
from typing import Dict, List

# List of input file names
input_files = ["Day06_p1_input.txt", "Day06_p2_input.txt", "Day06_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# # Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)

def bfs(graph: nx.DiGraph) -> List[str]:
    # Initialize the queue with the start node
    queue, path_lengths = deque([["RR"]]), defaultdict(list)
    
    while queue:
        current_path = queue.popleft()
        current_node = current_path[-1]
        
        # If we reach the destination node "@", store the path
        if current_node == "@":
            path_lengths[len(current_path)].append(current_path)
        
        # Continue if the node is "BUG" or "ANT" or if there are no further neighbors
        if current_node in {"BUG", "ANT"} or current_node not in graph:
            continue
        
        # Traverse the neighbors of the current node
        neighbors = list(graph.neighbors(current_node))
        for neighbor in neighbors:
            queue.append(current_path + [neighbor])

    # Return the first path that is of length 1
    return next(filter(lambda p: len(p) == 1, path_lengths.values())).pop()

def to_graph(lines: List[str]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for line in lines:
        node, children_str = line.strip().split(":")
        children = children_str.split(",")
        for child in children:
            graph.add_edge(node, child)
    return graph

def plot_word_tree(G):
    """Plots the word tree using a spring layout."""
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)  # Use spring layout for better visualization of the directed edges
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=7,
            font_weight="bold", edge_color="gray", arrows=True)
    plt.title("Word Tree of Word Pairs")
    plt.show()

def find_path(input_data, full_path = True):
    graph = to_graph(input_data)
    path = bfs(graph)
    # plot_word_tree(graph)

    if full_path:
        output_path = ''.join(path)
    else:
        first_letter = [node[0] for node in path]
        output_path = ''.join(first_letter)
    return output_path

ans_p1 = find_path(input_data_p1)
print(f"Quest 1: {ans_p1}")

ans_p2 = find_path(input_data_p2, full_path=False)
print(f"Quest 2: {ans_p2}")

ans_p3 = find_path(input_data_p3, full_path=False)
print(f"Quest 3: {ans_p3}")