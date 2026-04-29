"""Profile the one-hit wonders dataset: structure, coverage, completeness.

Run: python3 code/load_and_profile.py  (from PROJECT_DIR)
Data lives at /Users/forrest/Desktop/data2blog/data_pkg/pudding/54_one-hit-wonders/data.csv
"""

import pandas as pd
from collections import Counter

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/pudding/54_one-hit-wonders/data.csv"

df = pd.read_csv(DATA)

# --- ana_01: Dataset shape and coverage ---
print("=== ana_01 ===")
print(f"rows: {len(df)}")
print(f"columns: {len(df.columns)}")
print(f"unique players: {df['id'].nunique()}")
print(f"year range: {df['year'].min()}-{df['year'].max()}")
print(f"leagues: {sorted(df['league'].unique())}")
print(f"sports: {sorted(df['sport_name'].unique())}")
print()

# --- ana_02: Players and rows per league ---
print("=== ana_02 ===")
by_league = df.groupby('league').agg(
    rows=('id','size'),
    players=('id','nunique'),
    seasons=('year','nunique'),
).reset_index().sort_values('players', ascending=False)
print(by_league.to_string(index=False))
print()

# --- ana_03: Seasons-per-player distribution per league ---
print("=== ana_03 ===")
seasons_per = df.groupby(['league','id']).size().reset_index(name='seasons')
dist = seasons_per.groupby('league')['seasons'].agg(['mean','median','min','max']).round(2)
print(dist)
print()

# --- ana_04: Missingness on key fields ---
print("=== ana_04 ===")
for c in df.columns:
    n_null = df[c].isna().sum()
    if n_null:
        print(f"  {c}: {n_null} null ({100*n_null/len(df):.1f}%)")
print(f"dnp=true rows: {(df['dnp']==True).sum()}")
