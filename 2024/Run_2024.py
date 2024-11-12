# Everybody Codes - 2024
# # Solved in {2024}
# Puzzle Link: https://everybody.codes/event/2024/quests
# Solution by: [abbasmoosajee07]
# Brief: [Run all 2024 scripts]

#!/usr/bin/env python3
import os, subprocess, glob, time, sys
import matplotlib.pyplot as plt

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
    """Parse the input string for days (e.g., '1,2,3' or '1-5')."""
    days_to_run = []

    # Split by commas for cases like "1,2,3"
    for part in days_input.split(','):
        # Handle range (e.g., "1-5")
        if '-' in part:
            try:
                start, end = part.split('-')
                days_to_run.extend(range(int(start), int(end) + 1))
            except ValueError:
                print(f"Error: Invalid range format '{part}'")
                continue
        else:
            try:
                # Handle single day input (e.g., "5")
                days_to_run.append(int(part))
            except ValueError:
                print(f"Error: Invalid day format '{part}'")
                continue

    return days_to_run

def main(Year):
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
    base_dir = os.path.abspath(os.path.join(os.getcwd(), f"{Year}"))
    # os.path.join(os.path.dirname(os.path.abspath(__file__)), D7_file)
    if not os.path.isdir(base_dir):
        print(f"Directory '{base_dir}' does not exist.")
        return
    
    # Dictionary to track time for each day
    times_taken = {}

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
                # Track the start time for this day
                day_start_time = time.time()

                # Find all Python, Ruby, and C files in the padded day directory
                for script_file in glob.glob(f"{day_path}/*"):
                    if padded_day_dir in script_file:  # Only run files that match the padded day
                        run_script(script_file)

                # Calculate the time taken for this day and store it
                day_elapsed_time = time.time() - day_start_time
                times_taken[day_number] = day_elapsed_time

    # Calculate total elapsed time for the entire process
    total_elapsed_time = time.time() - total_start_time
    print(f"\nTotal time to execute specified scripts: {total_elapsed_time:.2f} seconds.")

    # Create a graph to visualize the time taken for each day
    if times_taken:
        days = list(times_taken.keys())
        times = list(times_taken.values())

        # Calculate percentage for each day's time
        percentages = [(time / total_elapsed_time) * 100 for time in times]

        # Plot the time taken for each day
        plt.figure(figsize=(10, 7))
        bars = plt.bar(days, times, color='#FFD700')

        # Add percentage labels on top of each bar
        # Add percentage labels on top of each bar
        for bar, percentage in zip(bars, percentages):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, 
                    f'{percentage:.2f}%', ha='center', va='bottom', fontsize=10)

        # Set plot labels and title
        plt.xlabel('Day')
        plt.ylabel('Time Taken (seconds)')
        plt.title(f'Everybody Codes Year {Year}: Total Time is {total_elapsed_time:.2f} seconds')
        plt.xticks(days)
        plt.tight_layout()

        # Define the path for saving the plot
        script_dir = os.path.dirname(os.path.abspath(__file__))
        plot_path = os.path.join(script_dir, f"{Year}_RunTime_plot.png")

        # Save the plot to the specified path before displaying
        plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)

        # Display the plot
        plt.show()

if __name__ == "__main__":
    Year = 2024
    main(Year)