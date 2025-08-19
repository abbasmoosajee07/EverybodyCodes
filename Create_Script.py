from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from challenge_utils.ScriptBuilder import ScriptBuilder

# Constants
PROBLEM_NO = 1
CHALLENGE = "Entertainment"
CHOSEN_LANGUAGE = "python"

AUTHOR = "Abbas Moosajee"

CONFIG_DICT = {
    "Entertainment": ("Stories/Entertainment_Hub", "entertainment.json"),
}

def main() -> None:
    """Main function to create challenge files."""

    repo_dir = Path(__file__).parent
    folder, config_file = CONFIG_DICT[CHALLENGE]
    challenge_dir = repo_dir / folder

    try:
        builder = ScriptBuilder(AUTHOR, challenge_dir, config_file)

        filepath = builder.create_files(
            prob_no=PROBLEM_NO,
            language=CHOSEN_LANGUAGE,
            txt_files=3,
        )

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()