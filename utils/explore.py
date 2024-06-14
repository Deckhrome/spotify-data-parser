import pandas as pd

try:
    df = pd.read_csv('../data/full_table_27_aug.csv', sep='\t', encoding='utf-8')
    print(df.info())
except Exception as e:
    print(f"Erreur lors de la lecture du fichier : {e}")

# Compter les occurrences de chaque genre
genre_1_counts = df['genre_1'].value_counts()

# Calculer le nombre total d'occurrences pour chaque genre
total_genre_1 = genre_1_counts.sum()

print(f"Total genre_1: {total_genre_1}")

# Write the first 50 best genres
write_file = open("distinct_genres.txt", "w")

for genre, count in genre_1_counts.items():
    write_file.write(f"{genre}: {count}\n")
