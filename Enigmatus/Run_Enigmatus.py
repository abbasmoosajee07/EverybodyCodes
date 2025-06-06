# Everybody Codes - 2024
# # Solved in {2024}
# Puzzle Link: https://everybody.codes/event/2024/quests
# Solution by: [abbasmoosajee07]
# Brief: [Run all 2024 scripts]

#!/usr/bin/env python3
import os
from Benchmarks.execute_challenge import execute_challenge_scripts

if __name__ == "__main__":
    # Define constants
    YEAR = 'Enigmatus'
    CHALLENGE_NAME = 'Everybody Codes Story'
    DAYS_TO_RUN = range(1, 4)
    COLOR_2024 = "#FFFF00"
    NUM_ITERATIONS = 3  # Number of iterations for benchmarking

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.abspath(script_dir)  # Repo directory (same level as script)
    base_dir = os.path.abspath(os.path.join(os.getcwd(), str(YEAR)))
    selected_dir = repo_dir
    # Print repo directory for debugging purposes
    print(f"Repository Directory: {selected_dir}")

    # Execute the challenge scripts
    execute_challenge_scripts(CHALLENGE_NAME, YEAR, DAYS_TO_RUN, selected_dir, NUM_ITERATIONS, COLOR_2024)
