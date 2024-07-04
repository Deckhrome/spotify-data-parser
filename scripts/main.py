import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import parse_data, build_hierarchies, ClassManager

def get_csv_path(filename):
    """ Helper function to get the full path of a CSV file. """
    return os.path.join(os.path.dirname(__file__), filename)

def ensure_directory(directory):
    """ Ensure the specified directory exists. """
    os.makedirs(directory, exist_ok=True)

def save_json(data, filepath):
    """ Save data to a JSON file. """
    with open(filepath, 'w') as f:
        json.dump(data, f)

full_path = '../data/full_table_27_aug.csv'
full_path_clean = '../data/full_table_27_aug_clean.csv'
sample_csv = '../data/sample_table.csv'
sample_csv_clean = '../data/sample_table_clean.csv'

def main():
    try:
        # Define paths
        output_dir = '../build'
        output_file = os.path.join(output_dir, 'full_data.json')

        # Initialize ClassManager
        class_manager = ClassManager()

        # Parse data
        class_manager = parse_data(get_csv_path(full_path))

        # Build hierarchies
        build_hierarchies(class_manager)

        # Convert to dictionary
        data = class_manager.to_dict()

        # Ensure output directory exists
        ensure_directory(output_dir)

        # Save data to JSON
        save_json(data, output_file)

        print(f"Data successfully parsed and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
