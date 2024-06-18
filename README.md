# Spotify Data Parser

This project provides a utility to parse Spotify track data from a CSV file, clean it, and transform it into a structured JSON format.

## Project Structure

- `main.py`: The entry point for the application. It reads the CSV file, processes the data, and outputs a JSON file.
- `parse_data.py`: Contains functions for parsing data from the CSV file and managing tags and media.
- `clean_CSV.py`: Contains functions for cleaning and transforming the data.
- `ClassManager.py`: Manages the tags, tagsets, and media.
- `hierarchies.py`: Contain every hierarchies and add them to the existing data in the ClassManager

## Requirements

- Python 3.8+
- pandas

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Deckhrome/spotify-data-parser.git
   cd SpotifyDataParser/scripts
   python3 main.py
