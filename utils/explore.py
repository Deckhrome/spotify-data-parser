import pandas as pd

try:
    df = pd.read_csv('../data/full_table_27_aug.csv', sep='\t', encoding='utf-8')
    print(df.info())
except Exception as e:
    print(f"Erreur lors de la lecture du fichier : {e}")

# count distinct values in a column
for key in df.keys():
    print(f"{key} : {df[key].nunique()}")

# Count unique values for each track_name and print them when the count is greater than 1
track_name_count = df['sp_track_name'].value_counts()
track_name_count = track_name_count[track_name_count > 1]
print(track_name_count)
