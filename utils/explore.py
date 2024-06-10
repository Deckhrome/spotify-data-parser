import pandas as pd

try:
    df = pd.read_csv('sample_table.csv', sep='\t', encoding='utf-8')
    print(df.info())
except Exception as e:
    print(f"Erreur lors de la lecture du fichier : {e}")


missing_genres = df[df[['genre_1', 'genre_2', 'genre_3']].isna().any(axis=1)]

print(missing_genres)