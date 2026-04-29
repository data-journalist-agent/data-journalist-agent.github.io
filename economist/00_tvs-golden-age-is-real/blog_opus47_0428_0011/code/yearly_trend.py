"""Year-by-year trend analysis: mean rating, prestige-tier counts, season volume."""

import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/economist/00_tvs-golden-age-is-real/IMDb_Economist_tv_ratings.csv"

df = pd.read_csv(DATA)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year

# --- ana_03: Yearly mean and median rating, with N seasons ---
print("=== ana_03 ===")
yearly = df.groupby("year").agg(
    n_seasons=("av_rating", "size"),
    mean_rating=("av_rating", "mean"),
    median_rating=("av_rating", "median"),
).reset_index()
yearly["mean_rating"]   = yearly["mean_rating"].round(3)
yearly["median_rating"] = yearly["median_rating"].round(3)
print(yearly.to_string(index=False))

early = df[df["year"].between(1990, 1999)]["av_rating"].mean()
mid   = df[df["year"].between(2000, 2009)]["av_rating"].mean()
late  = df[df["year"].between(2010, 2018)]["av_rating"].mean()
print(f"\nDecade means:")
print(f"  1990–1999: {early:.3f} (n={int((df['year'].between(1990,1999)).sum())})")
print(f"  2000–2009: {mid:.3f} (n={int((df['year'].between(2000,2009)).sum())})")
print(f"  2010–2018: {late:.3f} (n={int((df['year'].between(2010,2018)).sum())})")

# --- ana_04: Count of "prestige-tier" (>=9.0) seasons per year ---
print("\n=== ana_04 ===")
df["prestige"] = df["av_rating"] >= 9.0
prestige = df.groupby("year").agg(
    n_seasons=("av_rating", "size"),
    n_prestige=("prestige", "sum"),
).reset_index()
prestige["pct_prestige"] = (prestige["n_prestige"] / prestige["n_seasons"] * 100).round(2)
print(prestige.to_string(index=False))

# Also count in the >=8.5 "very-good" band
df["very_good"] = df["av_rating"] >= 8.5
vg = df.groupby("year").agg(
    n_seasons=("av_rating", "size"),
    n_very_good=("very_good", "sum"),
).reset_index()
vg["pct_very_good"] = (vg["n_very_good"] / vg["n_seasons"] * 100).round(2)
print("\n--- >=8.5 band ---")
print(vg.to_string(index=False))

# --- ana_05: Volume growth — number of unique seasons per year ---
print("\n=== ana_05 ===")
print(f"Seasons in 1990: {int(yearly[yearly['year']==1990]['n_seasons'].iloc[0])}")
print(f"Seasons in 2000: {int(yearly[yearly['year']==2000]['n_seasons'].iloc[0])}")
print(f"Seasons in 2010: {int(yearly[yearly['year']==2010]['n_seasons'].iloc[0])}")
print(f"Seasons in 2018: {int(yearly[yearly['year']==2018]['n_seasons'].iloc[0])}")
total_pre2000 = int(df[df["year"] < 2000].shape[0])
total_post2010 = int(df[df["year"] >= 2010].shape[0])
print(f"Total seasons before 2000:   {total_pre2000}")
print(f"Total seasons 2010-2018:     {total_post2010}")
print(f"Ratio (post-2010 / pre-2000): {total_post2010/total_pre2000:.2f}")
