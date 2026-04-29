"""Genre-level breakdowns: which genres carry the rise, which lag."""

import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/economist/00_tvs-golden-age-is-real/IMDb_Economist_tv_ratings.csv"

df = pd.read_csv(DATA)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year

# Explode genres
df["genre_list"] = df["genres"].fillna("").str.split(",")
ex = df.explode("genre_list")
ex["genre"] = ex["genre_list"].str.strip()
ex = ex[ex["genre"] != ""]

# --- ana_10: Genre frequency and average rating ---
print("=== ana_10 ===")
g = ex.groupby("genre").agg(
    n_seasons=("av_rating", "size"),
    mean_rating=("av_rating", "mean"),
    median_rating=("av_rating", "median"),
).reset_index().sort_values("n_seasons", ascending=False)
g["mean_rating"] = g["mean_rating"].round(3)
g["median_rating"] = g["median_rating"].round(3)
print(g.to_string(index=False))

# --- ana_11: Genre rating change, 1990s vs 2010s ---
print("\n=== ana_11 ===")
ex["era"] = pd.cut(
    ex["year"],
    bins=[1989, 1999, 2009, 2018],
    labels=["1990–1999", "2000–2009", "2010–2018"],
)
era_g = (
    ex.groupby(["genre", "era"], observed=True)["av_rating"]
    .agg(["size", "mean"])
    .reset_index()
)
era_g["mean"] = era_g["mean"].round(3)
# pivot for readability
piv_mean = era_g.pivot(index="genre", columns="era", values="mean")
piv_size = era_g.pivot(index="genre", columns="era", values="size").fillna(0).astype(int)
# only keep genres with at least 30 seasons total
keep = piv_size.sum(axis=1) >= 30
piv_mean = piv_mean.loc[keep]
piv_size = piv_size.loc[keep]
piv_mean["delta_90s_to_10s"] = (piv_mean["2010–2018"] - piv_mean["1990–1999"]).round(3)
combined = pd.concat(
    [piv_mean, piv_size.add_suffix(" (n)")], axis=1
).sort_values("delta_90s_to_10s", ascending=False)
print(combined.to_string())

# --- ana_12: Crime/Drama vs other genres rise rate ---
print("\n=== ana_12 ===")
df["is_crime"] = df["genres"].fillna("").str.contains("Crime")
df["era"] = pd.cut(
    df["year"], bins=[1989, 1999, 2009, 2018], labels=["1990s", "2000s", "2010s"]
)
g2 = df.groupby(["era", "is_crime"], observed=True)["av_rating"].agg(["size", "mean"]).round(3)
print(g2.to_string())
