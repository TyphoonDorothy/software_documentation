import sys
import os
import csv

# --- PATH RESOLUTION MAGIC ---
# 1. Find exactly where this script lives (the 'scripts' folder)
script_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Go up one level to find the project root (the 'lab2' folder)
project_root = os.path.dirname(script_dir)
# 3. Tell Python to look in 'lab2' when trying to import modules
sys.path.insert(0, project_root)

# Now Python can successfully find the 'business' folder!
from business.strategies import get_output_strategy

def read_dataset(file_path: str) -> list[dict]:
    """Reads the CSV file and returns a list of dictionaries."""
    data = []
    with open(file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def main():
    # Construct absolute paths so it never fails to find the files
    dataset_path = os.path.join(project_root, 'data', 'air_quality.csv')
    config_path = os.path.join(project_root, 'config.json')

    raw_data = read_dataset(dataset_path)

    # Get the strategy based on config.json
    output_strategy = get_output_strategy(config_path)

    # Execute the strategy
    output_strategy.write_data(raw_data)

if __name__ == "__main__":
    main()