# Use Setup scripts to create a script for any day/ year
import sys, os, time

# Import individual setup functions
from Polyglot_Setups.Setup_C import create_c_script
from Polyglot_Setups.Setup_Julia import create_julia_script
from Polyglot_Setups.Setup_Python import create_python_script
from Polyglot_Setups.Setup_Ruby import create_ruby_script
from Polyglot_Setups.Setup_Txt import create_txt_file

# Define default values for variables within the script
day = 2
folder = "Enigmatus"
author_name = "abbasmoosajee07"

# Define a dictionary for language options
language_script_create_functions = {
    "python": create_python_script,
    "c": create_c_script,
    "julia": create_julia_script,
    "ruby": create_ruby_script,
}

# Define the selected language/script type (change this variable as needed)
selected_language = "python"  # Choose between "python", "c", "julia", "ruby"
repo_dir = os.path.dirname(os.path.abspath(__file__))
def generate_header(day, year, author):
    """
    Generate the header for the script.

    Parameters:
        day (int): The day of the Code challenge.
        year (int): The year of the Code challenge.
        author (str): The name of the author.

    Returns:
        str: The formatted header string.
    """
    # Get current time
    current_time = time.localtime()
    month = time.strftime('%b', current_time)
    solve_year = time.strftime('%Y', current_time)

    # Construct the header content
    header_dict = {
    "Enigmatus": f'''# Everybody Codes - Day {day}, Story {year}
# Solved in {month}, {solve_year}
# Puzzle Link: https://everybody.codes/story/1/quests/{day}
# Solution by: [{author}]
# Brief: [Code/Problem Description]
'''}
    return header_dict[year]

def main():
    """
    Main function to always run the txt setup and then the selected language setup.
    """
    print(f"\nChallenge Code - Day {day}, Year {folder}")
    # Always run the Txt File setup first
    print("\nSelected Txt file setup...")
    for part in range(1, 4):
        create_txt_file(day=day, year=folder, part=part, author=author_name,repo_dir=repo_dir)

    # Map the selected language to the corresponding setup function
    language_create_function = language_script_create_functions.get(selected_language)

    if language_create_function:
        print(f"\nSelected {selected_language.capitalize()} script setup.")

        # Generate header for the selected script
        header = generate_header(day, folder, author_name)

        # Pass the generated header to the language setup function
        language_create_function(day=day, year=folder, author=author_name,
                                    header_text=header, repo_dir = repo_dir)
    else:
        print(f"Error: No setup function found for {selected_language}. Exiting.")
        sys.exit(1)
    print(f"\nCreated all necessary files")

if __name__ == "__main__":
    main()
