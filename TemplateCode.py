# Everybody Codes Challenge
# https://everybody.codes/home
# Create Template Script for Python
# python TemplateCode.py 00 2010 2024 abbasmoosajee07

import os
import sys

# Default values for the arguments
DEFAULT_DAY = 21
DEFAULT_YEAR = 2024
DEFAULT_YEAR_SOLVE = 2024
DEFAULT_AUTHOR = 'abbasmoosajee07'

# Filter out unwanted arguments (e.g., those that come from Jupyter or IDE)
valid_args = [arg for arg in sys.argv if not arg.startswith('--')]

# Check if correct number of arguments are passed
if len(valid_args) < 2:
    print("Using default arguments:")
    print(f"Day: {DEFAULT_DAY}, Year: {DEFAULT_YEAR}, Year_Solve: {DEFAULT_YEAR_SOLVE}, Author: {DEFAULT_AUTHOR}")
    Day = DEFAULT_DAY
    Year = DEFAULT_YEAR
    Year_Solve = DEFAULT_YEAR_SOLVE
    Author = DEFAULT_AUTHOR
else:
    # Retrieve command line arguments, using defaults if any are missing
    Day = int(valid_args[1]) if len(valid_args) > 1 else DEFAULT_DAY
    Year = int(valid_args[2]) if len(valid_args) > 2 else DEFAULT_YEAR
    Year_Solve = int(valid_args[3]) if len(valid_args) > 3 else DEFAULT_YEAR_SOLVE
    Author = valid_args[4] if len(valid_args) > 4 else DEFAULT_AUTHOR

# Add zero padding to the day number for folder and filenames (but not the web link)
padded_day = str(Day).zfill(2)  # Pads day numbers to two digits (e.g., '01', '02')

# Define the path for the new subfolder using the padded day and year variables
base_dir = os.path.join(str(Year), padded_day)

# Check if the subfolder already exists, if not, create it
if not os.path.exists(base_dir):
    os.makedirs(base_dir)
    print(f"Created subfolder '{padded_day}' in '{Year}'.")
else:
    print(f"Subfolder '{padded_day}' already exists in '{Year}'.")

# Define the path for the Python script file
python_file_path = os.path.join(base_dir, f'{Year}Day{padded_day}.py')

# Check if the Python script file already exists
if not os.path.exists(python_file_path):
    # Define the content of the Python script with dynamic day and year
    python_script_content = f'''
# Everybody Codes - Day {Day}, Year {Year}
# Solved in {Year_Solve}
# Puzzle Link: https://everybody.codes/event/{Year}/quests/{Day}
# Solution by: [{Author}]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# List of input file names
input_files = ["Day{padded_day}_p1_input.txt", "Day{padded_day}_p2_input.txt", "Day{padded_day}_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
print(input_data_p1), print(input_data_p2), print(input_data_p3)
'''

    # Write the Python script to the file
    with open(python_file_path, 'w') as file:
        file.write(python_script_content)
    print(f"Created Python script '{Year}Day{padded_day}.py'.")
else:
    print(f"Python script '{Year}Day{padded_day}.py' already exists.")

# Define the paths for the input files
input_file_paths = [
    os.path.join(base_dir, f'Day{padded_day}_p1_input.txt'),
    os.path.join(base_dir, f'Day{padded_day}_p2_input.txt'),
    os.path.join(base_dir, f'Day{padded_day}_p3_input.txt')
]

# Check if the input text files already exist
for i, input_file_path in enumerate(input_file_paths, start=1):
    if not os.path.exists(input_file_path):
        # Create the empty input text file
        with open(input_file_path, 'w') as file:
            pass  # Just create an empty file
        print(f"Created empty input file 'Day{padded_day}_p{i}_input.txt'.")
    else:
        print(f"Input file 'Day{padded_day}_p{i}_input.txt' already exists.")
