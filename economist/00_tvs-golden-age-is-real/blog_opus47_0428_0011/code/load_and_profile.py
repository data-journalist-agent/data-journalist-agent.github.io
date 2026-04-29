"""Load the IMDb/Economist TV ratings dataset and produce a basic profile.

Each row in the source CSV is one season of one TV drama from 1990–2018,
carrying an IMDb weighted average rating, the season's share of total
votes for the show, and a comma-separated list of genres.
"""

import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/economist/00_tvs-golden-age-is-real/IMDb_Economist_tv_ratings.csv"

df = pd.read_csv(DATA)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year

# --- ana_01: Dataset shape and coverage ---
print("=== ana_01 ===")
print(f"rows: {len(df)}")
print(f"columns: {list(df.columns)}")
print(f"unique titleId: {df['titleId'].nunique()}")
print(f"unique title:   {df['title'].nunique()}")
print(f"date min:       {df['date'].min().date()}")
print(f"date max:       {df['date'].max().date()}")
print(f"year span:      {int(df['year'].min())} – {int(df['year'].max())}")
print("missing per column:")
print(df.isna().sum().to_string())

# --- ana_02: Distribution of av_rating ---
print("\n=== ana_02 ===")
r = df["av_rating"]
print(f"av_rating min/max:  {r.min():.3f} / {r.max():.3f}")
print(f"av_rating mean:     {r.mean():.3f}")
print(f"av_rating median:   {r.median():.3f}")
print(f"av_rating std:      {r.std():.3f}")
# Histogram buckets at 0.5 intervals
bins = np.arange(0.0, 10.5, 0.5)
hist = pd.cut(r, bins=bins, include_lowest=True, right=False).value_counts().sort_index()
print("histogram (0.5-wide bins):")
for interval, n in hist.items():
    print(f"  [{interval.left:.1f}, {interval.right:.1f})  {n}")
