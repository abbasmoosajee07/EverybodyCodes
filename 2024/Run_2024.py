# Everybody Codes - 2024
# # Solved in {Year_Solve}
# Puzzle Link: https://everybody.codes/event/2024/quests
# Solution by: [abbasmoosajee07]
# Brief: [Run all 2024 scripts]

#!/usr/bin/env python3
import os, subprocess, glob, time, sys

def run_script(file_path):
    """Run a script based on its file extension and time its execution."""
    _, extension = os.path.splitext(file_path)
    
    try:
        # Ignore .txt files (such as input files) and .png images
        if extension == '.txt' or extension == '.png':
            return
        
        # Print the file name (not the full path) before running
        file_name = os.path.basename(file_path)
        print(f"\nRunning script: {file_name}")
        
        # Record start time
        start_time = time.time()

        if extension == '.py':
            # Run Python scripts with SUPPRESS_PLOT environment variable
            subprocess.run(['python', file_path], check=True, env={**os.environ, "SUPPRESS_PLOT": "1"})
        elif extension == '.c':
            # Compile and run C files
            executable = file_path.replace('.c', '')
            subprocess.run(['gcc', file_path, '-o', executable], check=True)
            subprocess.run([executable], check=True)
        elif extension == '.rb':
            # Run Ruby scripts
            subprocess.run(['ruby', file_path], check=True)
        else:
            print(f"Unsupported file type for {file_path}. Skipping.")

        # Calculate elapsed time for this script
        elapsed_time = time.time() - start_time
        print(f"Finished running {file_name} in {elapsed_time:.2f} seconds.")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {file_path}: {e}")

def parse_days_input(days_input):
    """Parse the input for days range or specific days."""
    days = []
    if ',' in days_input:
        # Handle specific days (e.g., "1,3,13")
        days = [int(day) for day in days_input.split(',')]
    elif '-' in days_input:
        # Handle range (e.g., "1-10")
        start, end = days_input.split('-')
        days = list(range(int(start), int(end) + 1))
    else:
        # Single day (e.g., "5")
        days = [int(days_input)]
    
    return sorted(set(days))  # Return a sorted unique list of days

def main():
    # Record the start time of the entire process
    total_start_time = time.time()

    # Argument handling for the day range
    if len(sys.argv) < 2:
        print("No specific days provided. Running scripts for all days.")
        days_to_run = range(1, 26)  # Assume there are 25 days (1-25)
    else:
        days_input = sys.argv[1]  # Get the input for days
        days_to_run = parse_days_input(days_input)
    
    print(f"Running scripts for days: {days_to_run}")

    # Define the base directory to the Year folder specifically
    base_dir = os.path.join(os.getcwd(), '2024')
    
    if not os.path.isdir(base_dir):
        print(f"Directory '{base_dir}' does not exist.")
        return
    
    # Traverse only the 'Day' subdirectories within specific Year
    for day_dir in os.listdir(base_dir):
        day_path = os.path.join(base_dir, day_dir)
        
        # Check if the directory name is a digit (Day folder)
        if os.path.isdir(day_path) and day_dir.isdigit():
            # Add zero padding to the Day part of the filename
            padded_day_dir = day_dir.zfill(2)  # Pads day numbers to two digits (e.g., '01', '02')
            
            # Run the script if this day is in the specified range or list
            day_number = int(day_dir)
            if day_number in days_to_run:
                # Find all Python, Ruby, and C files in the padded day directory
                for script_file in glob.glob(f"{day_path}/*"):
                    if padded_day_dir in script_file:  # Only run files that match the padded day
                        run_script(script_file)

    # Calculate total elapsed time for the entire process
    total_elapsed_time = time.time() - total_start_time
    print(f"\nTotal time to execute specified scripts: {total_elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
