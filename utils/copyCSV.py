num_lines = 20000  # Number of lines to copy

with open('../data/csv_file/full_table_aug_clean.csv', 'r', encoding='utf-8') as input_file:
    with open('../data/csv_file/sample_table_aug_clean.csv', 'w', encoding='utf-8') as output_file:
        for _ in range(num_lines):
            line = input_file.readline()
            if not line:
                break  # Stop if there are no more lines to read
            output_file.write(line)

print(f"First {num_lines} lines copied successfully!")

