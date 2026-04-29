"""Within-show season arcs: do later seasons get worse?"""

import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/economist/00_tvs-golden-age-is-real/IMDb_Economist_tv_ratings.csv"

df = pd.read_csv(DATA)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year

# Only shows with at least 3 seasons in the dataset
keep = df.groupby("title").size().pipe(lambda s: s[s >= 3]).index
sub = df[df["title"].isin(keep)].copy()

# --- ana_13: Mean rating by seasonNumber (across all shows with >=3 seasons) ---
print("=== ana_13 ===")
arc = sub.groupby("seasonNumber").agg(
    n_seasons=("av_rating", "size"),
    mean_rating=("av_rating", "mean"),
    median_rating=("av_rating", "median"),
).reset_index()
arc["mean_rating"] = arc["mean_rating"].round(3)
arc["median_rating"] = arc["median_rating"].round(3)
arc = arc[arc["seasonNumber"] <= 12]  # cap noise
print(arc.to_string(index=False))

# --- ana_14: Final-vs-first season rating delta per show ---
print("\n=== ana_14 ===")
def first_last(group):
    g = group.sort_values("seasonNumber")
    if len(g) < 2:
        return None
    return pd.Series({
        "n_seasons": len(g),
        "first_rating": g["av_rating"].iloc[0],
        "last_rating": g["av_rating"].iloc[-1],
        "first_year": g["year"].iloc[0],
        "last_year": g["year"].iloc[-1],
        "delta": g["av_rating"].iloc[-1] - g["av_rating"].iloc[0],
    })

fl = (
    sub.groupby("title", group_keys=False)
    .apply(first_last, include_groups=False)
    .dropna()
)
print(f"Shows with >=3 seasons: {len(fl)}")
print(f"Mean delta (last - first): {fl['delta'].mean():.3f}")
print(f"% with delta > 0: {(fl['delta'] > 0).mean()*100:.1f}%")
print(f"% with delta < 0: {(fl['delta'] < 0).mean()*100:.1f}%")

print("\nTop 10 RISERS:")
print(fl.sort_values("delta", ascending=False).head(10).round(3).to_string())
print("\nTop 10 FALLERS:")
print(fl.sort_values("delta").head(10).round(3).to_string())
