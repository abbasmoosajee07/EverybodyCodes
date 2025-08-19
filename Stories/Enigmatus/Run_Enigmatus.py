# Everybody Codes - 2024
# # Solved in {2024}
# Puzzle Link: https://everybody.codes/event/2024/quests
# Solution by: [abbasmoosajee07]
# Brief: [Run all 2024 scripts]

#!/usr/bin/env python3
from pathlib import Path
from challenge_utils.ChallengeBenchmarks import ChallengeBenchmarks

if __name__ == "__main__":

    base_dir = Path.cwd()
    script_dir = Path(__file__).parent.resolve()
    selected_dir = base_dir / "Stories" / "Enigmatus"
    config_file = "enigmatus.json"

    PROBLEMS_TO_RUN = list(range(1, 4))

    analyzer = ChallengeBenchmarks(
        base_dir = selected_dir,
        config_file = config_file,
    )

    results = analyzer.analyze(
        problems_to_run= PROBLEMS_TO_RUN,
        iterations=3,
        save_results=True,
        custom_dir= script_dir / "analysis"
    )

    print("\nAnalysis complete!")
    print(results.head(25))

