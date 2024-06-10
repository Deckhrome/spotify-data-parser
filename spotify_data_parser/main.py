import json
import os
import pandas as pd
from SpotifyDataParser.spotify_data_parser.parse_data import parse_data

# Path to the CSV file
path = os.path.join(os.path.dirname(__file__), '../data/sample_table.csv')

if __name__ == '__main__':
    try:
        # Parse the data into dictionaries
        data = parse_data(path).to_dict()
        
        # Ensure the output directory exists
        output_dir = 'outputfile'
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the data in a JSON file
        with open(os.path.join(output_dir, 'data.json'), 'w') as f:
            json.dump(data, f, indent=4)
        print("Data successfully parsed and saved to outputfile/data.json")
    except Exception as e:
        print(f"An error occurred: {e}")
