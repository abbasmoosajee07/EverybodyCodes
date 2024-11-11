# Everybody Codes - 2024
# # Solved in {Year_Solve}
# Puzzle Link: https://everybody.codes/event/2024/quests
# Solution by: [abbasmoosajee07]
# Brief: [Run all 2024 scripts]

#!/usr/bin/env python3
import os, subprocess, glob, time

def run_script(file_path):
    """Run a script based on its file extension and time its execution."""
    _, extension = os.path.splitext(file_path)
    
    try:
        # Ignore .txt files (such as input files)
        if extension == '.txt':
            return
        
        # Print the file name (not the full path) before running
        file_name = os.path.basename(file_path)
        print(f"\n Running script: {file_name}")
        
        # Record start time
        start_time = time.time()

        if extension == '.py':
            # Run Python scripts
            subprocess.run(['python', file_path], check=True)
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

def main():
    # Record the start time of the entire process
    total_start_time = time.time()
    
    # Define the base directory to the '2018' folder specifically
    base_dir = os.path.join(os.getcwd(), '2024')
    
    if not os.path.isdir(base_dir):
        print(f"Directory '{base_dir}' does not exist.")
        return
    
    # Traverse only the 'Day' subdirectories within '2018'
    for day_dir in os.listdir(base_dir):
        day_path = os.path.join(base_dir, day_dir)
        
        if os.path.isdir(day_path) and day_dir.isdigit():
            # Find all Python, Ruby, and C files in the day directory
            for script_file in glob.glob(f"{day_path}/*"):
                run_script(script_file)
    
    # Calculate total elapsed time for the entire process
    total_elapsed_time = time.time() - total_start_time
    print(f"\nTotal time to execute all scripts: {total_elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
