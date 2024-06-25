num_lines = 200000

with open('../data/full_table_27_aug.csv', 'r', encoding='utf-8') as input_file:
    with open('../data/sample_table.csv', 'w', encoding='utf-8') as output_file:
        for _ in range(num_lines):
            line = input_file.readline()
            if not line:
                break  # Stop if there are no more lines to read
            output_file.write(line)

print(f"First {num_lines} lines copied successfully!")

