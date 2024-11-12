# Everybody Codes - Day 6, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/6  # Web link without padding
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# List of input file names
input_files = ["Day06_p1_input.txt", "Day06_p2_input.txt", "Day06_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\n')
    for file in input_files
]

# # Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
# print(input_data_p1), print(input_data_p2), print(input_data_p3)


def create_word_tree(word_pairs):
    """Creates a directed graph representing a word tree from a list of word pairs."""
    G = nx.DiGraph()  # Using a directed graph
    end_node = 0  # Counter for unique end node identifiers
    
    for pair in word_pairs:
        # Split the pair at the colon to separate the first word and the second part
        first_word, second_part = pair.split(":")
        # If the second part is a single word (and not '@'), create a direct edge
        if ',' not in second_part:
            # if second_part != '@':  # If second part is not '@', create the edge normally
            G.add_edge(first_word, second_part)
            # else:
            #     # If second part is '@', create a unique terminal node with a number
            #     end_node += 1
            #     end_point = f'@{end_node}'  # Create a unique identifier for @ (e.g., @1, @2, etc.)
            #     G.add_edge(first_word, end_point)

        # If the second part contains multiple words separated by commas, create edges to all of them
        else:
            second_words = second_part.split(",")
            for word in second_words:
                word = word.strip()  # Remove leading/trailing spaces
                # if word != '@':  # If word is not '@', add a normal edge
                G.add_edge(first_word, word)
                # else:
                #     # If we encounter '@', create a unique terminal node with a number
                #     end_node += 1
                #     end_point = f'@{end_node}'  # Create a unique identifier for @
                #     G.add_edge(first_word, end_point)
    return G  # Return the constructed graph

def plot_word_tree(G):
    """Plots the word tree using a spring layout."""
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)  # Use spring layout for better visualization of the directed edges
    nx.draw(G, pos, with_labels=True, node_size=1200, node_color="skyblue", font_size=12,
            font_weight="bold", edge_color="gray", arrows=True)
    plt.title("Word Tree of Word Pairs")
    plt.show()

# Function to find the shortest branch path from a node
def shortest_branch_path_from_node(G, start_node):
    # Perform BFS to find the paths from the start node to all other nodes
    paths = nx.single_source_shortest_path(G, start_node)
    
    # Find leaf nodes (nodes with only one connection)
    leaf_nodes = [node for node, degree in G.degree() if degree == 1]
    
    # Find the shortest path to any leaf node
    shortest_leaf = min(leaf_nodes, key=lambda node: len(paths[node]))
    
    return paths[shortest_leaf], len(shortest_leaf)


def create_tree(input_data):

    # Create the word tree from pairs
    G = create_word_tree(input_data)

    # # Plot the word tree
    # plot_word_tree(G)

    # Print the length of the word tree (number of edges)
    print("Word Tree Length (edges):", G.size())
    # Find and print the shortest branch

    shortest_path, shortest_length = shortest_branch_path_from_node(G, 'RR')
    ans = ''.join(shortest_path)
    return ans

ans_p1 = create_tree(input_data_p1)
print(f"Part 1: {ans_p1}")

# ans_p2 = create_tree(input_data_p2)
# print(f"Part 2: {ans_p2}")

# ans_p3 = create_tree(input_data_p3)
# print(f"Part 3: {ans_p3}")