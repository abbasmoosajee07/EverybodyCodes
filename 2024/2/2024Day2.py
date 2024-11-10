# Everybody Codes - Day 2, Year 2024
# Solved in 2024
# Puzzle Link: https://everybody.codes/event/2024/quests/2
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from collections import Counter

# Load the input data from the specified file path
D2_file = "Day2_input.txt"
D2_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D2_file)

# Read and sort input data into a grid
with open(D2_file_path) as file:
    input_data = file.read().strip().split('\n')

    runic_words_p1 = input_data[0].strip('WORDS:').split(',')
    inscription_p1 = input_data[2]

    runic_words_p2 = input_data[4].strip('WORDS:').split(',')
    inscription_p2 = input_data[6:609]

    runic_words_p3 = input_data[610].strip('WORDS:').split(',')
    inscription_p3 = input_data[612:]


runic_count = 0
for word in runic_words_p1:
    # runic_occurrence = count_overlapping_substring(inscription, word)
    if word != '':
        runic_occurrence = inscription_p1.count(word)
        runic_count += runic_occurrence

print(f"Part 1: {runic_count}")

def include_reversed_strings(word_list):
    # Add reversed words to the words list
    for word in word_list:
        reversed_word = word[::-1]
        if reversed_word not in word_list:
            word_list.append(reversed_word)
    return word_list


def find_runes(runic_words, inscription):

    # Initialize the answer
    runic_count = 0
    runic_words = include_reversed_strings(runic_words)

    # Process each line in the text
    for line in inscription:
        # Create a grid of booleans for the line
        line_as_grid = list(line)
        line_as_booleans_grid = [False] * len(line)

        # Search for each word in the line
        for word in runic_words:
            for j in range(len(line_as_grid) - len(word) + 1):  # Avoid going out of bounds
                word_found = True
                # Check if the word exists at position j
                for i in range(len(word)):
                    if word[i] != line_as_grid[j + i]:
                        word_found = False
                        break
                if word_found:
                    # Mark the positions as found in the boolean grid
                    for i in range(len(word)):
                        line_as_booleans_grid[j + i] = True

        # Count the number of true values in the boolean grid
        runic_count += sum(line_as_booleans_grid)
    return runic_count
runic_count_p2 = find_runes(runic_words_p2, inscription_p2)
print("Part 2:", runic_count_p2)

# 4889, correct length, incorrect first digit
# 5651, correct length, correct first digit


"""---------------------Part 3--------------------"""

def isValid(x, y, sizeX, sizeY):
    return 0 <= x < sizeX and 0 <= y < sizeY

def searchWord(grid, word, result_grid):
    ans = []
    n = len(grid)
    m = len(grid[0])

    # Directions for 4 possible movements: up, down, left, right
    directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]

    for i in range(n):
        for j in range(m):
            # Check if the first character matches
            if grid[i][j] == word[0]:
                for dirX, dirY in directions:
                    if findWordInDirection(grid, n, m, word, 0, i, j, dirX, dirY):
                        ans.append([i, j])
                        markWordInGrid(result_grid, grid, word, i, j, dirX, dirY)
                        break

    return ans, result_grid

def findWordInDirection(grid, n, m, word, index, i, j, dirX, dirY):
    # Check if all characters of the word are within the bounds, considering circular rows
    for k in range(len(word)):
        newRow = i + dirX * k
        newCol = (j + dirY * k) % m  # Apply wrap-around only for columns

        # If the new row is out of bounds (for up or down), return False
        if not (0 <= newRow < n):
            return False
        
        # If the character does not match, return False
        if grid[newRow][newCol] != word[k]:
            return False

    # If all characters match, return True
    return True

def markWordInGrid(result_grid, grid, word, startRow, startCol, dirX, dirY):
    # Mark the found word in the result grid
    for k in range(len(word)):
        newRow = startRow + dirX * k
        newCol = (startCol + dirY * k) % len(grid[0])  # Wrap-around for columns

        # Mark the corresponding position in the result grid
        result_grid[newRow][newCol] = word[k]

def count_strings_with_letters(strings):
    # Filter the list to count only non-empty strings that contain at least one letter
    count = 0
    for s in strings:
        if s and any(c.isalpha() for c in s):  # non-empty and contains at least one letter
            count += 1
    return count


runic_words_p3 = include_reversed_strings(runic_words_p3)

# Convert grid and initialize the found grid
grid = [list(row) for row in inscription_p3]
found_grid = np.array([['' for _ in row] for row in inscription_p3])

# Search for each word and mark the found words in the grid
for word in runic_words_p3:
    if word:
        word_found, found_grid = searchWord(grid, word, found_grid)

# Count the occurrences of strings with letters in the found grid
runic_count_p3 = sum(count_strings_with_letters(row) for row in found_grid)

print(f"Part 3: {runic_count_p3}")

