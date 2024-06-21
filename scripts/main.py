import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import parse_data, genre_hierarchy, build_hierarchy_json, tagset, ClassManager

full_csv = '../data/full_table_27_aug.csv'
sample_csv = '../data/sample_table.csv'
small_csv = '../data/small_sample.csv'

full_csv_clean = '../data/full_table_27_aug_clean.csv'
sample_csv_clean = '../data/sample_table_clean.csv'
# Path to the CSV file
path = os.path.join(os.path.dirname(__file__), sample_csv_clean)

if __name__ == '__main__':
    try:
        class_manager = ClassManager()
        
        # Build the tagsets into the class manager
        tagset.build_tagset(class_manager)
        # Parse the data into dictionaries
        class_manager = parse_data(path)
        # Build the genre hierarchy into the class manager
        build_hierarchy_json(genre_hierarchy, class_manager) 

        data = class_manager.to_dict()

        # Ensure the output directory exists
        output_dir = '../build'
        os.makedirs(output_dir, exist_ok=True)
        # Save the data in a JSON file
        with open(os.path.join(output_dir, 'full_data.json'), 'w') as f:
            json.dump(data, f, indent=4)
        print("Data successfully parsed and saved to build/data.json")
    except Exception as e:
        print(f"An error occurred: {e}")
