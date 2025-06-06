## Setup for Python Script
#!/usr/bin/env python3
import os

def create_python_script(
        day=1, year=2024, author='your name',
        header_text="Test", repo_dir=""):
    """
    Sets up the folder structure, Python script, and input file for a Coding challenge.

    Parameters:
        day (int): The day/problem of the challenge (1-25).
        year (int): The year/level of the challenge.
        author (str): Name of the script author.
        header_text (str): Header text for the Python script.
        repo_dir (str): Base directory for the Challenge Code repository.

    Returns:
        None
    """
    # Zero-pad the day to ensure two-digit formatting (e.g., "01", "12")
    formatted_day = str(day).zfill(2)
    
    # Define the directory structure for the specified year and day
    challenge_dir = os.path.join(repo_dir, str(year), formatted_day)
    
    # Define the filename for the Python script and its full path
    script_filename = f'{year}Day{formatted_day}.py'
    script_filepath = os.path.join(challenge_dir, script_filename)
    
    # Ensure the base directory for the challenge exists
    os.makedirs(challenge_dir, exist_ok=True)

    # Create the Python script if it doesn't already exist
    if not os.path.exists(script_filepath):
        # Template content for the Python script
        script_content = f'''"""{header_text}"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# List of input file names
input_files = ["Day{formatted_day}_p1_input.txt", "Day{formatted_day}_p2_input.txt", "Day{formatted_day}_p3_input.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(os.path.join(os.path.dirname(__file__), file)).read().strip().split('\\n')
    for file in input_files
]

# Now, input_data_p1, input_data_p2, input_data_p3 contain the respective data
print(input_data_p1), print(input_data_p2), print(input_data_p3)
print(f"Execution Time = {{time.time() - start_time:.5f}}s")
'''

        # Write the template content to the Python script file
        with open(script_filepath, 'w') as script_file:
            script_file.write(script_content)

        print(f"Created Python script '{script_filename}'.")
    else:
        print(f"Python script '{script_filename}' already exists.")

    # Display the full path to the Python script
    print(f"Full Path: {script_filepath}")
