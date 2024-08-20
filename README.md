# Spotify Data Parser

The **Spotify Data Parser** is a utility designed to process and structure Spotify track data from CSV files into a JSON format.

## Features

- **Data Parsing:** Extracts and organizes track data from CSV files.
- **Data Cleaning:** Cleans and transforms raw data for consistency and usability.
- **Hierarchy Building:** Constructs hierarchical relationships and integrates them into the dataset.
- **JSON Output:** Outputs the structured data in JSON format for easy integration with other tools and applications.

## Project Structure

- **`main.py`**: The entry point of the application.
  - **Purpose**: Reads the input CSV file, processes the data, builds hierarchies stored in `hierarchies.json`, and outputs a structured JSON file.

- **`parse_data.py`**: Handles the core functionality of parsing data from the CSV file, managing tags, and organizing media.

- **`clean_CSV.py`**: Contains functions dedicated to cleaning and transforming the raw CSV data, ensuring it meets the required format for processing.

- **`ClassManager.py`**: Manages the relationships between tags, tagsets, and media, ensuring data is correctly structured and accessible.

- **`hierarchies.py`**: Defines and manages hierarchical structures, integrating them into the `ClassManager` to enhance data organization.

## Requirements

- **Python**: Version 3.8 or higher.
- **Pandas**: A Python library used for data manipulation and analysis.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/Deckhrome/spotify-data-parser.git
   cd spotify-data-parser
   ```

2. **Navigate to the Scripts Directory**:
   ```sh
   cd scripts
   ```

3. **Run the Main Script**:
   ```sh
   python3 main.py <path_to_csv_file> <output_directory> <hierarchy_file> <optional_output_name>
   ```

   Replace `<path_to_csv_file>`, `<output_directory>`, `<hierarchy_file>`, and `<optional_output_name>` with your actual file paths and desired output name.

## Usage

The main script (`main.py`) requires at least three arguments:

1. **CSV File Path**: The path to the CSV file containing Spotify track data.
2. **Output Directory**: The directory where the resulting JSON file will be saved.
3. **Hierarchy File Path**: The path to the `hierarchies.json` file that defines the hierarchical structure.
4. **Optional Output Name**: (Optional) The name of the output JSON file (default is `data.json`).

Example command:

```sh
python3 main.py ../data/csv_file/sample_table_aug.csv ../build/ ../data/hierarchies.json sample_data
```

This will output the processed data as `sample_data.json` in the specified output directory.