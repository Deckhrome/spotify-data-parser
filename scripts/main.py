import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts import parse_data, build_hierarchies, ClassManager

def get_csv_path(filename):
    """Helper function to get the full path of a CSV file."""
    return os.path.join(os.path.dirname(__file__), filename)

def ensure_directory(directory):
    """Ensure the specified directory exists."""
    os.makedirs(directory, exist_ok=True)

def add_extension(filepath, extension):
    """Add an extension to a file path if it doesn't already have one."""
    if not filepath.endswith(extension):
        filepath += extension
    return filepath

def save_json(data, filepath):
    """Save data to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def main(input_csv, output_dir, hierarchy_path, output_name="data"):
    try:
        # Define paths
        output_file = os.path.join(output_dir, add_extension(output_name, ".json"))

        # Initialize ClassManager
        class_manager = ClassManager()

        # Parse data
        class_manager = parse_data(get_csv_path(input_csv))

        # Build hierarchies
        build_hierarchies(class_manager, hierarchy_path)

        # Convert to dictionary
        data = class_manager.to_dict()

        # Ensure output directory exists
        ensure_directory(output_dir)

        # Save data to JSON
        save_json(data, output_file)

        print(f"Data successfully parsed and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    nb_args = len(sys.argv)
    if nb_args not in [4, 5]:
        print("Usage: python main.py <path to your csv file> <output directory> <hierarchy path> [output name]")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_dir = sys.argv[2]
    hierarchy_path = sys.argv[3]
    output_name = sys.argv[4] if nb_args == 5 else "data"

    main(input_csv, output_dir, hierarchy_path, output_name)
